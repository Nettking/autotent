# Strawberry monitoring candidate — human-reference update

**Image-Driven Monitoring of Indoor Strawberries: A Prototype and Retrospective Pilot**

The executed 24-image component pilot now has **859 human-labelled points** from the system developer. Five points remain unreviewed. The primary point results are precision **0.973**, recall **0.563**, and F1 **0.713**. This is not independent expert validation, a validated plant-state classifier, a complete native ThingML/MQTT demonstration, or a submission.

Branch: `paper/masters-monitoring-candidate-2026-09-16`.
The original application remains at `final`, commit `814bb768aa9994b59e17437cb4964cefd3d11b0f`, unchanged.

## Current evidence

Read **`pilot/human_review/REPORT.md`** for the human-label audit, confusion counts, exclusions, comparison with the earlier AI reference, and post-hoc crop subset. On unchanged predictions, the extractor finds 36 of 64 foliage points and misses 28; it gives one false positive among 795 background points. The input CSV is hash-identified, with decisions encoded separately as `pilot/human_review/labels.json`. No blank is replaced by an AI answer.

The earlier AI-reference result (F1 0.921) remains in the original records and `pilot/REPORT.md` as historical evidence, not the current primary result. The change is in the reference labels, not algorithm tuning. Scene-level flower/fruit witnesses remain AI-assisted and unreviewed. The earlier 24-image execution and strict-adapter results are unchanged; native state-model integration remains unexecuted.

## Build, rescore, and test

```sh
cd papers/masters-monitoring
make pdf
make human-score
make test
```

Open `build/main.pdf`. A TeX installation with LNCS (`llncs`, `splncs04`), TikZ/PGFPlots, and the packages in `main.tex` is needed. Some installations require `make pdf BIBTEX=bibtex.original`. For Overleaf, import the source ZIP and compile `main.tex` using pdfLaTeX/BibTeX. Private images are not needed to build the paper.

Human rescoring uses the Python standard library and frozen predictions:

```sh
python pilot/rescore_human.py --labels pilot/human_review/labels.json --output build/human-rescore
```

It generates a scored-point CSV, per-frame CSV and summary. `pilot/human_review/results/summary.json` is the expected result. An authorized local user may instead provide the original human CSV through `--labels`; exact identities and coordinates are required. The raw reviewer name is not written into scored outputs.

`make test` runs 23 artifact checks: six paper/diagnostic checks, nine original pilot checks, and eight human-rescoring checks. The old AI records remain intact. Passing tests verifies the evaluation machinery, not the truth of every reference label or full-system biological validity.

## Original image execution and records

`pilot/records.zip` contains the original selected-frame manifest, AI point/scene labels, freeze records, measurements, prediction CSVs, and observation envelopes. Run `python pilot/unpack_records.py` to inspect them. `EVIDENCE.md` separates historical and current evidence.

An image rerun requires authorized access to the exact 24 originals and dependencies in `pilot/requirements.txt`:

```sh
python pilot/unpack_records.py
python pilot/run_pilot.py --images /absolute/path/to/originals --output /tmp/autotent-pilot-rerun
```

Use a fresh output directory. Image hashes are checked. No cameras, actuators, Drive account or MQTT broker are contacted. The archived function is unchanged; B is a separate variant, and the strict CSV adapter a separately documented correction. The current human-rescoring update did not run a new image experiment.

## Scope and remaining work

The supplied labels belong to the original whole-scene sample. A post-hoc restriction to the requested crop reuses 288 existing reviewed points; it is not a newly cropped-image evaluation. There is no need to discard the completed review or relabel the same 864 points.

Native integration, a suitable state-level reference, and stronger measurement validation remain necessary for broader claims. The sample does not establish germination/seedling transitions; intervention dates do not support watering-cause validation. Confirm authorship, affiliation, venue, originality, data access and AI-use declarations before submission.

No private source document is cited. Private photographs, reference crops, operational logs, cloud IDs, and the raw identifying review CSV are not released. Only public implementation material, normalized point decisions, and derived records are added. No PR, merge, deployment, submission or personal-website update is included.
