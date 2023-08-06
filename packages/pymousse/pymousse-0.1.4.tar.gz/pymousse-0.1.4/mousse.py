import os, contextlib, re, shlex, ast

from pathlib import Path
from tempfile import TemporaryDirectory
from concurrent import futures
from configparser import ConfigParser

import requests, bs4

from chardet import detect as detect_encoding
from tqdm import tqdm
from mosspy import Moss

_default_config = """
[moss]
[lang:java]
suffix = .java
search = *.java
comment = //
moss_lang = java
[lang:python]
suffix = .py
search = *.py
comment = #
moss_lang = python
[lang:processing]
suffix = .pde
search = *.pde
comment = //
moss_lang = java
[lang:c]
suffix = .c
search = *.c *.h
comment = ["//", ("/*", "*/")]
moss_lang = c
"""

config = ConfigParser()
config.read_string(_default_config)
config.read(Path("~/.config/mousse.ini").expanduser())

class Language :
    def __init__ (self, lang) :
        section = config[f"lang:{lang}"]
        self.suffix = section["suffix"]
        self.search = shlex.split(section["search"]) or ["*"]
        self.cmt_format = self._mk_cmt(section["comment"])
        self.moss_lang = section["moss_lang"]
    _spn = re.compile(r"\s{2,}")
    _spx = re.compile(r"(?<=\W)\s|\s(?=\W)")
    def _mk_cmt (self, cmt) :
        try :
            cmt = ast.literal_eval(cmt)
        except :
            pass
        if not isinstance(cmt, (list, tuple, set)) :
            cmt = [cmt]
        cmt = list(cmt)
        if isinstance(cmt[0], str) :
            self._cmt_left, self._cmt_right = cmt[0], ""
        else :
            self._cmt_left, self._cmt_right = cmt[0]
        choice = []
        for c in cmt :
            if isinstance(c, str) :
                choice.append(re.escape(c))
            elif isinstance(c, (tuple, list)) and len(c) == 2 :
                b, e = c
                choice.append(f"{re.escape(b)}.*?{re.escape(e)}")
            else :
                raise ValueError(f"invalid comment spec: {c!r}")
        self._cmt = re.compile("|".join(choice), re.M|re.S)
    def comment (self, src) :
        return self._cmt_left + self.clean(src) + self._cmt_right
    def clean (cls, src) :
        src = cls._cmt.sub("", src)
        src = cls._spn.sub(" ", src)
        src = cls._spx.sub("", src)
        return src

@contextlib.contextmanager
def chdir (path) :
    old = os.getcwd()
    try :
        os.chdir(path)
        yield
    finally :
        os.chdir(old)

