# Sources for the motivation and related-work revision

Prepared 16 September 2026. This is a targeted comparison, not a systematic review, new benchmark, or new experiment. The paper's human-reference results and execution boundaries are unchanged. Scientific descriptions below are based on primary publication material; comparative statements about the present prototype are the authors' analysis of its recorded evidence.

## Added primary studies

| Citation key | Primary material consulted | Supported use in the manuscript |
|---|---|---|
| `easlon2014` | Easlon and Bloom, *Applications in Plant Sciences* 2(7), 1400033 (2014). DOI `10.3732/apps.1400033`. Original article's indexed abstract and method: https://pmc.ncbi.nlm.nih.gov/articles/PMC4103476/ | Colour-ratio segmentation and red calibration area; contrast with uncalibrated scene fractions. |
| `gehan2017` | Gehan et al., *PeerJ* 5, e4088 (2017). DOI `10.7717/peerj.4088`. Original article's indexed methods and software descriptions: https://pmc.ncbi.nlm.nih.gov/articles/PMC5713628/ | White balancing, size normalization, multi-plant processing and trainable segmentation; no local benchmark claimed. |
| `minervini2016` | Minervini et al., *Pattern Recognition Letters* 81, 80–89 (2016). DOI `10.1016/j.patrec.2015.10.013`. Publisher abstract: https://www.sciencedirect.com/science/article/abs/pii/S0167865515003645 . Author-institution record: https://eprints.imtlucca.it/3541/ | Expert-annotated rosette data and distinct segmentation/counting/classification tasks; contrasts with sparse point labels. |
| `elhariri2023` | Elhariri, El-Bendary and Saleh, *Data in Brief* 48, 109165 (2023). DOI `10.1016/j.dib.2023.109165`. Original dataset article's indexed description and annotation procedure: https://pmc.ncbi.nlm.nih.gov/articles/PMC10165176/ | 247 images, 1,062 fruit boxes, six ripening categories; fruit rather than whole-plant or foliage references. |
| `wen2024` | Wen et al., WACV 2024. Official CVF abstract and BibTeX: https://openaccess.thecvf.com/content/WACV2024/html/Wen_The_Growing_Strawberries_Dataset_Tracking_Multiple_Objects_With_Biological_Development_WACV_2024_paper.html | Long-term tracking and identity under biological/environmental change; not equivalent to aggregate foreground trends. CVF page range 7104–7114 is retained from its own record. |
| `yang2024` | Yang et al., *Computers and Electronics in Agriculture* 220, 108911 (2024). DOI `10.1016/j.compag.2024.108911`. Indexed publisher abstract, introduction and section snippets: https://www.sciencedirect.com/science/article/pii/S0168169924003028 . Author data record confirms publication metadata: https://zenodo.org/records/10957909 | Fruit-trait detection, growth simulation and image assimilation; direct precedent against a generic image-plus-model novelty claim. |
| `xu2025` | Xu, Wang and Yang, *PeerJ Computer Science* 11, e2085 (2025). DOI `10.7717/peerj-cs.2085`. Original article's indexed abstract and dataset/method descriptions: https://pmc.ncbi.nlm.nih.gov/articles/PMC11784530/ | A lightweight learned fruit detector and stage classifier; no unsupported efficiency advantage for fixed thresholds. |
| `vargasrojas2024` | Vargas-Rojas et al., *Frontiers in Plant Science* 15, 1265073 (2024). DOI `10.3389/fpls.2024.1265073`. Original article's indexed abstract, methods and case descriptions: https://pmc.ncbi.nlm.nih.gov/articles/PMC10915008/ | Standardized collection, identifiers and column transformation; context for the specific CSV hand-off experiment. |

Several publisher/PMC direct-page requests returned access errors or a browser challenge. Search-indexed text from the same primary articles was readable. Descriptions are limited to that material; complete full-text review, systematic search completeness, detailed reanalysis, and reproduction of external results are not claimed. The comparison table summarizes tasks and reference types, not relative algorithm accuracy. Later publications are compared retrospectively; they are not presented as sources that guided the historical implementation.

## Retained public references

The pinned `autotent` repository, versioned OpenCV documentation, ThingML, the urban hydroponic twin, the MODELS cyber-biophysical study, and the DarTwin/SysMLv2 experiment remain cited. Bibliography size is 14 entries: 12 scientific publications, one software repository, and one documentation source.

The incomplete David et al. entry now includes DOI `10.1109/MODELS58315.2023.00014` and pages 1–12, verified against the lead author's publication record: https://istvandavid.com/publications/ . The official conference page supplies its abstract and authors: https://conf.researchr.org/details/models-2023/models-2023-technical-track/5/Digital-Twins-for-Cyber-Biophysical-Systems-Challenges-and-Lessons-Learned . Its treatment here remains limited to the industrial controlled-environment case and engineering challenges, not detailed claims borrowed from an unread experimental section.

Jans-Singh et al. metadata and abstract: https://www.repository.cam.ac.uk/items/233c2831-f478-49b6-9f88-a14a899ea7cb . The specific DarTwin reference remains the already-cited public arXiv version `2510.12478v1`; no status of a later version is inferred.

## Motivating example provenance

The operator decision is explicitly illustrative. The dates and A foreground fractions (27 August: 4.968%; 30 August: 4.004%) come from the already-executed eight-day sequence in `pilot/records.zip` and are already reported in the manuscript. The example's discussion of missing-field zeros comes from the existing CSV experiment. No operator action, warning event, watering treatment, biological cause, or new state-model execution is asserted. The figure is the unchanged already-public cultivation image.

## Unchanged evidence and boundaries

The human-reference labels, five excluded blanks, frozen predictions, point metrics, crop-subset results, image-processing parameters, and offline adapter results are not modified. External tools and datasets are discussed but not installed or benchmarked for this revision. Native ThingML/MQTT integration, independent expert reference review and full lifecycle validation remain unestablished. No private source document, images, crops, acquisition logs or identifying review CSV are released by this revision.
