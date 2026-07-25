# The Arithmetic of Intelligence — build
#
#   make install   fetch KaTeX and the three typefaces from npm
#   make pdf       build dist/The-Arithmetic-of-Intelligence.pdf
#   make figure    regenerate the cover figure from its equations
#   make audit     run the source consistency checks
#   make serve     preview the web edition at http://localhost:8000
#   make clean     remove build artefacts

.PHONY: all install figure prerender assemble pdf audit serve clean distclean
.DEFAULT_GOAL := pdf

PY ?= python3
NODE ?= node
VENV := .venv
VPYTHON := $(VENV)/bin/python

all: audit pdf

$(VENV):
	$(PY) -m venv $(VENV)
	$(VPYTHON) -m pip install -r requirements.txt

install: $(VENV)
	npm install

figure: $(VENV)
	$(VPYTHON) build/coverfig.py

prerender: node_modules
	$(NODE) build/prerender.js

assemble: prerender $(VENV)
	$(VPYTHON) build/assemble.py

pdf: assemble $(VENV)
	$(VPYTHON) build/topdf.py

audit: $(VENV)
	$(VPYTHON) tools/audit.py

serve:
	@echo "web edition -> http://localhost:8000"
	@cd src && $(PY) -m http.server 8000

node_modules:
	npm install

clean:
	rm -rf .cache

distclean: clean
	rm -rf dist node_modules $(VENV)
