"""Small PyQGIS example: the same municipal buffer -> bounding box as PR6.

In a QGIS console call make_roi(processing.run, municipal_layer). The two returned
layers are temporary: export them to new named GeoPackage layers and reopen them.
The review activity supplies its recorded Processing callback and persists both.
"""

import math


def make_roi(run_algorithm, municipal_layer, distance=500):
    if not municipal_layer.isValid() or municipal_layer.crs().authid() != "EPSG:25831":
        raise ValueError("Expected a valid municipal layer in EPSG:25831")
    if municipal_layer.subsetString() or municipal_layer.selectedFeatureCount():
        raise ValueError("Clear filters and selections before comparing the model")
    rows = list(municipal_layer.getFeatures())
    if len(rows) != 1 or rows[0].geometry().isEmpty() or not rows[0].geometry().isGeosValid():
        raise ValueError("Expected one nonempty valid municipality")
    if not math.isfinite(distance) or distance <= 0:
        raise ValueError("The margin must be a positive distance in metres")
    buffered = run_algorithm("native:buffer", {
        "INPUT": municipal_layer, "DISTANCE": distance, "SEGMENTS": 8,
        "END_CAP_STYLE": 0, "JOIN_STYLE": 0, "MITER_LIMIT": 2,
        "DISSOLVE": False, "SEPARATE_DISJOINT": False, "OUTPUT": "TEMPORARY_OUTPUT",
    })["OUTPUT"]
    roi = run_algorithm("native:boundingboxes", {"INPUT": buffered, "OUTPUT": "TEMPORARY_OUTPUT"})["OUTPUT"]
    return buffered, roi
