all: build
	python -m pip install --upgrade .

build:
	rm -rf dist
	python -m build

upload: build
	python -m twine upload --repository pypi dist/*
