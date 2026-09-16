PYTHON ?= python3
PDFLATEX ?= pdflatex
BIBTEX ?= bibtex

.PHONY: pdf check test clean

pdf:
	mkdir -p build
	$(PDFLATEX) -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
	cd build && BIBINPUTS=..: $(BIBTEX) main
	$(PDFLATEX) -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
	$(PDFLATEX) -interaction=nonstopmode -halt-on-error -output-directory=build main.tex

check:
	$(PYTHON) checks/check_archived_operations.py

test:
	$(PYTHON) -m unittest discover -s checks -v

clean:
	$(PYTHON) -c "import shutil; shutil.rmtree('build', ignore_errors=True)"
