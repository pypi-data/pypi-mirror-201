.PHONY: build test clean

clean:
	rm -rf build
	rm -rf dist
	rm -rf hcs_cli.egg-info
	find . -name .DS_Store -delete
	find . -name "*.pyc" -delete
	
lint:
	python3 -m black .	

build:
	export SCM_REV=$(shell git rev-parse --short HEAD); \
	python3 setup.py sdist bdist_wheel

buildrelease:
	python3 setup.py sdist bdist_wheel

uninstall:
	pip3 uninstall -y hcs-cli

devinstall:
	export SCM_REV=$(shell git rev-parse --short HEAD); \
	pip3 install -e .

dev: clean uninstall lint build devinstall

SHELL := /bin/bash
test:
	python3 -m unittest discover ./tests

publish:
	twine upload dist/*

install:
	pip3 install hcs-cli

wait:
	sleep 30

release: clean buildrelease publish uninstall wait install

