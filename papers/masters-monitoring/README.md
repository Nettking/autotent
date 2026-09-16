# Candidate paper: indoor strawberry monitoring

**Image-Driven Plant-State Monitoring of Indoor Strawberries: A Prototype Implementation**

A written, ten-page candidate manuscript derived from Martin Arthur Andersen's master's thesis and the preserved `autotent` implementation. It is not a submission, a new cultivation experiment, or a validated plant-health classifier.

- Branch: `paper/masters-monitoring-candidate-2026-09-16`.
- Base: `final` at `814bb768aa9994b59e17437cb4964cefd3d11b0f`.
- Scope: camera-derived colour measurements, the ThingML Plant State Model, monitoring interfaces, historical observations, and bounded source-inspection findings.
- Working format: LNCS. No venue has been selected or submission made. A document compiling in LNCS is not evidence of venue eligibility.

## Read and build

The complete manuscript is `main.tex`, with seven bibliography entries in `references.bib`. It includes a cultivation photograph already public in this repository, an information-flow diagram, the literal green-range configuration, the conceptual state interpretation, and four small software-check results. The PDF supplied with the conversation is a compiled reading copy; the repository stores its reproducible sources rather than a multi-megabyte PDF binary.

From this directory:

```sh
make pdf
make check
make test
```

Open `build/main.pdf`. Requirements for the paper are a TeX installation with `llncs`, `splncs04`, TikZ, `microtype`, `xurl`, and the standard packages named in `main.tex`. `make pdf BIBTEX=bibtex.original` works on installations that provide the underlying BibTeX under that name. The Python checks need Python 3.9 or later, NumPy, and OpenCV. They do not need cameras, a broker, credentials, or the private Drive archive.

For Overleaf, import the source ZIP, select `main.tex`, and compile with pdfLaTeX/BibTeX. The image is included. No online acquisition or shell escape is needed.

## What the evidence does and does not establish

`EVIDENCE.md` maps manuscript claims to thesis sections and pinned source files. Historical replay observations are attributed to the thesis. The new checks use explicitly transcribed source fixtures; they do not execute the historical application or establish the behaviour of a generated ThingML binary.

`checks/results.json` records four expected source-level consequences. Five accompanying unit tests pass, including bibliography-key integrity. Passing these checks means the diagnostic examples behave as stated, **not** that the monitoring application passes acceptance testing. In particular, the checks demonstrate incompatible or ambiguous configurations rather than validating plant classifications.

Watering dates, independent plant-state labels, a complete verified image inventory, biological accuracy estimates, and a confirmed executed historical configuration remain unavailable or unestablished. They are not invented. Environmental forecasting results, sensor maintenance, energy/noise measurements, FCP, and newer architectural research are excluded from the contribution.

## Essential author review before submission

1. **Historical implementation:** identify whether the pinned source matches the version actually used. Review the HSV bounds, overlapping channels, CSV mapping, MQTT topics/message types, state guards, and replay timing. Any fixes must be separately documented; the original application files were not changed by this paper branch.
2. **Contribution and venue:** decide whether a prototype/implementation account with this evidence is sufficient for the selected venue. This draft makes no acceptance claim. A small integration demonstration may be needed, but a large annotation campaign or new cultivation experiment is not silently made a prerequisite.
3. **Authorship and provenance:** confirm coauthors, affiliation, original thesis title/deposit year, and reuse/permissions. The supplied thesis cover says 16 September 2026; this is not assumed to be the original degree year. The existing DarTwin/SysMLv2 paper is cited and its shared case acknowledged.
4. **Submission declarations:** approve the manuscript, AI-use statement, data availability, venue format/anonymity, and any supplementary release. Nothing has been submitted, merged, or added to the personal website.

## Privacy and scope of repository changes

All additions are below `papers/masters-monitoring/`. The existing source and `final` branch are unchanged. No private Drive photographs, operational logs, cloud file identifiers, network addresses, or thesis PDF are uploaded. `figures/cultivation.jpg` reuses the already-public Git blob of `machine_learning/image_analysis/count_pixels/input.png` without alteration. The figure is illustrative and contains no newly assigned biological labels.
