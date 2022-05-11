.PHONY: run tests

build: requirements.txt
	pip install -r requirements.txt
	cd app/algo & pip install algo_module/ && cd ../..


tests:
	python -m pytest tests/ --disable-pytest-warnings -v


run:
	python start.py


fclean:
	rm -rf venv
