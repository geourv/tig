#!/usr/bin/env python3
"""Prepare, verify and retain the concrete Vila-seca beginner GUI exercise.

Run in the pinned QGIS image. The original classroom files are read-only inputs.
The GUI actor, rather than this preparer, exports the selected municipality and
saves the two named projects through QGIS's native dialogs.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
import secrets

from qgis.core import (
    Qgis, QgsApplication, QgsFeatureRequest, QgsProject, QgsRectangle,
    QgsVectorFileWriter, QgsVectorLayer,
)

ROOT = Path(__file__).resolve().parents[2]
IMAGE = "qgis/qgis@sha256:e016b5296b99f0b07760b883888bc4ba615c0099feae9432374b4c83e8e073cc"
SOURCE = ROOT / "tmp/reference-exercises/sources/divisions-administratives-v2r2-municipis-5000-20260120.fgb"
SOURCE_SHA = "069f755f253f7af969e80403f6e81fa2cadefbd4c40ffd2f825f30e167bf2b2d"
STEM = "pr1-project-setup-exemple"
SHOTS = (
    "wms-overview", "selected-municipality", "export-menu", "export-dialog",
    "wms-result", "connect-dialog", "save-project-menu", "save-project-dialog",
    "refresh-connection", "projects-in-browser",
)
APP = None


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def prepare(stage):
    require(not stage.exists(), f"Use a new run directory: {stage}")
    require(digest(SOURCE) == SOURCE_SHA, "The fixed ICGC input has changed")
    source = QgsVectorLayer(str(SOURCE), "Municipis ICGC", "ogr")
    require(source.isValid() and source.featureCount() == 947, "Unexpected ICGC source")
    require(source.crs().authid() == "EPSG:25831", "Unexpected source CRS")
    selected = list(source.getFeatures(QgsFeatureRequest().setFilterExpression('"CODIMUNI" = \'431711\'')))
    require(len(selected) == 1 and selected[0]["NOMMUNI"] == "Vila-seca", "Municipality not identified")
    classroom = QgsVectorLayer(
        str(ROOT / "assets/projectes/vila-seca/pr1-aula/pr1-project-setup-zaragozi.gpkg")
        + "|layername=vilaseca_icgc_15000", "Classroom", "ogr")
    require(classroom.isValid(), "Missing retained classroom source")
    require(next(classroom.getFeatures()).geometry().isGeosEqual(selected[0].geometry()),
            "The classroom and fixed ICGC municipality differ")
    extent = QgsRectangle(selected[0].geometry().boundingBox())
    extent.scale(1.7)
    neighbours = list(source.getFeatures(QgsFeatureRequest().setFilterRect(extent)))
    require(len(neighbours) > 1, "The demonstration needs other municipalities")
    source.selectByIds([feature.id() for feature in neighbours])
    (stage / "data/raw").mkdir(parents=True)
    (stage / "sandbox").mkdir()
    (stage / "captures").mkdir()
    (stage / "runtime-home").mkdir()
    (stage / "runtime-home/auth").mkdir()
    (stage / "runtime-home/globalsettings.ini").write_text("[auth]\nuse_password_helper=false\n[locale]\noverrideFlag=true\nuserLocale=ca_ES\n")
    password_file = stage / "runtime-home/auth/master-password.txt"
    password_file.write_text(secrets.token_urlsafe(32) + "\n")
    password_file.chmod(0o600)
    destination = stage / "data/raw/municipis_entorn.gpkg"
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "GPKG"
    options.layerName = "municipis_entorn"
    options.onlySelectedFeatures = True
    result = QgsVectorFileWriter.writeAsVectorFormatV3(
        source, str(destination), QgsProject.instance().transformContext(), options)
    require(result[0] == QgsVectorFileWriter.NoError, str(result))
    provenance = {
        "source": SOURCE.name,
        "source_url": "https://datacloud.icgc.cat/datacloud/divisions-administratives/fgb_unzip_EPSG25831/" + SOURCE.name,
        "source_sha256": SOURCE_SHA, "source_count": 947,
        "licence": "ICGC, CC BY 4.0", "runtime_image": IMAGE,
        "subset_operation": "Municipalities whose bounding boxes intersect the Vila-seca extent enlarged by 1.7",
        "subset_count": len(neighbours),
        "subset_names": sorted(feature["NOMMUNI"] for feature in neighbours),
        "subset_sha256": digest(destination), "subset_crs": "EPSG:25831",
        "selection_expression": '"CODIMUNI" = \'431711\'',
        "municipality_geometry_sha256": hashlib.sha256(bytes(selected[0].geometry().asWkb())).hexdigest(),
        "wms_url": "https://geoserveis.icgc.cat/servei/catalunya/orto-territorial/wms",
        "wms_layer": "ortofoto_25cm_color_2025",
        "classroom_geometry_equal": True,
        "prepared_by": "PyQGIS; export and project saves are executed later in the native GUI",
    }
    (stage / "provenance.json").write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"stage": str(stage), "municipalities": len(neighbours), "names": provenance["subset_names"]}, ensure_ascii=False))


def verify(stage, report_path=None):
    provenance = json.loads((stage / "provenance.json").read_text())
    trace = json.loads((stage / "gui-evidence.json").read_text())
    require(trace.get("complete") is True, "The GUI sequence did not finish")
    require(set(trace["captures"]) == set(SHOTS), "The GUI sequence is missing screenshots")
    require(digest(stage / "data/raw/municipis_entorn.gpkg") == provenance["subset_sha256"], "Input subset changed")
    gpkg = stage / "sandbox" / f"{STEM}.gpkg"
    external = stage / "sandbox" / f"{STEM}.qgz"
    layer = QgsVectorLayer(f"{gpkg}|layername=municipi_vilaseca", "Output", "ogr")
    require(layer.isValid() and layer.featureCount() == 1, "Export did not retain exactly one municipality")
    feature = next(layer.getFeatures())
    require(feature["CODIMUNI"] == "431711" and feature["NOMMUNI"] == "Vila-seca", "Wrong municipality")
    require(layer.crs().authid() == "EPSG:25831" and feature.geometry().isGeosValid(), "Invalid exported geometry or CRS")
    geometry_sha = hashlib.sha256(bytes(feature.geometry().asWkb())).hexdigest()
    require(geometry_sha == provenance["municipality_geometry_sha256"], "Export changed the municipality geometry")
    with sqlite3.connect(gpkg.resolve().as_uri() + "?mode=ro", uri=True) as db:
        require(db.execute("PRAGMA integrity_check").fetchone() == ("ok",), "SQLite integrity failed")
        names = [row[0] for row in db.execute("SELECT name FROM qgis_projects ORDER BY name")]
        require(names == ["comparacio", "pr1"], f"Unexpected embedded projects: {names}")
    projects = []
    for name, uri in (("external", str(external)), ("pr1", f"geopackage:{gpkg}?projectName=pr1"),
                      ("comparacio", f"geopackage:{gpkg}?projectName=comparacio")):
        project = QgsProject()
        require(project.read(uri), f"Cannot reopen {name}")
        require(project.crs().authid() == "EPSG:25831", f"Wrong project CRS: {name}")
        local = [item for item in project.mapLayers().values() if item.providerType() == "ogr"]
        remote = [item for item in project.mapLayers().values() if item.providerType() == "wms"]
        require(len(local) == 1 and local[0].isValid(), f"Local layer does not resolve in {name}")
        require(Path(local[0].source().split("|", 1)[0]).resolve() == gpkg.resolve(), "External local dependency")
        require(len(remote) == 1 and provenance["wms_layer"] in remote[0].source(), "WMS definition lost")
        require(project.filePathStorage() == Qgis.FilePathType.Relative, "Absolute project storage")
        projects.append({"name": name, "local_count": local[0].featureCount(),
                         "local_source": local[0].source(), "wms": remote[0].source()})
        project.clear()
    report = {"ok": True, "qgis": Qgis.QGIS_VERSION, "image": IMAGE, "geometry_sha256": geometry_sha,
              "municipality_count": 1, "embedded_projects": names, "reopened": projects,
              "captures": {key: digest(stage / "captures" / f"qgis-pr1-{key}.png") for key in SHOTS},
              "gui_export_verified": True, "gui_project_saves_verified": True,
              "gui_steps": trace["steps"], "external_project_save": trace["external_project_save"]}
    (report_path or stage / "validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report


def publish(stage):
    verify(stage)
    target = ROOT / "assets/projectes/vila-seca/pr1-guia"
    target.mkdir(parents=True, exist_ok=True)
    for source in (stage / "data/raw/municipis_entorn.gpkg", stage / "sandbox" / f"{STEM}.gpkg",
                   stage / "sandbox" / f"{STEM}.qgz", stage / "provenance.json", stage / "validation.json"):
        require(not (target / source.name).exists(), "Retained guide inputs already exist; review replacement explicitly")
    for source in (stage / "data/raw/municipis_entorn.gpkg", stage / "sandbox" / f"{STEM}.gpkg",
                   stage / "sandbox" / f"{STEM}.qgz", stage / "provenance.json", stage / "validation.json"):
        shutil.copyfile(source, target / source.name)
    for shot in SHOTS:
        for suffix in (".png", ".manifest.yml"):
            name = f"qgis-pr1-{shot}{suffix}"
            destination = ROOT / "assets/img/qgis" / name
            require(not destination.exists(), f"Capture already exists: {destination}")
            shutil.copyfile(stage / "captures" / name, destination)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "verify", "publish"))
    parser.add_argument("--stage", type=Path, required=True)
    parser.add_argument("--report", type=Path, help="Separate report path when the verified stage is mounted read-only")
    args = parser.parse_args()
    global APP
    APP = QgsApplication([], False)
    APP.initQgis()
    if args.action == "verify":
        verify(args.stage.resolve(), args.report)
    else:
        {"prepare": prepare, "publish": publish}[args.action](args.stage.resolve())


if __name__ == "__main__":
    main()
