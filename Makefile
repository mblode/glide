PYTHON := python3
VENV_PYTHON := .venv/bin/python
VERSION := $(shell cat version.txt)

.PHONY: venv build verify clean zip proof

venv:
	$(PYTHON) -m venv .venv
	. .venv/bin/activate && python -m pip install -r requirements.txt

build:
	. .venv/bin/activate && python build/release.py build --force

verify:
	. .venv/bin/activate && python build/release.py verify

clean:
	. .venv/bin/activate && python build/release.py clean

zip: build
	. .venv/bin/activate && python build/release.py zip

proof: build
	$(PYTHON) -m http.server 8765
