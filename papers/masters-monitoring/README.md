# Strawberry monitoring candidate — executed image pilot

**Image-Driven Monitoring of Indoor Strawberries: A Prototype and Retrospective Pilot**

A written candidate with an executed **24-image component evaluation**. The frozen visual labels are **AI-assisted and unreviewed**. This is not a validated plant-state classifier, a complete native ThingML/MQTT demonstration, or a submission.

Branch: `paper/masters-monitoring-candidate-2026-09-16`.
The historical application remains at `final`, commit `814bb768aa9994b59e17437cb4964cefd3d11b0f`, unchanged.

## Main findings

Against 847 assessed grid points (41 provisional foliage references), archived green extraction gives TP=35, FP=0, FN=6, TN=806; pooled F1=0.921. Seventeen uncertain points are excluded. The all-background baseline has 95.2% accuracy, demonstrating why overall accuracy is misleading here.

Archived red/yellow/white bounds yield zero pixels on all 24 photographs despite provisional visual witnesses. The new strict CSV adapter preserves 72/72 extracted fields; the original header/default lookup turns all fields into zero. These are real-image component results, not native state-model validation. See **`pilot/REPORT.md`** for the complete outcome and execution boundary.

## Build and inspect

```sh
cd papers/masters-monitoring
make pdf
make test
```

Open `build/main.pdf`. A TeX installation with LNCS (`llncs`, `splncs04`), TikZ/PGFPlots, and the packages named in `main.tex` is required. On installations with that executable name, use `make pdf BIBTEX=bibtex.original`. The paper builds without access to private images. For Overleaf, import the source ZIP, choose `main.tex`, and use pdfLaTeX/BibTeX.

The compact frozen records are in `pilot/records.zip`. Extract them without altering different local records:

```sh
python pilot/unpack_records.py
```

This exposes the exact image manifest, point/scene references, freeze records, measured CSVs, observation envelopes and JSON summary. It contains no source photographs, private image crops, operational logs, or cloud identifiers. `EVIDENCE.md` distinguishes these records from the earlier constructed diagnostic checks.

## Re-run with authorized image access

Python 3.10+ and the dependencies in `pilot/requirements.txt` are required. The recorded execution used Python 3.13.5. With the 24 original files named as in the manifest:

```sh
python pilot/unpack_records.py
python pilot/run_pilot.py --images /absolute/path/to/originals --output /tmp/autotent-pilot-rerun
```

Use a new output directory to retain the frozen execution. Inputs must match the recorded SHA-256 hashes. Nothing contacts cameras, actuators, Drive, or a broker. The archived green function is checked against its original Git blob. B is an explicitly new measurement variant; the strict CSV adapter is a separate correction. Original application files are not patched.

`make test` runs six existing diagnostics/bibliography checks and nine pilot artifact/regression tests. Passing them confirms internal consistency, not human-reference agreement, biological accuracy, or submission readiness.

## Remaining scientific work

Human review of the provisional labels, an executable native integration configuration, and suitable state-level references remain necessary before claiming validated plant-state monitoring. The current sample does not establish germination/seedling transitions. Missing intervention dates prevent watering-cause validation. No publication claim follows from the document compiling.

Confirm author/coauthor details, affiliation, venue, originality, data access and AI-use declarations before submission. The shared case with the public DarTwin/SysMLv2 paper is acknowledged. Private documents are not cited, and private source images are not released. No PR, merge, deployment, submission or personal-website update is included.
