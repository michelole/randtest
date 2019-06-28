# Global parameters
SHELL := /bin/bash
PYEXE := python3

# Main
.PHONY: all help program
all: program

help: Makefile
	@sed -n 's/^##//p' $<

program:
	@echo "Commands for package management"
	@echo "make help"


## install:  Install package
.PHONY: install
install:
	$(PYEXE) -m pip install .


## develop:  Install development package
.PHONY: develop
develop:
	$(PYEXE) -m pip install -e .


## example_smart_drug:  Run the smart drug example
.PHONY: example_smart_drug
example_smart_drug:
	$(PYEXE) examples/smart_drug.py


## tests:  Run tests
.PHONY: tests
tests:
	cd tests/; make tests; cd -
