#!/usr/bin/env python3
"""Inspect the retained classroom PR1 without saving either QGIS project.

Run with system Python for archive/SQLite checks and --retain. Run with the
pinned QGIS image and --qgis for geometry and relocated-project checks.
"""

import argparse
import hashlib
import io
import json
from pathlib import Path
import sqlite3
import xml.etree.ElementTree as ET
import zipfile


ROOT = Path(__file__).resolve().parents[2]
STEM = "pr1-project-setup-zaragozi"
RETAINED = ROOT / "assets/projectes/vila-seca/pr1-aula"
EXPECTED = {
    f"{STEM}.gpkg": "88075560914a0da195dab9540325a7390f49d6b6cdf237c72639e3271c0f7ad9",
    f"{STEM}.qgz": "7147be541f7da8f487ebb1e1d3ef3b9f1602f01a109f7c21e7468c161d4cc050",
}
LAYERS = ("vilaseca_icgc_15000", "vilaseca_cnig")
QGIS_APP = None


def checked_bytes(path):
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED[path.name]:
        raise ValueError(f"Input changed; review a new classroom revision: {path}")
    return data


def project_xml(data):
    if isinstance(data, str):
        data = bytes.fromhex(data)
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        names = [name for name in archive.namelist() if name.endswith(".qgs")]
        if len(names) != 1:
            raise ValueError("Expected exactly one QGS document")
        return ET.fromstring(archive.read(names[0]))


def project_summary(xml):
    return {
        "qgis_version": xml.get("version"),
        "saved_at": xml.get("saveDateTime"),
        "crs": xml.findtext("projectCrs/spatialrefsys/authid"),
        "absolute_paths": xml.findtext("properties/Paths/Absolute"),
        "layers": [
            {
                "name": layer.findtext("layername"),
                "source": layer.findtext("datasource"),
                "provider": layer.findtext("provider"),
                "crs": layer.findtext("srs/spatialrefsys/authid"),
            }
            for layer in xml.findall("projectlayers/maplayer")
        ],
        "layouts": [layout.get("name") for layout in xml.findall("Layouts/Layout")],
    }


def inspect_archives(root):
    inputs = {name: checked_bytes(root / name) for name in EXPECTED}
    gpkg = root / f"{STEM}.gpkg"
    with sqlite3.connect(gpkg.resolve().as_uri() + "?mode=ro&immutable=1", uri=True) as db:
        db.row_factory = sqlite3.Row
        integrity = [row[0] for row in db.execute("PRAGMA integrity_check")]
        if integrity != ["ok"] or db.execute("PRAGMA foreign_key_check").fetchall():
            raise ValueError("GeoPackage integrity check failed")
        projects = db.execute("SELECT name, content FROM qgis_projects ORDER BY name").fetchall()
        if [row["name"] for row in projects] != ["pr1"]:
            raise ValueError("Expected exactly one embedded project, pr1")
        layers = {}
        for name in LAYERS:
            fields = [dict(row) for row in db.execute(f'PRAGMA table_info("{name}")')]
            records = [
                {key: value for key, value in dict(row).items() if key != "geom"}
                for row in db.execute(f'SELECT * FROM "{name}"')
            ]
            if len(records) != 1:
                raise ValueError(f"Expected one municipality in {name}")
            layers[name] = {"fields": fields, "records": records}
        embedded = project_summary(project_xml(projects[0]["content"]))
        external = project_summary(project_xml(inputs[f"{STEM}.qgz"]))
        return {
            "input_sha256": EXPECTED,
            "integrity": integrity,
            "geometry_columns": [dict(row) for row in db.execute("SELECT * FROM gpkg_geometry_columns")],
            "contents": [dict(row) for row in db.execute("SELECT * FROM gpkg_contents")],
            "layers": layers,
            "embedded": embedded,
            "external": external,
            "matching_layer_definitions": embedded["layers"] == external["layers"],
            "matching_layout_names": embedded["layouts"] == external["layouts"],
        }


