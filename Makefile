.PHONY: test
test:
	python3 -m unittest discover -s $(shell pwd)/tests -t $(shell pwd)

