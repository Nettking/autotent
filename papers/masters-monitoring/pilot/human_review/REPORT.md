# Human-reference rescoring of the strawberry image pilot

16 September 2026. **859 human-labelled points received; unchanged predictions rescored. Native state-model integration and lifecycle validation remain unestablished.**

## Received review and identity checks

The uploaded CSV contains all 864 original sample identities across 24 images. Reviewer R1 is the system developer and manuscript author. Of these points, 859 are labelled and flagged human-reviewed: 64 foliage (F), 795 other/background (B), and no uncertain (U) labels. The first five points in `top_20230705.png.jpg` remain blank and are excluded. They are not replaced by AI labels or assumed background.

All image names, point numbers, x/y coordinates, category values, and review flags passed validation. There are no duplicate sample identities. The labels belong to the original whole-scene grid, not a newly cropped/resampled grid.

Original CSV SHA-256: `099a6435723e4966b61f6994fb1e939a566c523df2cf5cc0ec66052717117148`.

`labels.json` retains the exact received decisions in original point order, using `.` for an unreviewed point. It binds the coordinates to the frozen reference-file hash. The reviewer's typed name is represented by R1 in this public record. No original photographs, private image derivatives, or raw identifying CSV are included.

## Evaluation method

The existing per-point predictions in `../records.zip` were joined to these labels. No images were reprocessed, no thresholds were tuned, no predictions were changed, and no reference labels were corrected after seeing scores. Blank and U entries are excluded from binary confusion counts. The original AI-reference records remain unchanged as a separate historical assessment.

The worksheet withheld pointwise predictions and AI answers. R1 nevertheless knows the system and had seen aggregate pilot results. This is single-developer human annotation, not an independent expert assessment, a fully blinded study, or multi-rater ground truth. The point review does not review the prior scene-level flower/fruit observations.

## Results for archived green extraction (A100)

| Sample | Images | Scored points | Foliage | Background | TP | FP | FN | TN | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Calendar-spread | 16 | 571 | 49 | 522 | 27 | 0 | 22 | 522 | 1.000 | 0.551 | 0.711 |
| Consecutive sequence | 8 | 288 | 15 | 273 | 9 | 1 | 6 | 272 | 0.900 | 0.600 | 0.720 |
| Combined | 24 | 859 | 64 | 795 | 36 | 1 | 28 | 794 | 0.973 | 0.563 | 0.713 |

The principal limitation exposed by this reference is missed foliage: 28 of 64 foliage points, or 43.75%, are missed. One point labelled background is classified as foliage. The A0/A100/A1000 and B variants give identical predictions at these sampled coordinates; this does not imply identical dense masks.

Overall point accuracy is 96.6%, but an all-background predictor already obtains 92.5% with zero foliage recall. Overall accuracy therefore conceals substantial missed foliage. Repeated frame/point observations are not independent cultivation trials; no confidence interval based on independent pixels is reported.

## Difference from the original AI-reference result

The historical AI comparison gave F1 0.921 on 847 determinate points. The human comparison gives 0.713 on 859 points. Predictions are unchanged; the reference sets and denominators differ. At 29 reviewed positions, the labels differ: 11 AI-B and 13 AI-U become human F; four AI-U become human B; and one AI-F becomes human B. No label is overwritten in either reference set. The original AI-only agreement was optimistic relative to this human assessment; this is not a measured degradation of the algorithm between runs.

## Requested crop: reuse without relabelling

As an explicitly post-hoc check, the existing labelled points inside the right half and central 80% of the original image were selected: x in [1640,3280), y in [246,2218). This retains 288 points, all reviewed, including 61 foliage and 227 background points. The unchanged predictions give TP34, FP1, FN27, TN226; precision 0.971, recall 0.557, F1 0.708.

This is a restriction of previously sampled points, not a cropped-image rerun, a new grid, a new independent experiment, or evidence of changed image-processing performance. It shows that the completed labels remain usable; removing wall/background points from the score does not remove the missed-foliage problem. The whole-scene result remains the primary result.

## Reproduce and verify

From `papers/masters-monitoring`:

```sh
python pilot/rescore_human.py --labels pilot/human_review/labels.json --output build/human-rescore
make test
```

Rescoring uses only the Python standard library and `pilot/records.zip`, not private image files. It generates a point-level joined CSV, per-frame results, and a JSON summary. `results/summary.json` is the frozen expected result. The received CSV and compact public labels reproduce the same metrics and joined rows; their input-file hashes necessarily differ. Eight new tests verify identities, coordinates, duplicate rejection, review flags, exclusions, metrics, the stated crop subset, and reproduction of the summary. Together with six existing paper checks and nine original pilot tests, all 23 tests pass. These are artifact checks, not 23 biological validation experiments.

## Publication consequence

The paper now has human-referenced evidence for the image component, with explicitly limited annotation independence and spatial coverage. It does not have validated plant-state reports, independent biological replication, a human-reviewed flower/fruit reference, or watering-cause labels. Native ThingML/MQTT execution remains the next technical integration task. The original application and `final` branch are unchanged.