def inspect_qgis(root):
    from qgis.core import QgsApplication, QgsProject, QgsVectorLayer, Qgis

    global QGIS_APP
    QGIS_APP = QgsApplication([], False)
    QGIS_APP.initQgis()
    gpkg = root / f"{STEM}.gpkg"
    geometries = []
    layers = []
    for name in LAYERS:
        layer = QgsVectorLayer(f"{gpkg}|layername={name}", name, "ogr")
        features = list(layer.getFeatures())
        if not layer.isValid() or len(features) != 1 or layer.crs().authid() != "EPSG:25831":
            raise ValueError(f"Invalid municipal layer: {name}")
        geometry = features[0].geometry()
        if geometry.isEmpty() or not geometry.isGeosValid():
            raise ValueError(f"Invalid municipal geometry: {name}")
        geometries.append(geometry)
        layers.append({"name": name, "count": 1, "crs": layer.crs().authid(),
                       "valid_geometry": True, "planar_area_m2": geometry.area()})
    projects = []
    for uri in (str(root / f"{STEM}.qgz"), f"geopackage:{gpkg}?projectName=pr1"):
        project = QgsProject()
        if not project.read(uri):
            raise ValueError(f"QGIS could not read {uri}")
        local_layers = []
        remote_layers = []
        for layer in project.mapLayers().values():
            source = layer.source()
            if layer.providerType() == "ogr" and "|layername=" in source and "https://" not in source:
                if not layer.isValid() or Path(source.split("|", 1)[0]).resolve() != gpkg.resolve():
                    raise ValueError(f"Local dependency does not resolve in the test directory: {source}")
                local_layers.append({"name": layer.name(), "source": source, "count": layer.featureCount()})
            else:
                remote_layers.append({"name": layer.name(), "source": source,
                                      "provider": layer.providerType(), "available_in_probe": layer.isValid()})
        if len(local_layers) != 2 or project.crs().authid() != "EPSG:25831":
            raise ValueError("Unexpected project contents")
        projects.append({"uri": uri, "relative_paths": project.filePathStorage() == Qgis.FilePathType.Relative,
                         "local_layers": local_layers, "remote_layers": remote_layers,
                         "layouts": [layout.name() for layout in project.layoutManager().layouts()]})
        project.clear()
    return {"runtime": Qgis.QGIS_VERSION, "layers": layers,
            "symmetric_difference_m2": geometries[0].symDifference(geometries[1]).area(),
            "projects": projects,
            "measurement": "Planar GEOS geometry in EPSG:25831; not an ellipsoidal $area measurement.",
            "network": "Use --network=none: remote unavailability then describes the test, not a server failure."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-root", type=Path, default=RETAINED)
    parser.add_argument("--retain", action="store_true", help="Retain exact classroom inputs from sandbox, without overwrite.")
    parser.add_argument("--qgis", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    if args.retain:
        contents = {name: checked_bytes(ROOT / "sandbox" / name) for name in EXPECTED}
        RETAINED.mkdir(parents=True, exist_ok=True)
        for name, data in contents.items():
            destination = RETAINED / name
            if destination.exists():
                checked_bytes(destination)
            else:
                with destination.open("xb") as handle:
                    handle.write(data)
    root = args.input_root.resolve()
    report = inspect_archives(root)
    if args.qgis:
        report["qgis"] = inspect_qgis(root)
    for name in EXPECTED:
        checked_bytes(root / name)
    report["inputs_unchanged"] = True
    output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.report:
        path = args.report.resolve()
        if not path.is_relative_to(ROOT / "tmp"):
            raise ValueError("Generated reports must be inside this repository's tmp directory")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(output, encoding="utf-8")
        print(json.dumps({"report": str(path), "inputs_unchanged": True,
                          "matching_layer_definitions": report["matching_layer_definitions"]}))
    else:
        print(output)


if __name__ == "__main__":
    main()