class Assignment (object) :
    def __init__ (self, root, lang, projects="projects", report="moss", base=None) :
        self.root = Path(root)
        self.proj = self.root / projects
        self.report_dir = self.root / report
        self.lang = Language(lang)
        self.base = self.root / base if base else None
        self._tmp = TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
    def run (self, incremental, prune, absolute, clean, **args) :
        if not incremental or not self.report_dir.exists() :
            self.walk()
            url = self.submit()
            if not url.startswith("http://") or url.startswith("https://") :
                return "Failed to get report URL"
            self.download()
        if not self.extract(clean) :
            return "MOSS reported no matches"
        self.heatmap(prune, absolute, **args)
    def walk (self) :
        self.projects = []
        for path in tqdm(list(self.proj.iterdir()), desc="collecting", unit=" project") :
            if not path.is_dir() :
                # WARN: "unexpected file", path
                continue
            if path == self.base :
                continue
            self.projects.append(path.stem)
            self._load_source(path, path.stem)
        if self.base is not None :
            name, num = f"{self.base.stem}{self.lang.suffix}", 1
            while (self.tmp / name).exists() :
                name, num = f"{self.base.stem}-{num}{self.lang.suffix}", num+1
            self._base = name
            self._load_source(self.base, name)
    def _load_source (self, path, name) :
        with open(self.tmp / name, "w", encoding="utf-8") as out :
            out.write(self.lang.comment(f"FILE: {path}") + "\n")
            for source in self._search(path) :
                out.write(self.lang.comment(f"FILE: {source}") + "\n")
                src = source.read_bytes()
                enc = detect_encoding(src)["encoding"]
                if enc is None :
                    # WARN: "unknown encoding", source
                    enc = "utf-8"
                out.write(src.decode(encoding=enc, errors="replace"))
    def _search (self, path) :
        for child in path.iterdir() :
            if child.is_dir() :
                yield from self._search(child)
            elif any(child.match(s) for s in self.lang.search) :
                yield child
    def submit (self) :
        moss = Moss(config["moss"]["userid"], self.lang.moss_lang)
        with chdir(self.tmp) :
            if self.base is not None :
                moss.addBaseFile(str(self._base))
            for proj in self.projects :
                moss.addFile(str(proj))
            with tqdm(total=1 + len(self.projects),
                      desc="uploading", unit=" files") as log :
                def update (*args) :
                    log.update()
                self.report_url = moss.send(update).rstrip("/") + "/"
        self._tmp.cleanup()
        del self._tmp, self.tmp
        return self.report_url
    def _http_get (self, path, target) :
        req = requests.get(f"{self.report_url}{path}")
        if req.status_code == requests.codes.ok :
            html = req.text.replace(self.report_url, "")
            target.write_text(html, encoding="utf-8")
            return html
    def _html_refs (self, html) :
        soup = bs4.BeautifulSoup(html, "lxml")
        return set(link for a in soup.find_all("a")
                   if (link := a["href"]).startswith("match"))
    def download (self) :
        self.report_dir.mkdir(exist_ok=True)
        with tqdm(desc="downloading", unit=" pages") as log :
            main = self._http_get("", self.report_dir / "index.html")
            todo = set()
            for link in self._html_refs(main) :
                path = Path(link)
                base, suffix = path.stem, path.suffix
                todo.update([link,
                             f"{base}-0{suffix}",
                             f"{base}-1{suffix}",
                             f"{base}-top{suffix}"])
            log.total = len(todo)
            with futures.ThreadPoolExecutor(max_workers=10) as pool :
                tasks = [pool.submit(self._http_get, path, self.report_dir / path)
                         for path in todo]
                for done in futures.as_completed(tasks) :
                    log.update()
    def _extract_side (self, name, side) :
        path = self.report_dir / f"{name.stem}-{side}{name.suffix}"
        soup = bs4.BeautifulSoup(path.read_text(), "lxml")
        matches = {}
        for a in soup.find_all("a") :
            if not a.get("name", None) :
                continue
            txt = a.find_next_sibling("font").text.strip()
            matches[int(a["name"])] = self.lang.clean(txt)
        return [v for k, v in sorted(matches.items())]
    def _extract_details (self, name) :
        path = Path(name)
        return list(zip(self._extract_side(path, 0),
                        self._extract_side(path, 1)))
    _weight = re.compile("^(.*?)\s+\(([\d.]+)\%\)$")
    def extract (self, clean=True) :
        soup = bs4.BeautifulSoup((self.report_dir / "index.html").read_text(), "lxml")
        dists, copied, keys = {}, {}, set()
        source_matches = {}
        left = right = None
        self.report_map = {}
        for td in soup.find_all("td") :
            txt = td.text.strip()
            if left is None :
                match = self._weight.match(txt)
                left, wl = match.group(1), float(match.group(2)) / 100.0
                url = td.find("a")["href"]
            elif right is None :
                match = self._weight.match(txt)
                right, wr = match.group(1), float(match.group(2)) / 100.0
            else :
                source_matches[left,right] = self._extract_details(url)
                keys.update([left, right])
                c = float(txt)
                self.report_map[left, right] = self.report_map[right, left] = url
                dists[left, right] = dists[right, left] = (1.0 - 2*c / (c/wl + c/wr))
                copied[left, right] = copied[right, left] = max(wr, wl)
                left = right = None
        if not dists :
            return False
        from thefuzz import fuzz
        import pandas as pd
        data = []
        for (left, right), matches in source_matches.items() :
            data.extend(((left, right),
                         max(len(srcl), len(srcr))
                         * copied[left,right]
                         * fuzz.ratio(srcl, srcr))
                        for srcl, srcr in matches)
        score = pd.DataFrame(data, columns=["group", "score"])
        score["bad"] = score["score"] >= score["score"].mean()
        keep = set(score["group"][score["bad"]])
        keep.update([(b, a) for a, b in keep])
        keys = list(sorted(keys))
        with (self.root / "dists.csv").open("w") as df :
            df.write("," + ",".join(keys) + "\n")
            for row in keys :
                df.write(row)
                for col in keys :
                    if row == col :
                        df.write(",")
                    elif ((clean and (row, col) not in keep)
                          or (row, col) not in dists) :
                        df.write(",1.0")
                    else :
                        df.write(f",{dists[row,col]}")
                df.write("\n")
        return True
    def heatmap (self, prune=.5, absolute=False, **args) :
        import pandas as pd
        import numpy as np
        from scipy.cluster.hierarchy import ClusterWarning
        from warnings import simplefilter
        simplefilter("ignore", ClusterWarning)
        dists = pd.read_csv((self.root / f"dists.csv").open(), index_col=0)
        dists.fillna(1, inplace=True)
        kw = {"lnk" : {},
              "sns" : {"vmax" : 1.0 if absolute else dists.max().max(),
                       "cmap" : "RdYlBu"},
              "plt" : {}}
        for key, val in args.items() :
            if key[:3] in kw and key[3:4] == "_" :
                kw[key[:3]][key[4:]] = val
            else :
                raise TypeError(f"unexpected argument {key!r}")
        # draw whole heat,map
        a = (dists != 1).any()
        k = a[a]
        dists = dists[a][k.index]
        np.fill_diagonal(dists.values, 0)
        tree = self._heatmap(dists, "dists", kw)
        # prune outliers
        if prune is None or not tree.dist :
            return
        def _leaves (node) :
            if node.is_leaf() :
                return dists.index[node.get_id()]
        leaves = set()
        if 0 <= prune <= 1 :
            d = dists.values[np.triu_indices_from(dists.values, 1)]
            d = d[d < 1.0]
            cut = d.mean() - d.std() * prune
            todo = [tree]
            while todo :
                node = todo.pop()
                if node.dist / tree.dist <= cut :
                    if node.get_count() > 1 :
                        leaves.update(node.pre_order(_leaves))
                else :
                    if node.left :
                        todo.append(node.left)
                    if node.right :
                        todo.append(node.right)
        elif prune > 1 :
            forest = [tree]
            def sort_key (node) :
                return node.dist, -node.get_count()
            while sum(node.get_count() for node in forest) > prune :
                node = forest.pop(-1)
                for child in (node.left, node.right) :
                    if child and child.get_count() > 1 :
                        forest.append(child)
                forest.sort(key=sort_key)
            for node in forest :
                leaves.update(node.pre_order(_leaves))
        if keep := list(sorted(leaves - {None})) :
            sub = dists[keep]
            self._heatmap(sub[sub.index.isin(leaves)], "dists-pruned", kw)
    def _heatmap (self, dists, name, kw) :
        import numpy as np
        import seaborn as sns
        import matplotlib.pylab as plt
        from scipy.cluster.hierarchy import linkage, to_tree
        if len(dists) < 55 :
            kw["sns"] = kw["sns"].copy()
            kw["sns"].setdefault("xticklabels", 1)
            kw["sns"].setdefault("yticklabels", 1)
        link = linkage(dists.values[np.triu_indices(len(dists), 1)], **kw["lnk"])
        cg = sns.clustermap(dists, row_linkage=link, col_linkage=link, **kw["sns"])
        plt.setp(cg.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
        ax = cg.ax_heatmap
        xl = [t.label1.get_text() for t in ax.xaxis.get_major_ticks()]
        yl = [t.label1.get_text() for t in ax.yaxis.get_major_ticks()]
        mossdir = self.report_dir.relative_to(self.root)
        for i, x in enumerate(xl) :
            for j, y in enumerate(yl) :
                if x == y :
                    continue
                if url := self.report_map.get((x,y), None) :
                    ax.annotate("@", xy=(i+.5,j+.5), ha="center", va="center", alpha=0.0,
                                url=f"l{mossdir}/{url}",
                                bbox={"color": "w", "alpha": 0.0,
                                      "url": f"{mossdir}/{url}"})
        plt.setp(cg.ax_heatmap.xaxis.get_majorticklabels(), rotation=90)
        cg.savefig(self.root / f"{name}.pdf", **kw["plt"])
        plt.close(cg.fig)
        return to_tree(cg.dendrogram_row.calculated_linkage)

if __name__ == "__main__" :
    import argparse
    parser = argparse.ArgumentParser(prog="mousse",
                                     description="submit source to MOSS and extract data")
    parser.add_argument("-c", "--config", default=None, type=str,
                        help="configuration file (default: '~/.config/mousse.ini')")
    parser.add_argument("-i", "--incremental", default=False, action="store_true",
                        help="continue previously started analysis")
    parser.add_argument("-u", "--userid", default=None, type=int,
                        help="MOSS user id")
    parser.add_argument("-s", "--source", default="projects", type=str,
                        help="students' source location (default: 'projects')")
    parser.add_argument("-b", "--base", default=None, type=str,
                        help="base code location (default: none)")
    parser.add_argument("-r", "--report", default="moss", type=str,
                        help="where to save MOSS' report")
    parser.add_argument("-R", "--raw", default=False, action="store_true",
                        help="use raw distances with cleaning")
    parser.add_argument("-p", "--prune", default=0.5, type=float, metavar="P",
                        help="prune heatmaps at P (default: 0.5)")
    parser.add_argument("-a", "--absolute", default=False, action="store_true", 
                        help="use absolute scale for heatmap")
    parser.add_argument("-l", "--lang", default="c", type=str,
                        help="programming language (default: 'c')")
    parser.add_argument("-L", "--list-lang", default=False, action="store_true",
                        help="list available languages and exit")
    parser.add_argument("root", type=str, metavar="ROOT", nargs="?",
                        help="root directory for assignment")
    parser.add_argument("options", type=str, metavar="OPT", nargs="*",
                        help="options for heatmap drawing")
    args = parser.parse_args()
    # load config
    if args.config is not None :
        ini = Path(args.config).expanduser()
        if not ini.exists() :
            parser.exit(1, f"could not read config '{ini}\n'")
        config.read_file(ini.open(), str(ini))
    # process --list-lang/root or check chosen lang
    if args.list_lang :
        langs = ', '.join(k[5:] for k in config if k.startswith("lang:"))
        parser.exit(0, f"supported languages: {langs}\n")
    elif not args.root :
        parser.exit(1, "mousse: argument 'ROOT' is required\n")
    if f"lang:{args.lang}" not in config :
        parser.exit(1, f"mousse: unsupported language '{args.lang}'\n")
    # set userid
    if args.userid is not None :
        config["moss"]["userid"] = args.userid
    # check directories
    root = None
    for opt in ("root", "source", "base", "report") :
        name = getattr(args, opt)
        if name is None :
            continue
        elif root is None :
            root = path = Path(name)
        else :
            path = root / name
        if opt != "report" and not path.is_dir() :
            parser.exit(1, f"{parser.prog}: {opt} dir '{path}' not found\n")
    # analyse assignment
    options = {}
    for opt in args.options :
        k, v = opt.split("=", 1)
        options[k] = v
    if args.prune <= 0 :
        args.prune = None
    assign = Assignment(args.root, args.lang, args.source, args.report, args.base)
    msg = assign.run(args.incremental, args.prune, args.absolute, not args.raw, **options)
    if msg is not None :
        parser.exit(2, f"{msg}\n")
