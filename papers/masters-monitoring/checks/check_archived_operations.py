#!/usr/bin/env python3
"""Four bounded, offline checks of transcribed archived operations.

These are NOT tests of the complete original application or biological accuracy.
The literals and reader/plot operations are transcribed from the pinned files
listed in SOURCE. No historical modules are imported or executed. No camera,
actuator, MQTT broker, credential, or private image is used.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
from pathlib import Path
from typing import Any

import cv2
import numpy as np

SOURCE_COMMIT = "814bb768aa9994b59e17437cb4964cefd3d11b0f"
SOURCE = {
    "green": {
        "path": "machine_learning/image_analysis/count_pixels/grid_count.py",
        "git_blob": "35b9d8ad2c2835f356d277adaf972bf28d78b7f9",
    },
    "rwy": {
        "path": "machine_learning/image_analysis/count_pixels/grid_count_rwy.py",
        "git_blob": "84536a29c7de8cc4ff5854be16c22efdb3803e61",
    },
    "sender": {
        "path": "digital_twin/MQTT/communication/send_to_model.py",
        "git_blob": "2519469496f8dfe09399b972444df2f29ff5b8c2",
    },
}
GREEN = {
    "light_green": ((30, 85, 30), (90, 255, 255)),
    "medium_green": ((40, 30, 30), (70, 85, 255)),
    "dark_green": ((30, 30, 30), (90, 85, 255)),
}
RWY = {
    "white": ((220, 220, 220), (255, 255, 255)),
    "yellow": ((255, 160, 0), (255, 255, 100)),
    "red": ((255, 0, 0), (255, 75, 30)),
}


def run_checks() -> dict[str, Any]:
    """Return observations and check outcomes; do not write unless requested."""
    hsv_pixel = np.array([[[50, 60, 100]]], dtype=np.uint8)
    overlap = [name for name, (lo, hi) in GREEN.items()
               if int(cv2.inRange(hsv_pixel, np.array(lo), np.array(hi))[0, 0])]

    names = ["red", "yellow", "white", "green", "blue", "black"]
    rgb = np.array([[[255, 0, 0], [255, 255, 0], [255, 255, 255],
                     [0, 255, 0], [0, 0, 255], [0, 0, 0]]], dtype=np.uint8)
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    rwy_matches = {name: int(cv2.countNonZero(cv2.inRange(
        hsv, np.array(lo), np.array(hi)))) for name, (lo, hi) in RWY.items()}

    # These are exactly the exporter-style header construction and the
    # sender's absent-key/default-zero operation, applied to a synthetic row.
    headers = (["Image Index"] + [f"{c.capitalize()} Num Leaves" for c in GREEN]
               + [f"{c.capitalize()} Total Pixel Count" for c in GREEN])
    stream = io.StringIO()
    writer = csv.writer(stream)
    writer.writerow(headers)
    writer.writerow([0, 1, 2, 3, 100, 200, 300])
    stream.seek(0)
    row = next(csv.DictReader(stream))
    reader_keys = ["light_green_pixel_count", "green_pixel_count", "dark_green_pixel_count"]
    decoded = {key: int(row.get(key, 0)) for key in reader_keys}

    series = [[7, 0, 9], [7, 8, 0]]
    filtered = [[value for value in values if value != 0] for values in series]
    source_indices = [[i for i, value in enumerate(values) if value != 0]
                      for values in series]
    outcomes = {
        "green_range_overlap": {
            "input_hsv": [50, 60, 100], "matching_channels": overlap,
            "confirmed": overlap == ["medium_green", "dark_green"],
        },
        "unreachable_rwy_hue": {
            "input_rgb_names": names, "converted_hsv": hsv[0].tolist(),
            "matching_pixel_counts": rwy_matches,
            "confirmed": all(v == 0 for v in rwy_matches.values()),
        },
        "csv_header_default_zero": {
            "writer_headers": headers, "input_areas": [100, 200, 300],
            "reader_values": decoded,
            "confirmed": all(v == 0 for v in decoded.values()),
        },
        "per_channel_zero_removal": {
            "input_series": series, "plotted_series": filtered,
            "retained_source_indices": source_indices,
            "confirmed": filtered == [[7, 9], [7, 8]] and source_indices[0] != source_indices[1],
        },
    }
    return {
        "schema": "autotent.paper.archived-operation-checks.v1",
        "source_commit": SOURCE_COMMIT,
        "scope": "Constructed checks of manually transcribed source values/operations; not historical replay or biological validation",
        "sources": SOURCE,
        "environment": {"opencv": cv2.__version__, "numpy": np.__version__},
        "checks": outcomes,
        "all_confirmed": all(item["confirmed"] for item in outcomes.values()),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Optional JSON report path; no source files are changed")
    args = parser.parse_args()
    report = run_checks()
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if report["all_confirmed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
