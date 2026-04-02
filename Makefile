PYTHON := python3
VENV_PYTHON := $(shell [ -x .venv/bin/python ] && echo .venv/bin/python || echo python3)
VERSION := $(shell cat version.txt)

.PHONY: venv build verify clean zip proof

venv:
	$(PYTHON) -m venv .venv
	.venv/bin/python -m pip install -r requirements.txt

build:
	$(VENV_PYTHON) build/release.py build --force

verify:
	$(VENV_PYTHON) build/release.py verify

clean:
	$(VENV_PYTHON) build/release.py clean

zip: build
	$(VENV_PYTHON) build/release.py zip

proof: build
	$(PYTHON) -m http.server 8765
