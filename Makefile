.PHONY: dist
dist:
	python -m build

.PHONY: upload
upload:
	python -m twine upload dist/*

.PHONY: upload-test
upload-test:
	python -m twine upload --repository testpypi dist/*
