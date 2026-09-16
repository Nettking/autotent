# Retrospective image pilot, version 1 (16 September 2026)

Prepared before running image algorithms or inspecting their outputs on the pilot.
The two endpoint frames and an August 31 preview have been viewed in earlier sessions.
This is an exploratory within-archive pilot, not a preregistered independent experiment.

## Fixed sample
24 top-camera files: 16 calendar-spread frames plus 8 consecutive filename dates.
Calendar-spread: 20230705, 20230720, 20230805, 20230820, 20230905, 20230915,
20231020, 20231105, 20231120, 20231205, 20231220, 20240105, 20240120,
20240205, 20240220, 20240306.
Sequence: 20230824 through 20230831 inclusive.
Exact files were selected from the accessible folder listing, without algorithm results.
No substitution for a difficult or unreadable frame. This is not a complete archive census.
Top-camera scope only; side-camera generalization and plant identity across months are untested.

## Reference assessment before algorithm outputs
For each frame annotate a fixed 6x6 grid over the image after its historical 100-column
right crop. Grid centres are x=(j+0.5)/6 and y=(i+0.5)/6, i,j=0..5.
Each point: F=clearly visible green strawberry leaf tissue; B=other material;
U=uncertain/boundary/occluded or insufficient resolution. Include small non-strawberry
plants as B when distinguishable; otherwise U. Record global visible flowers/fruit as
present, not seen, or uncertain (not seen does not imply absence).
Use original image/crops without algorithm masks or feature values.
Annotations are produced by the assistant's visual inspection and MUST be called
AI-assisted provisional reference labels, not human/independent biological ground truth.
Save the labels before processing; no retrospective relabeling to improve agreement.
Provide an offline human-review worksheet without predictions. No human review has occurred.

## Image methods
A: archived green pipeline configuration: HSV bounds, 7x7 closing/opening twice,
external contours; chosen area cutoff 100 pixels, with sensitivity at 0 and 1000.
Historical interactive cutoff is unknown; these are pilot settings, not recovered settings.
Run at original resolution. Evaluate filled retained external-contour union at grid points;
record literal contour areas and individual channels separately, retaining all zero values.
B: same green hue/value domain without overlapping classes, S>=30, retain binary union;
this is a transparent new variant, not a biological correction.
Keep crop, timestamps and ordering explicit. Do not tune thresholds using reference labels.
Optional established baseline must be specified and distinguished before scoring.

## Scores and interpretation
Report TP/FP/FN/TN and uncertain exclusions, point precision/recall/F1 and point accuracy,
plus per-frame counts and foreground fraction. These are point-sample agreement measures,
NOT dense-mask IoU, physical leaf area, health accuracy or overall developmental accuracy.
If frames contain only mature vegetative/flowering plants, do not claim lifecycle coverage.
Measure sequence outputs with elapsed filename days retained. Do not invent treatment dates.

## Model integration
Attempt to establish an executable archived/generated ThingML configuration without live
cameras, real actuators or external brokers. Keep all changes under this pilot directory.
When toolchain/dependencies or source discrepancies block native execution, record the exact
blocker; any limited offline interpreter/port must be labeled separately, never as running
the original ThingML binary. Source checks alone are not a successful integration result.

## Reporting and privacy
Publish code, aggregate measurements, configuration and hashes on the existing paper branch.
Do not publish private images, previews, reference crops or Google Drive IDs/links.
Private source documents are not cited or uploaded. No changes to original application files or final.
All findings, including poor agreement and failed execution, must be retained.

Editorial note after execution: only the privacy wording above was generalized.
All sampling, annotation, algorithm and scoring rules are unchanged. The pre-run
protocol hash remains recorded in reference_freeze.json.
