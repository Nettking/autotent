# Evidence register — executed pilot revision

Prepared 16 September 2026. No private document is a bibliographic dependency. The paper distinguishes design, source inspection, actual image execution, provisional reference agreement and unexecuted integration.

## Pinned public source

Repository `Nettking/autotent`, historical `final` commit `814bb768aa9994b59e17437cb4964cefd3d11b0f`, tree `31930897139d581eb05fe826b973401683ae63e5`.

| File | Git blob |
|---|---|
| `machine_learning/image_analysis/count_pixels/grid_count.py` | `35b9d8ad2c2835f356d277adaf972bf28d78b7f9` |
| `machine_learning/image_analysis/count_pixels/grid_count_rwy.py` | `84536a29c7de8cc4ff5854be16c22efdb3803e61` |
| `digital_twin/model/pim.thingml` | `765118e9462420c8dddd0480310ed172a55f463b` |
| `digital_twin/model/pim_messages.thingml` | `95d36dbd79ea50e09eee3e690194214b0f942916` |
| `digital_twin/model/psm.thingml` | `19934afbe579332154b6ef45b9fcaa41d2c3fcb8` |
| `digital_twin/MQTT/communication/send_to_model.py` | `2519469496f8dfe09399b972444df2f29ff5b8c2` |
| Public `input.png`, reused as `figures/cultivation.jpg` | `a8392978b619ebf1fd12cacd8a37f9774b2393d3` |

The copy at `pilot/archived/grid_count.py` is byte-identical and hash-checked before execution. Functions are extracted without executing the interactive top level. The pilot does not execute native ThingML; transfer of its binary into the execution environment was blocked. That is not evidence of an application-startup failure.

## Claim-to-evidence map

| Claim | Evidence and boundary |
|---|---|
| Prototype decomposition, state names/timers/messages | Public implementation and explicit design interpretation; not end-to-end execution |
| 24 readable originals, dimensions and dates | `pilot/manifest.csv`; selected-file census only, private image bytes hash-checked |
| 864 point labels; 41 F, 806 B, 17 U | Frozen `reference_points.csv`; AI-assisted, not human-reviewed |
| Provisional flower/fruit witnesses | Frozen `reference_scenes.csv`; not_seen is not proof of absence |
| TP35/FP0/FN6/TN806, pooled F1 .921 | Actual `points_scored.csv`, recomputable summary and per-frame scores; point agreement only |
| Method B/cutoff variants identical at sample points | Same scored points; dense masks differ, so not equal segmentation accuracy |
| No red/yellow/white pixels on all 24 images | Literal archived HSV bounds applied to real decoded images; no corrected detector validation |
| 71 nonzero values lost by original lookup | Exporter-style rows constructed from actual original-function measurements, original lookup expression |
| 72/72 strict-mapped fields preserved | Actual observation envelopes from the new adapter; no native delivery or region mapping |
| Repeatability | Second 24-image run: exact measurements/scores/envelopes excluding timing and run timestamps |
| Fifteen passing artifact tests | Six original and nine pilot tests; not biological validation experiments |
| No causal watering/state accuracy claim | Intervention dates and suitable independently reviewed state references are unavailable |

## Frozen data identity

The ZIP is a compact transport for the original CSV/JSON bytes, not a replacement for the source images. Run `python pilot/unpack_records.py` to inspect the records. They have these SHA-256 hashes:

- `manifest.csv`: `c16269f30b1c1b0f0e2728b2d91653118033b5f320c7879f910d2eddfd284ec2`
- `reference_points.csv`: `7534b20ad29ec264385a76a913046f645179d4f03cd5a27488a78c9082053cbe`
- `reference_scenes.csv`: `5ac575559ac476784ae1ebe0484f51f8b0f3943f14cf2e05881700ba5bca6f72`

Point labels were frozen before image-algorithm outputs at 09:18:27 UTC; scene labels at 09:28:18 UTC. First run was recorded at 09:28:29 UTC. `reference_freeze.json` retains the pre-run protocol digest. The public protocol received only a documented editorial privacy-wording amendment afterward; sampling and scoring rules were not changed. The labels remain unchanged after scoring.

## Interpretation and privacy

The same AI assistant prepared the reference labels and the analysis. No human/independent expert reference or complete blinding is claimed. No germination/seedling transition is observed in this sample; no whole-system plant-state accuracy, disease diagnosis, watering-cause result, agronomic gain or generalization across independent cultivation runs is established. No private image, reference crop, operational log, Drive ID or private document was uploaded to GitHub.

The original four diagnostic examples in `checks/` remain supplementary source-level examples. They are not the real-image validation and are not substituted for it. The main paper now reports the executed pilot rather than relying on unverifiable historical run quantities.

## Public external references

The six bibliography entries are the pinned software, ThingML (Harrand et al., 2016; DOI 10.1145/2976767.2976812), the urban hydroponic twin (Jans-Singh et al., 2020; DOI 10.1017/dce.2020.21), the MODELS cyber-biophysical study (David et al., 2023), DarTwin/SysMLv2 (Haugen et al.; arXiv:2510.12478v1), and versioned OpenCV 4.0.0 colourspace documentation. Related work is contextual, not a systematic review or empirical benchmark comparison. Standard 8-bit HSV's hue domain 0–179 was rechecked in official OpenCV documentation for this pilot.
