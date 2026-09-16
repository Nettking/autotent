# Evidence register

Prepared 16 September 2026 for the candidate paper. This register distinguishes source-derived statements, newly constructed checks, and interpretation. It is not a validation certificate.

## Source versions

**D — original development account.** The manuscript directly describes the author's monitoring design, test procedure, and qualitative development observations. These are not new experimental findings or independently reproduced runs. Working provenance is retained separately from the public package. No private document is cited or offered as an accessible publication, and no private bibliographic record or document locator is included here.

**R — repository.** `Nettking/autotent`, default branch `final`, commit `814bb768aa9994b59e17437cb4964cefd3d11b0f`, tree `31930897139d581eb05fe826b973401683ae63e5`. All implementation claims refer to this version, not every historical deployment or generated binary.

| Source file | Git blob SHA | Material inspected |
|---|---|---|
| `machine_learning/image_analysis/count_pixels/grid_count.py` | `35b9d8ad2c2835f356d277adaf972bf28d78b7f9` | HSV ranges, crop, morphology, contour areas, CSV headers, directory traversal, zero filtering |
| `machine_learning/image_analysis/count_pixels/grid_count_rwy.py` | `84536a29c7de8cc4ff5854be16c22efdb3803e61` | HSV conversion and incompatible red/yellow/white bounds |
| `digital_twin/model/pim.thingml` | `765118e9462420c8dddd0480310ed172a55f463b` | State names, sessions, timers, guards, reply port |
| `digital_twin/model/pim_messages.thingml` | `95d36dbd79ea50e09eee3e690194214b0f942916` | Observation and reply declarations |
| `digital_twin/model/psm.thingml` | `19934afbe579332154b6ef45b9fcaa41d2c3fcb8` | MQTT topic and message declarations |
| `digital_twin/MQTT/communication/send_to_model.py` | `2519469496f8dfe09399b972444df2f29ff5b8c2` | Expected CSV fields, zero defaults, topic names, placeholder settings |
| `machine_learning/image_analysis/count_pixels/input.png` | `a8392978b619ebf1fd12cacd8a37f9774b2393d3` | Public illustration reused byte-for-byte as `figures/cultivation.jpg` |

**A — recovered acquisition material.** Two original top-camera endpoint files with filename dates 2023-07-05 and 2024-03-06, a capture script, and an operational log were accessed during the preparation sessions. The July file's Git-blob hash equals R's public `input.png`; both inspected originals are JPEG images of 3280 by 2464 pixels. The capture script has startup acquisition and a daily 07:59 condition. The log contains paired top-camera success and side-camera failure with a subsequent general acquisition message. No complete frame census, configuration history, or plant continuity study was completed. Private acquisition files and identifiers are not redistributed.

## Claim-to-source map

| Manuscript content | Source | Evidence class and limit |
|---|---|---|
| Indoor setup, top and side cameras | D; R public image | Development setting and illustrative scene, not an independent sample count |
| Image processor, Plant State Model, Python monitor, human-facing reports | D, stated directly in sections 3-4; R component files | Functional design; figure 2 does not claim current integrated execution |
| Cropping, HSV thresholding, contour measures, CSV | R green script | Literal implementation, not a recalibrated or validated segmentation method |
| Germination, seedling, growth, fruiting and distress interpretation | D; R PIM | Intended model categories; table 2 does not correct or validate the source guards |
| Flowering versus fruiting | R PIM and the intended interpretation in section 4.2 | `Fruting`/`Fruiting` are software labels; flower- or fruit-related colour evidence does not establish biological stage |
| Five-second MQTT replay and timer factor 1440 | D, stated directly in section 4.3 | Recorded development settings; not a newly reproduced or verified time-preserving replay |
| 258 days of hourly environmental data, six unusable image days, 252 image-days | D, stated directly in section 5.2 | Historical collection account, not a recovered archive census or evidence of hourly images |
| Expected transitions, two initialization messages, distress/recovery | D, stated directly in section 5.2 | Developer observations; no independent labels, linked execution trace, or accuracy estimate |
| Watering sequence and feature changes | D, stated directly in section 5.2 | Historical interpretation; dates unavailable; no treatment-aligned labels or causal analysis |
| Dates and partial acquisition success | A | Limited recovery inspection; no complete archive claim or failure rate |
| Four checks in table 3 | `checks/check_archived_operations.py` and `checks/results.json` | Constructed software checks, not execution of the original application or biological validation |
| Retain provenance, distinguish missing values from zero, explicit replay time | Present analysis of D/R/A | Recommendations, not features claimed to exist in the historical implementation |

