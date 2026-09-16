# Executed retrospective image-component pilot

16 September 2026. Status: **executed; provisional AI-reference agreement; native ThingML integration not executed; not submission-ready**.

## What was executed

The pinned original `grid_count.py` functions were executed on **24 original top-camera photographs**, not screenshots or synthetic plant images. The sample comprises **16 calendar-spread frames** (5 July 2023–6 March 2024) and **8 consecutive filename dates** (24–31 August 2023). All 24 files decoded as 3280 × 2464 JPEG images; the original 100-column right crop was retained. Image bytes total 132,597,616. This is a selected-frame inventory, not a census of the archive or 24 independent cultivation trials.

The original function slice is verified against Git blob `35b9d8ad2c2835f356d277adaf972bf28d78b7f9` before execution. Its returned contour counts and areas matched the scoring harness on all 24 images. The interactive historical area threshold is unknown; the pilot uses 100, with sensitivity at 0 and 1000. There was no score-driven tuning.

## Reference procedure and its limits

A fixed 6 × 6 grid was visually assessed on every cropped image, yielding **864 points**. The labels are **41 foliage, 806 background, and 17 uncertain**. Original-image neighbourhoods were inspected without algorithm masks or feature values. Point labels were frozen at 09:18:27 UTC and scene observations at 09:28:18 UTC, before the first algorithm run recorded at 09:28:29 UTC. Hashes and the complete labels are retained in `records.zip`.

**The annotator was an AI assistant. No human or botanical expert has reviewed the labels.** The same assistant had read the method description and prepared the code. These are provisional visual reference labels, not independent human ground truth, and the work is not a fully blinded experiment. Labels have not been changed after scoring.

The labels assess visible green strawberry leaf tissue. Uncertain boundaries, ambiguous colour and other-plant identity remain uncertain. Scene-level flower/fruit observations are presence witnesses; “not seen” is not scored as proof of absence. No watering treatment or disease labels were assigned.

## Measured agreement

A is the union of filled retained external contours from the archived green configuration. B is a separately identified binary-union variant using the same raw ranges before morphology, preserving binary pixels/holes and omitting contour-area filtering.

| Sample | Frames | Assessed points | Foliage references | TP | FP | FN | TN | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Calendar-spread | 16 | 560 | 27 | 25 | 0 | 2 | 533 | 0.926 | 0.962 |
| Consecutive sequence | 8 | 287 | 14 | 10 | 0 | 4 | 273 | 0.714 | 0.833 |
| Pooled | 24 | 847 | 41 | 35 | 0 | 6 | 806 | 0.854 | 0.921 |

A at cutoffs 0/100/1000 and B all give these same **sampled-point** predictions. Their dense masks and foreground measurements differ. Pooled precision is 1.000 on this limited set; that is not evidence of zero false positives throughout the images. The all-background baseline has 95.2% point accuracy and zero foliage recall. Accordingly, A's 99.3% overall point accuracy is not a useful validation headline.

Assigning all 17 uncertain labels against or in favour of the predictions gives pooled F1 bounds **0.753–0.925**. These are sensitivity bounds, not confidence intervals or independently adjudicated labels.

Six missed foliage points occur at July 20/point 11, August 20/point 17, and August 28–31/point 28. Four errors therefore repeat the same coordinate on successive dates. They must not be treated as independent failures.

## Actual image and interface findings

**Flower/fruit configuration:** every archived red/yellow/white range produced zero pixels in **24/24 images**. Provisional source-image inspection recorded flower witnesses in **11 frames** and a red-fruit witness in **one frame**. Standard 8-bit HSV bounds with lower hue 220/255 cannot detect these objects. This is a counterexample to the archived configuration, not a validated corrected flower detector. No replacement flower thresholds were tuned in this pilot.

**Colour overlap:** summed filled-channel pixel memberships divided by the union ranged from **1.019 to 1.932**, median **1.310**. Channels cannot be added as disjoint foliage classes. This calculation compares raster counts with raster counts; analytic contour areas are recorded separately.

**Real CSV hand-off:** the 24 frames produced **72 fields, including 71 non-zero values**. The archived sender's key/default expression returns **72 zeros** on those exporter-style rows. The new strict adapter preserves **72/72 values**, retaining floats and rejecting missing, negative and non-finite values. Its output includes image/date/hash and explicit whole-frame units. It does not assign a plant-section ID or send a message to ThingML.

**Temporal measurement:** foreground fractions in the eight-day sequence were 4.311, 5.198, 5.301, 4.968, 4.772, 4.720, 4.004 and 4.280%. These are proportions of the cropped camera scene, not physical leaf area, growth-stage accuracy or evidence of a particular watering treatment. Perspective, occlusion and scene changes remain possible influences.

## Native integration: not completed

The native `model.jar` was not transferred into this runtime. The binary decoded-blob route raised a UTF-8 decoding error, binary materialization was unsupported, and direct container retrieval failed DNS. Base64 could be viewed through a text response but was not reliably materialized. **This is a retrieval/execution-environment blocker, not an observed failure of the model application.** No native ThingML build, MQTT round trip, state-transition evaluation or substitute interpreter is reported as executed.

The actual executed boundary is **original images → archived Python feature functions → scored masks and typed feature envelopes**. Existing topic/message/guard/initialization discrepancies still need a separately recorded native integration configuration.

## Repeatability and artifact checks

A second full 24-image run reproduced `points_scored.csv`, `per_frame_scores.csv` and `observations.jsonl` byte-for-byte. All other frame measurements matched except timing; summaries matched except run timestamp. Nine pilot artifact/regression tests and six existing paper tests pass. These are correctness checks on the evaluation machinery, not 15 biological validation experiments.

Environment: Python 3.13.5, OpenCV 4.13.0, NumPy 2.3.5, Pillow 12.3.0. The environment is recorded rather than attributed to the original installation.

## Corrections kept separate

The original application files and default branch are unchanged. New work is entirely under this paper directory. B is an explicit measurement variant; `strict_observations` is the new interface correction. The archived green function remains byte-identical. Invalid flower/fruit bounds and original state guards are not silently repaired.

## Publication consequence

This is now an **executed image-component pilot**, rather than only a narrative account or constructed diagnostics. It is still **not a validated plant-state system**. The sample begins with developed foliage; germination/seedling transitions and independently labelled state histories are missing. Human reference review, native integration and a suitable state-level reference remain necessary for broader claims. No causal watering-stress, disease, yield or resource-saving conclusion is supported.

Private images, crops, camera logs and cloud IDs are not published. Public frozen labels/results are in `records.zip`; use `python pilot/unpack_records.py` to inspect the CSV/JSON files. Full image reruns require authorized access to the original image bytes. A private offline reference worksheet is supplied separately in the conversation, without predictions or provisional answers.
