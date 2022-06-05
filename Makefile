SRC := src/injectme

.PHONY: test
test:
	python3 -m unittest discover -s $(shell pwd)/tests -t $(shell pwd)

.PHONY: install
install:
	pip install -e .

.PHONY: black
black:
	python3 -m black --check $(SRC)

.PHONY: flake8
flake8:
	python3 -m flake8 $(SRC)

.PHONY: pylint
pylint:
	python3 -m pylint --disable=C0114,C0115,C0116 $(SRC)

.PHONY: requirements
requirements:
	pip-compile requirements.in > requirements.txt