## New check method and constraints

The constants and the CSV/default-zero and plotting operations are manually transcribed from the pinned files listed above. This choice avoids importing interactive scripts, running acquisition programs, contacting a broker, or silently changing the application. The checker runs only these constructed examples:

- A single HSV point `(50,60,100)` against the three archived green ranges.
- Six constructed RGB colours converted by the current check environment to standard 8-bit HSV and tested against the archived red/yellow/white ranges.
- A non-zero constructed exporter-format CSV row read with the sender's expected field names and default-zero expression.
- Two short constructed series subjected to the archived per-channel removal of zero values.

The software reports the installed OpenCV/NumPy versions; those versions are **not** asserted to be the historical environment. The checker produces four source-level outcomes. Unit tests cover those outcomes, bibliography-key integrity, and a publication-source boundary check. These outcomes verify the limited examples, not the original pipeline, ThingML compilation, MQTT round trip, scientific novelty, or submission readiness.

The incompatible red/yellow/white hue bounds are also outside the documented 0-179 domain for standard 8-bit HSV. The six-colour check illustrates this configuration issue; it is not a six-image biological dataset. The conceptual source interpretation is kept separate from potential corrections.

## External references verified for this draft

The short related-work discussion is contextual, not a systematic review or performance comparison. Sources consulted:

- Harrand et al. (2016), ThingML, primary SINTEF publication record: https://www.sintef.no/en/publications/publication/0198cc602765-d996d4b6-c09e-469e-a574-3b9a3a6f6dd7/ . Author list, venue, pp. 125-135, DOI `10.1145/2976767.2976812` and abstract checked.
- Jans-Singh et al. (2020), primary Cambridge repository publication record: https://www.repository.cam.ac.uk/items/233c2831-f478-49b6-9f88-a14a899ea7cb . Journal, authors, volume and DOI `10.1017/dce.2020.21` checked; contextual claims limited to the abstract.
- David et al. (2023), official MODELS conference record: https://conf.researchr.org/details/models-2023/models-2023-technical-track/5/Digital-Twins-for-Cyber-Biophysical-Systems-Challenges-and-Lessons-Learned . Author list, venue and abstract checked; no detailed empirical findings borrowed from an unread full text.
- Haugen et al. (2025), https://arxiv.org/abs/2510.12478 and https://arxiv.org/html/2510.12478v1 . Authorship, DOI and strawberry modelling example checked. Shared case disclosed; no new authorship assigned to this candidate.
- OpenCV, versioned *Changing Colorspaces* documentation: https://docs.opencv.org/4.0.0/df/d9d/tutorial_py_colorspaces.html . The indexed official text specifies standard 8-bit HSV hue 0-179 and saturation/value 0-255. Direct page rendering was unavailable; the indexed official text was readable. No claim about the latest OpenCV version is made.

## Explicitly unsupported claims

No quantified growth-stage or health accuracy; no validated watering diagnosis; no reconstructed treatment dates; no independent biological replications inferred from frames or section sessions; no verified complete image dataset; no present end-to-end build or deployment; no demonstrated resource/yield gains; no regression superiority; no guarantee of acceptance or publication. Author approval and confirmation of the historical executed configuration remain pending.
