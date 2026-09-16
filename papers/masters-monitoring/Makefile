PYTHON ?= python3
PDFLATEX ?= pdflatex
BIBTEX ?= bibtex

.PHONY: pdf check test records pilot human-score clean
pdf:
	mkdir -p build
	$(PDFLATEX) -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
	cd build && BIBINPUTS=..: $(BIBTEX) main
	$(PDFLATEX) -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
	$(PDFLATEX) -interaction=nonstopmode -halt-on-error -output-directory=build main.tex

records:
	$(PYTHON) pilot/unpack_records.py

check:
	$(PYTHON) checks/check_archived_operations.py

test: records
	$(PYTHON) -m unittest discover -s checks -v
	$(PYTHON) -m unittest discover -s pilot -v

pilot: records
	@test -n "$(IMAGES)" || (echo 'Set IMAGES=/absolute/path/to/originals'; exit 1)
	$(PYTHON) pilot/run_pilot.py --images "$(IMAGES)" --output build/pilot-rerun

human-score:
	$(PYTHON) pilot/rescore_human.py --labels pilot/human_review/labels.json --output build/human-rescore

clean:
	rm -rf build
