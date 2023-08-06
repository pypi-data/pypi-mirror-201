build:
	python -m build

pip: build
	python -m twine upload --repository pypi dist/*
