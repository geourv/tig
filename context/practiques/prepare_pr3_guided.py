#!/usr/bin/env python3
"""Actual QGIS selections and expression controls for the chapter 05 case.

download: host Python with Playwright and PyYAML; use the official web workflow.
prepare/finalize/check/publish: Python inside the pinned QGIS image, without network.
"""
import argparse
import base64
from collections import Counter
from contextlib import closing
import hashlib
import json
import os
from pathlib import Path
import secrets
import shutil
import sqlite3
import subprocess
import sys
import zipfile
import zlib
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor

import yaml

ROOT = Path(__file__).resolve().parents[2]
CATALOGUE = ROOT / "context/practiques/pr3-sources.yml"
STEM = "pr3-consultes-exemple"
ROAD_FILTER = '"clased" IN (\'Autopista libre / autovía\', \'Autopista de peaje\')'
SHOTS = ("manual-selection", "layer-filter-menu", "layer-filter-dialog", "table-filter",
         "table-visible-filter", "table-expression-filter", "selection-tools", "selection-expression-menu",
         "selection-expression-dialog", "portals-filter", "spatial-selection", "portals-selected",
         "selected-export-menu", "portals-export-dialog", "blocks-spatial-selection", "blocks-selected",
         "blocks-export-dialog", "exported-selections", "roads-filter", "roads-spatial-selection",
         "roads-selected", "roads-export-dialog", "roads-result", "field-calculator", "field-update",
         "aggregate-help", "label-expression")
APP = None
EXPORT_PROOFS = {}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1048576), b""):
            digest.update(block)
    return digest.hexdigest()


def catalogue():
    return yaml.safe_load(CATALOGUE.read_text())


def json_value(value):
    from qgis.PyQt.QtCore import QDate, QDateTime, QTime, Qt, QVariant
    if isinstance(value, QVariant):
        return None if value.isNull() or not value.isValid() else value.value()
    if isinstance(value, QDateTime):
        return value.toUTC().toString(Qt.ISODateWithMs) if value.isValid() else None
    if isinstance(value, (QDate, QTime)):
        return value.toString(Qt.ISODate) if value.isValid() else None
    raise TypeError(f"Unexpected result type: {type(value).__name__}")


def download():
    from playwright.sync_api import sync_playwright
    config = catalogue()
    cache = ROOT / config["cache"]
    cache.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path="/usr/bin/google-chrome", headless=True)
        context = browser.new_context(accept_downloads=True)
        for item in config["sources"].values():
            path = cache / item["archive"]
            if path.exists():
                require(sha(path) == item["sha256"], f"Input changed: {path}")
                continue
            page = context.new_page()
            page.goto(item["detail_url"], wait_until="networkidle")
            with page.expect_download(timeout=120000) as event:
                page.locator('[title="Descargar fichero"]').click()
            artifact = event.value
            pending = path.with_suffix(".pending")
            artifact.save_as(pending)
            require(pending.stat().st_size <= item["max_bytes"], "Unexpected download size")
            require(zipfile.is_zipfile(pending) and sha(pending) == item["sha256"], "Downloaded bytes do not match the reviewed edition")
            with zipfile.ZipFile(pending) as archive:
                require(archive.testzip() is None, "ZIP CRC failed")
            pending.rename(path)
            page.close()
        browser.close()


def inputs():
    config = catalogue()
    cache = ROOT / config["cache"]
    # OGR may update GeoPackage metadata even when no features are edited.
    # Keep the earlier exploratory extraction and prepare an exact read-only one.
    directory = ROOT / "tmp/pr3-guided/inputs-exact"
    for key, item in config["sources"].items():
        path = cache / item["archive"]
        require(sha(path) == item["sha256"], f"Input changed: {path}")
        with zipfile.ZipFile(path) as archive:
            for entry in archive.infolist():
                relative = Path(entry.filename)
                require(not relative.is_absolute() and ".." not in relative.parts, "Invalid archive member")
                target = directory / key / relative
                if entry.is_dir():
                    target.mkdir(parents=True, exist_ok=True)
                elif target.exists():
                    require(target.stat().st_size == entry.file_size, f"Extracted input changed: {target}")
                    crc = 0
                    with target.open("rb") as handle:
                        for block in iter(lambda: handle.read(1048576), b""):
                            crc = zlib.crc32(block, crc)
                    require(crc == entry.CRC, f"Extracted input CRC differs: {target}")
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with archive.open(entry) as source, target.open("xb") as output:
                        shutil.copyfileobj(source, output)
                if target.is_file():
                    target.chmod(0o444)
    return directory


def initialize():
    from qgis.core import QgsApplication
    global APP
    APP = QgsApplication([], False)
    APP.initQgis()
    sys.path.insert(0, str(Path(QgsApplication.pkgDataPath()) / "python/plugins"))
    from processing.core.Processing import Processing
    Processing.initialize()


def load(path, name, table=None):
    from qgis.core import QgsVectorLayer
    layer = QgsVectorLayer(str(path) + (f"|layername={table}" if table else ""), name, "ogr")
    require(layer.isValid(), f"Invalid layer: {path}, {table}")
    return layer


def effective_count(layer):
    from qgis.core import QgsFeatureRequest
    request = QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry).setSubsetOfAttributes([])
    return sum(1 for _ in layer.getFeatures(request))


def write_layer(layer, gpkg, name, selected=False):
    from qgis.core import Qgis, QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsProject, QgsVectorFileWriter
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "GPKG"
    options.layerName = name
    options.fileEncoding = "UTF-8"
    options.onlySelectedFeatures = selected
    options.actionOnExistingFile = (QgsVectorFileWriter.CreateOrOverwriteLayer if gpkg.exists()
                                   else QgsVectorFileWriter.CreateOrOverwriteFile)
    options.ct = QgsCoordinateTransform(layer.crs(), QgsCoordinateReferenceSystem("EPSG:25831"), QgsProject.instance())
    result = QgsVectorFileWriter.writeAsVectorFormatV3(layer, str(gpkg), QgsProject.instance().transformContext(), options)
    require(result[0] == QgsVectorFileWriter.NoError, str(result))
    output = load(gpkg, name, name)
    fields = layer.fields().names()
    original = content_signature(layer, fields, selected=selected, reproject=True)
    require(content_signature(output, fields) == original, f"Export changed source attributes or complete geometry: {name}")
    EXPORT_PROOFS[name] = {"fields": fields, "sha256": original, "count": output.featureCount(),
                          "source_crs": layer.crs().authid(), "output_crs": output.crs().authid()}
    return output


def content_signature(layer, fields, selected=False, reproject=False):
    from qgis.core import QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsGeometry, QgsProject
    transform = QgsCoordinateTransform(layer.crs(), QgsCoordinateReferenceSystem("EPSG:25831"), QgsProject.instance())
    records = []
    for feature in (layer.getSelectedFeatures() if selected else layer.getFeatures()):
        geometry = QgsGeometry(feature.geometry())
        if reproject:
            require(geometry.transform(transform) == 0, "Export control transform failed")
        geometry.convertToMultiType()
        geometry.normalize()
        row = [feature[field] for field in fields]
        row.append(bytes(geometry.asWkb()).hex())
        records.append(hashlib.sha256(json.dumps(row, ensure_ascii=False, default=json_value).encode()).hexdigest())
    return hashlib.sha256("\n".join(sorted(records)).encode()).hexdigest()


def expression_controls(layer, roads=False):
    from qgis.core import Qgis, QgsDistanceArea, QgsExpression, QgsExpressionContext, QgsExpressionContextUtils, QgsProject
    project = QgsProject.instance()
    calculator = QgsDistanceArea()
    calculator.setSourceCrs(layer.crs(), project.transformContext())
    require(calculator.setEllipsoid("GRS80") and calculator.willUseEllipsoid(), "GRS80 measurement is not active")
    context = QgsExpressionContext()
    context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layer))
    definitions = {
        "area_plana_m2": "area($geometry)",
        "area_ellipsoide_m2": "$area",
        "area_km2": "$area / 1000000",
        "perimetre_pla_m": "perimeter($geometry)",
        "perimetre_km": "$perimeter / 1000",
        "classe_area": "CASE WHEN $geometry IS NULL OR is_empty($geometry) THEN NULL WHEN $area / 1000000 < 10 THEN 'petit' WHEN $area / 1000000 < 50 THEN 'mitja' ELSE 'gran' END",
        "nom_etiqueta": "coalesce(nullif(trim(\"NAMEUNIT\"), ''), 'Sense nom')",
    }
    if roads:
        definitions = {"long_plana_m": "length($geometry)", "long_ellipsoide_m": "$length", "long_km": "$length / 1000"}
    compiled = {}
    for name, text in definitions.items():
        expression = QgsExpression(text)
        expression.setGeomCalculator(calculator)
        expression.setAreaUnits(Qgis.AreaUnit.SquareMeters)
        expression.setDistanceUnits(Qgis.DistanceUnit.Meters)
        require(expression.prepare(context), expression.parserErrorString())
        compiled[name] = expression
    rows = []
    for feature in layer.getFeatures():
        context.setFeature(feature)
        row = ({"fid": feature.id(), "id_tramo": feature["id_tramo"]} if roads
               else {"NATCODE": feature["NATCODE"], "NAMEUNIT": feature["NAMEUNIT"]})
        for name, expression in compiled.items():
            row[name] = expression.evaluate(context)
            require(not expression.hasEvalError(), expression.evalErrorString())
        if roads:
            require(abs(row["long_plana_m"] - feature.geometry().length()) < 0.0001, "Planar length mismatch")
            require(abs(row["long_ellipsoide_m"] - calculator.measureLength(feature.geometry())) < 0.0001, "Ellipsoidal length mismatch")
        else:
            require(abs(row["area_plana_m2"] - feature.geometry().area()) < 0.0001, "Planar area mismatch")
            require(abs(row["area_ellipsoide_m2"] - calculator.measureArea(feature.geometry())) < 0.0001, "Ellipsoidal area mismatch")
            require(abs(row["perimetre_km"] * 1000 - calculator.measurePerimeter(feature.geometry())) < 0.0001, "Perimeter mismatch")
        rows.append(row)
    return {"crs": layer.crs().authid(), "ellipsoid": "GRS80", "area_unit": "m2", "distance_unit": "m",
             "expressions": definitions, "rows": rows}


def store_measures(layer, controls, key, omit=()):
    from qgis.PyQt.QtCore import QMetaType
    from qgis.core import QgsField
    names = [name for name in controls["expressions"] if name not in omit]
    require(layer.startEditing(), "Cannot store calculated attributes")
    for name in names:
        is_text = name in {"classe_area", "nom_etiqueta"}
        kind = QMetaType.Type.QString if is_text else QMetaType.Type.Double
        require(layer.addAttribute(QgsField(name, kind, len=100 if is_text else 20, prec=0 if is_text else 8)), f"Cannot create {name}")
    layer.updateFields()
    rows = {row[key]: row for row in controls["rows"]}
    for feature in layer.getFeatures():
        row = rows[feature.id() if key == "fid" else feature[key]]
        for name in names:
            require(layer.changeAttributeValue(feature.id(), layer.fields().indexFromName(name), row[name]), f"Cannot set {name}")
    require(layer.commitChanges(), str(layer.commitErrors()))


def prepare(stage):
    from qgis.core import (
        Qgis, QgsApplication, QgsCoordinateReferenceSystem, QgsFeatureRequest,
        QgsField, QgsProcessingContext, QgsProcessingFeedback, QgsProject, QgsWkbTypes,
    )
    from qgis.PyQt.QtCore import QMetaType
    import processing
    require(not stage.exists(), "Use a new staging directory")
    source = inputs()
    (stage / "sandbox").mkdir(parents=True)
    (stage / "captures").mkdir()
    (stage / "controls").mkdir()
    (stage / "runtime-home/auth").mkdir(parents=True)
    (stage / "runtime-home/globalsettings.ini").write_text("[auth]\nuse_password_helper=false\n[locale]\noverrideFlag=true\nuserLocale=ca_ES\n")
    password = stage / "runtime-home/auth/master-password.txt"
    password.write_text(secrets.token_urlsafe(32) + "\n")
    password.chmod(0o600)
    gpkg = stage / "sandbox" / f"{STEM}.gpkg"
    expected_gpkg = stage / "controls/expected-exports.gpkg"
    project = QgsProject.instance()
    project.setCrs(QgsCoordinateReferenceSystem("EPSG:25831"))
    project.setEllipsoid("GRS80")
    project.setAreaUnits(Qgis.AreaUnit.SquareMeters)
    project.setDistanceUnits(Qgis.DistanceUnit.Meters)
    context = QgsProcessingContext()
    context.setProject(project)
    feedback = QgsProcessingFeedback()
    provenance = catalogue()
    controls = {"qgis": Qgis.QGIS_VERSION, "counts": {}, "criteria": {}, "algorithms": {}}
    paths = {}
    for level in ("municipales", "provinciales", "autonomicas"):
        stem = f"recintos_{level}_inspire_peninbal_etrs89"
        paths[level] = str(source / "limits/SHP_ETRS89" / stem / (stem + ".shp"))
    paths["cartociudad"] = str(source / "cartociudad/CARTOCIUDAD_CALLEJERO_TARRAGONA/tarragona.gpkg")
    paths["transport"] = str(source / "transport/red_viaria.gpkg")
    boundary_path = ROOT / "assets/projectes/vila-seca/pr1-guia/pr1-project-setup-exemple.gpkg"
    boundary = load(boundary_path, "Vila-seca ICGC", "municipi_vilaseca")
    write_layer(boundary, gpkg, "municipi_vilaseca")
    boundary = write_layer(boundary, gpkg, "municipi_treball")
    require(boundary.startEditing(), "Cannot prepare the municipal key")
    require(boundary.addAttribute(QgsField("codi_muni", QMetaType.Type.QString, len=5)), "Cannot add municipal key")
    boundary.updateFields()
    for feature in boundary.getFeatures():
        require(feature["CODIMUNI"] == "431711", "Unexpected classroom municipality")
        boundary.changeAttributeValue(feature.id(), boundary.fields().indexFromName("codi_muni"), "43171")
    require(boundary.commitChanges(), str(boundary.commitErrors()))
    controls["inherited_boundary"] = "ICGC municipality retained unchanged as municipi_treball; not used for this CNIG lesson's spatial selections"
    municipality = load(paths["municipales"], "Municipis CNIG")
    controls["counts"]["municipis_font"] = municipality.featureCount()
    criterion = '"CODNUT3"=\'ES514\''
    require(municipality.setSubsetString(criterion), "Province filter rejected")
    controls["criteria"]["municipis_tarragona"] = criterion
    controls["counts"]["municipis_tarragona"] = municipality.featureCount()
    require(municipality.featureCount() == 184, "Tarragona municipality count changed")
    municipality.selectByExpression('"NATCODE"=\'34094343171\'')
    require(municipality.selectedFeatureCount() == 1, "Vila-seca selection failed")
    boundary = write_layer(municipality, gpkg, "municipi_consulta", selected=True)
    controls["boundary_source"] = "CNIG municipal source, NATCODE=34094343171, exported complete as municipi_consulta in EPSG:25831"
    municipality.invertSelection()
    require(municipality.selectedFeatureCount() == 183, "Inversion failed")
    municipality.removeSelection()
    municipalities = write_layer(municipality, gpkg, "municipis_tarragona")
    controls["selection_counts"] = {"vila_seca": 1, "inverted_within_filtered_layer": 183, "cleared": 0}
    for level, output_name, condition in (
        ("provinciales", "provincies_catalunya", '"NATCODE" LIKE \'3409%\''),
        ("autonomicas", "ccaa_context", '"CODNUT2" IN (\'ES24\',\'ES51\',\'ES52\')'),
    ):
        layer = load(paths[level], output_name)
        controls.setdefault("administrative_schema", {})[level] = [
            {name: feature[name] for name in ("NATCODE", "NAMEUNIT", "CODNUT1", "CODNUT2", "CODNUT3")}
            for feature in layer.getFeatures()]
        layer.selectByExpression(condition)
        expected = 4 if level == "provinciales" else 3
        require(layer.selectedFeatureCount() == expected, f"Unexpected {output_name} selection")
        result = write_layer(layer, gpkg, output_name, selected=True)
        controls["criteria"][output_name] = condition
        controls["counts"][output_name] = result.featureCount()
    algorithm = QgsApplication.processingRegistry().algorithmById("native:selectbylocation")
    require(algorithm is not None, "Missing native:selectbylocation")
    controls["algorithms"]["native:selectbylocation"] = {
        "predicates": algorithm.parameterDefinition("PREDICATE").options(),
        "methods": algorithm.parameterDefinition("METHOD").options(),
    }
    predicate_options = controls["algorithms"]["native:selectbylocation"]["predicates"]
    intersects = next(i for i, text in enumerate(predicate_options) if text.lower() == "intersect")
    within = next(i for i, text in enumerate(predicate_options) if text.lower() == "are within")

    def select_spatial(layer, predicate):
        processing.run("native:selectbylocation", {"INPUT": layer, "PREDICATE": [predicate],
                       "INTERSECT": boundary, "METHOD": 0}, context=context, feedback=feedback)
        return layer.selectedFeatureCount()

    portals = load(paths["cartociudad"], "Portals CartoCiudad", "portalpk_publi")
    controls["counts"]["portalpk_font"] = portals.featureCount()
    require(portals.setSubsetString('"tipo"=\'Portal\''), "Portal filter rejected")
    controls["criteria"]["portals"] = '"tipo"=\'Portal\''
    controls["reported_fast_counts"] = {"portals_after_filter": portals.featureCount()}
    controls["counts"]["portals_sense_pk"] = effective_count(portals)
    require(controls["counts"]["portals_sense_pk"] == 364921, "Portal domain/count changed")
    controls["counts"]["portals_interseccio"] = select_spatial(portals, intersects)
    controls["counts"]["portals_dins"] = select_spatial(portals, within)
    select_spatial(portals, intersects)
    expected_portals = write_layer(portals, expected_gpkg, "portals_vilaseca", selected=True)
    blocks = load(paths["cartociudad"], "Illes CartoCiudad", "manzana")
    controls["counts"]["illes_font"] = blocks.featureCount()
    controls["counts"]["illes_dins"] = select_spatial(blocks, within)
    within_ids = set(blocks.selectedFeatureIds())
    controls["counts"]["illes_interseccio"] = select_spatial(blocks, intersects)
    controls["block_boundary_ids"] = sorted(set(blocks.selectedFeatureIds()) - within_ids)
    blocks.selectByIds(sorted(within_ids))
    controls["criteria"]["illes_exportades"] = "are within; predicate evaluated in the source EPSG:4258"
    expected_blocks = write_layer(blocks, expected_gpkg, "illes_vilaseca", selected=True)
    boundary_geometry = next(boundary.getFeatures()).geometry()
    require(all(f.geometry().within(boundary_geometry) for f in expected_blocks.getFeatures()), "An exported contained block extends outside the municipality")
    roads = load(paths["transport"], "Vials RT", "rt_tramo_vial")
    controls["counts"]["trams_font"] = roads.featureCount()
    controls["criteria"]["vies_principals"] = ROAD_FILTER
    require(roads.setSubsetString(ROAD_FILTER), "Road filter rejected")
    controls["reported_fast_counts"]["roads_after_filter"] = roads.featureCount()
    controls["counts"]["trams_principals_provincia"] = effective_count(roads)
    controls["counts"]["trams_principals_interseccio"] = select_spatial(roads, intersects)
    exported_roads = write_layer(roads, expected_gpkg, "transport_candidats_c06", selected=True)
    require(all(f.geometry().intersects(boundary_geometry) for f in exported_roads.getFeatures()), "An exported motorway no longer intersects the municipality")
    controls["motorways"] = {"rows": exported_roads.featureCount(),
        "unique_id_tramo": len({f["id_tramo"] for f in exported_roads.getFeatures()}),
        "names": dict(Counter(f["nombre"] for f in exported_roads.getFeatures())),
        "classes": dict(Counter(f["clased"] for f in exported_roads.getFeatures()))}
    controls["geometry_types"] = {layer.name(): QgsWkbTypes.displayString(layer.wkbType())
        for layer in (expected_portals, expected_blocks, exported_roads)}
    controls["native_export_tables"] = ["portals_vilaseca", "illes_vilaseca", "transport_candidats_c06"]
    controls["measurements"] = expression_controls(municipalities)
    controls["road_measurements"] = expression_controls(exported_roads, roads=True)
    store_measures(municipalities, controls["measurements"], "NATCODE", omit=("area_km2",))
    store_measures(exported_roads, controls["road_measurements"], "fid")
    controls["exports"] = EXPORT_PROOFS
    controls["area_classes"] = dict(sorted(Counter(row["classe_area"] for row in controls["measurements"]["rows"]).items()))
    controls["road_length_sum_km"] = sum(row["long_km"] for row in controls["road_measurements"]["rows"])
    total = sum(round(row["area_km2"], 6) for row in controls["measurements"]["rows"])
    controls["aggregates"] = {"layer": "municipis_tarragona", "count": 184,
        "area_sum_km2": total, "updated_expression": "round($area / 1000000, 6)",
        "expression": '\"area_km2\" / aggregate(@layer, \'sum\', \"area_km2\") * 100',
        "quota_area_pct": {row["NATCODE"]: round(row["area_km2"], 6) / total * 100 for row in controls["measurements"]["rows"]}}
    controls["input_paths"] = paths
    controls["project_crs"] = "EPSG:25831"
    controls["geometry_policy"] = "Whole selected features; export reprojection is explicit; no clipping, buffer or geometric overlay"
    controls["count_method"] = "Filtered GeoPackage counts are checked by feature iteration; this runtime can retain the original fast metadata count after setSubsetString"
    provenance["inherited_boundary"] = {"path": str(boundary_path.relative_to(ROOT)), "sha256": sha(boundary_path),
                              "table": "municipi_vilaseca", "CODIMUNI": "431711", "codi_muni": "43171",
                              "key_concordance": "Explicit mapping for Vila-seca, not a generic string truncation rule"}
    provenance["authoritative_sources"] = {str(path.relative_to(ROOT)): sha(path) for path in (
        CATALOGUE, Path(__file__).resolve(), ROOT / "context/practiques/capture_pr3_guided.py",
        ROOT / "context/practiques/pr3-captures.yml")}
    (stage / "provenance.json").write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + "\n")
    (stage / "controls.json").write_text(json.dumps(controls, ensure_ascii=False, indent=2, default=json_value) + "\n")
    print(json.dumps({"stage": str(stage), "counts": controls["counts"], "algorithms": controls["algorithms"],
                      "vila_seca": [row for row in controls["measurements"]["rows"] if row["NAMEUNIT"] == "Vila-seca"]}, ensure_ascii=False, indent=2))


def finalize(stage):
    """Close the SQLite transport file after the one-shot GUI process exits."""
    trace = json.loads((stage / "gui-evidence.json").read_text())
    require(trace.get("complete") is True, "Cannot finalize an incomplete GUI run")
    gpkg = stage / "sandbox" / f"{STEM}.gpkg"
    with closing(sqlite3.connect(gpkg, timeout=0)) as db:
        require(db.execute("PRAGMA wal_checkpoint(TRUNCATE)").fetchone()[0] == 0, "Database is still busy")
        require(db.execute("PRAGMA journal_mode=DELETE").fetchone()[0] == "delete", "Could not finalize the transport journal")
        require(db.execute("PRAGMA integrity_check").fetchone()[0] == "ok", "SQLite integrity failed")


def capture_bundle(stage, wheel):
    """Run this lesson and its isolated frames with the installed provider.

    The provider's bridge owns a one-shot QGIS process and exits after rendering.
    Each frame therefore replays the lesson prefix on its own seed copy. No
    provider code is copied, patched or imported past its normal entry point.
    """
    require(not stage.exists() and stage.is_relative_to(ROOT / "tmp/pr3-guided"), "Use a fresh confined capture directory")
    config = catalogue()
    require(wheel.is_file() and sha(wheel) == config["annotation_provider"]["sha256"], "Wrong installed annotation wheel")
    image = config["runtime_image"]
    user = f"{os.getuid()}:{os.getgid()}"
    mounts = ["--mount", f"type=bind,source={ROOT},target=/workspace,readonly"]
    base = ["docker", "run", "--rm", "--pull=never", "--user", user,
            "--label", "io.context.mcp-project=5fb70984e2683ec7", "--label", "io.context.role=tig-c05-native"]
    seed = stage / "seed"
    subprocess.run(base + ["--network=none", "-e", "HOME=/tmp", "-e", "QT_QPA_PLATFORM=offscreen", *mounts,
        "--mount", f"type=bind,source={ROOT}/tmp/pr3-guided,target=/workspace/tmp/pr3-guided",
        "--entrypoint", "/usr/bin/python3", image, "/workspace/context/practiques/prepare_pr3_guided.py",
        "prepare", "--stage", "/workspace/" + str(seed.relative_to(ROOT))], check=True)

    def gui(path, shot=""):
        shutil.copytree(seed, path)
        name = "tig-c05-" + hashlib.sha256(str(path).encode()).hexdigest()[:16]
        command = base + ["--name", name, "--network=bridge", *mounts,
            "--mount", f"type=bind,source={path},target=/home/docent/tig",
            "--mount", f"type=bind,source={wheel},target=/provider.whl,readonly",
            "-e", "HOME=/home/docent/tig/runtime-home", "-e", "QT_QPA_PLATFORM=xcb",
            "-e", "QT_SCALE_FACTOR=1", "-e", "QT_AUTO_SCREEN_SCALE_FACTOR=0", "-e", "QT_ENABLE_HIGHDPI_SCALING=0",
            "-e", "QGIS_AUTH_PASSWORD_FILE=/home/docent/tig/runtime-home/auth/master-password.txt",
            "-e", f"PR3_RENDER_SHOT={shot}", "-e", "PR3_ANNOTATION_WHEEL=/provider.whl",
            "--entrypoint", "/bin/bash", image, "-lc",
            "Xvfb :99 -screen 0 1280x1000x24 -dpi 96 -nolisten tcp & export DISPLAY=:99; sleep 1; "
            "exec qgis --nologo --noversioncheck --noplugins --lang ca_ES "
            "--globalsettingsfile /home/docent/tig/runtime-home/globalsettings.ini "
            "--authdbdirectory /home/docent/tig/runtime-home/auth "
            "--profiles-path /home/docent/tig/runtime-home/profiles --profile pr3 "
            "--code /workspace/context/practiques/capture_pr3_guided.py"]
        try:
            process = subprocess.run(command, capture_output=True, text=True, timeout=240)
        except subprocess.TimeoutExpired:
            subprocess.run(["docker", "rm", "-f", name], check=False, capture_output=True)
            raise
        (path / "runtime.log").write_text(process.stdout + process.stderr)
        require(process.returncode == 0, f"QGIS failed: {path}")
        trace = json.loads((path / "gui-evidence.json").read_text())
        require(not trace.get("error"), str(trace.get("error")))
        if shot:
            result = json.loads((path / "annotation-result.json").read_text())
            require(result.get("ok") is True and not result.get("warnings"), f"Annotation provider failed: {shot}: {result.get('warnings', result.get('error'))}")
            require(trace["frame_ready"]["id"] == shot, "Wrong prepared frame")
            print(json.dumps({"frame": shot, "ok": True}), flush=True)
        else:
            require(trace.get("complete") is True, "Incomplete lesson")
        return path

    main_stage = gui(stage / "main")
    finalize(main_stage)
    shutil.copytree(main_stage / "captures", main_stage / "raw-captures")
    # These two workers write disjoint scene copies. Assembly is serial.
    with ThreadPoolExecutor(max_workers=2) as pool:
        frames = list(pool.map(lambda shot: gui(stage / "frames" / shot, shot), SHOTS))
    evidence = {}
    for shot, frame in zip(SHOTS, frames):
        trace = json.loads((frame / "gui-evidence.json").read_text())
        evidence[shot] = trace["frame_ready"]
        evidence[shot]["files"] = {}
        for suffix in (".png", ".annotations.svg", ".manifest.yml"):
            source = frame / "captures" / f"qgis-c05-{shot}{suffix}"
            evidence[shot]["files"][source.name] = sha(source)
            shutil.copyfile(source, main_stage / "captures" / source.name)
    (main_stage / "frame-evidence.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"ok": True, "stage": str(main_stage), "frames": len(frames)}, ensure_ascii=False))


def check(stage, report_path=None):
    from qgis.core import Qgis, QgsCoordinateReferenceSystem, QgsProject
    provenance = json.loads((stage / "provenance.json").read_text())
    controls = json.loads((stage / "controls.json").read_text())
    trace = json.loads((stage / "gui-evidence.json").read_text())
    frames = json.loads((stage / "frame-evidence.json").read_text())
    require(trace.get("complete") is True and not trace.get("error"), "Incomplete native GUI run")
    require(set(trace["captures"]) == set(SHOTS), "Missing captures")
    for path, expected in provenance["authoritative_sources"].items():
        require(sha(ROOT / path) == expected, f"Source changed after capture: {path}")
    for test in trace["selection_tests"]:
        require(test["ids"] == test["expected_ids"], "Failed map gesture")
    for test in trace["table_selection_tests"]:
        require(test["actual"] == test["expected"], "Failed table gesture")
    native_exports = {item["table"]: item for item in trace.get("native_exports", [])}
    require(set(native_exports) == set(controls["native_export_tables"]), "The three selected subsets were not exported in the GUI")
    for name, proof in native_exports.items():
        require(proof["initially_absent"] and proof["only_selected"] and proof["count"] == controls["exports"][name]["count"], "Invalid native export evidence")
    gpkg = stage / "sandbox" / f"{STEM}.gpkg"
    external = gpkg.with_suffix(".qgz")
    initial_hashes = {gpkg.name: sha(gpkg), external.name: sha(external)}
    layers = {}
    for name, proof in controls["exports"].items():
        layer = load(gpkg, name, name)
        require(effective_count(layer) == proof["count"], f"Wrong output count: {name}")
        require(layer.crs().authid() == "EPSG:25831", f"Wrong output CRS: {name}")
        require(content_signature(layer, proof["fields"]) == proof["sha256"], f"Source fields or complete geometry changed: {name}")
        require(all(not f.geometry().isEmpty() and f.geometry().isGeosValid() for f in layer.getFeatures()), f"Invalid geometries in {name}")
        layers[name] = layer
    boundary = next(layers["municipi_treball"].getFeatures())
    require(boundary["CODIMUNI"] == "431711" and boundary["codi_muni"] == "43171", "Municipal key lost")
    require(all(f["tipo"] == "Portal" for f in layers["portals_vilaseca"].getFeatures()), "PK leaked into portal export")
    require(next(layers["municipi_consulta"].getFeatures())["NATCODE"] == "34094343171", "Wrong CNIG query municipality")
    reference = next(layers["municipi_consulta"].getFeatures()).geometry()
    require(all(f.geometry().within(reference) for f in layers["illes_vilaseca"].getFeatures()), "A retained block is outside the municipality")
    require(all(f.geometry().intersects(reference) for f in layers["transport_candidats_c06"].getFeatures()), "A retained motorway misses the municipality")
    project = QgsProject.instance()
    project.setCrs(QgsCoordinateReferenceSystem("EPSG:25831"))
    project.setEllipsoid("GRS80")
    project.setAreaUnits(Qgis.AreaUnit.SquareMeters)
    project.setDistanceUnits(Qgis.DistanceUnit.Meters)
    for table, key, roads in (("municipis_tarragona", "NATCODE", False), ("transport_candidats_c06", "fid", True)):
        calculated = expression_controls(layers[table], roads=roads)
        expected = {row[key]: row for row in calculated["rows"]}
        for feature in layers[table].getFeatures():
            row = expected[feature.id() if key == "fid" else feature[key]]
            for name in calculated["expressions"]:
                actual = feature[name]
                wanted = row[name]
                require(actual == wanted if isinstance(wanted, str) else abs(actual - wanted) < 0.00001, f"Persisted expression differs: {table}.{name}")
    for feature in layers["municipis_tarragona"].getFeatures():
        expected = controls["aggregates"]["quota_area_pct"][feature["NATCODE"]]
        require(abs(feature["quota_area_pct"] - expected) < 1e-7, "Persisted aggregate field differs")
    require(abs(sum(f["quota_area_pct"] for f in layers["municipis_tarragona"].getFeatures()) - 100) < 1e-7, "Aggregate shares do not sum to 100")
    with closing(sqlite3.connect(gpkg.resolve().as_uri() + "?mode=ro", uri=True)) as db:
        require(db.execute("PRAGMA integrity_check").fetchone() == ("ok",), "SQLite integrity failed")
        names = [r[0] for r in db.execute("SELECT name FROM qgis_projects ORDER BY name")]
        require(names == ["pr3"], "Unexpected projects in this demonstration package")
        for name, proof in controls["exports"].items():
            require(db.execute(f'SELECT count(*) FROM "{name}"').fetchone()[0] == proof["count"], "SQL/QGIS count mismatch")
    reopened = []
    for name, uri in (("external", str(external)), ("pr3", f"geopackage:{gpkg}?projectName=pr3")):
        candidate = QgsProject()
        require(candidate.read(uri), f"Cannot reopen {name}")
        require(candidate.crs().authid() == "EPSG:25831" and candidate.ellipsoid() == "GRS80", "Measurement settings lost")
        require(candidate.filePathStorage() == Qgis.FilePathType.Relative, "Absolute project paths")
        local = [item for item in candidate.mapLayers().values() if item.providerType() == "ogr"]
        require(len(local) == len(layers), "Not all accumulated layers are in the project")
        for item in local:
            require(item.isValid() and Path(item.source().split("|", 1)[0]).resolve() == gpkg.resolve(), "External local dependency")
        require(any(item.providerType() == "wms" and "ortofoto_25cm_color_2025" in item.source() for item in candidate.mapLayers().values()), "WMS definition lost")
        reopened.append({"project": name, "local_layers": len(local), "local_dependencies": [gpkg.name]})
        candidate.clear()
    captures = {}
    for shot in SHOTS:
        image = stage / "captures" / f"qgis-c05-{shot}.png"
        manifest = json.loads(image.with_suffix(".manifest.yml").read_text())
        require(manifest["ok"] and manifest["capture_id"] == shot and not manifest["warnings"], "Invalid annotated capture")
        require(manifest["probe"]["annotation_provider"] == provenance["annotation_provider"], "Wrong annotation provider")
        require(frames[shot]["sources"] == provenance["authoritative_sources"], "Frame sources differ")
        for name, expected in frames[shot]["files"].items():
            require(sha(stage / "captures" / name) == expected, "Frame artifact changed")
        svg = image.with_suffix(".annotations.svg")
        tree = ET.parse(svg)
        embedded = tree.find(".//{http://www.w3.org/2000/svg}image")
        uri = embedded.get("{http://www.w3.org/1999/xlink}href") or embedded.get("href")
        require(uri.startswith("data:image/png;base64,"), "Missing original native screenshot")
        require(base64.b64decode(uri.split(",", 1)[1]).startswith(b"\x89PNG\r\n\x1a\n"), "Invalid embedded screenshot")
        captures[shot] = {"png_sha256": sha(image), "svg_sha256": sha(svg), "manifest": manifest,
                          "frame": frames[shot]}
    retained_controls = {k: v for k, v in controls.items() if k != "input_paths"}
    require({gpkg.name: sha(gpkg), external.name: sha(external)} == initial_hashes,
            "Verification changed files: finalize again and mount the stage read-only")
    report = {"ok": True, "qgis": Qgis.QGIS_VERSION, "runtime_image": provenance["runtime_image"],
              "files": initial_hashes, "reopened": reopened,
              "evidence_hashes": {name: sha(stage / name) for name in ("provenance.json", "controls.json", "gui-evidence.json", "frame-evidence.json")},
              "controls": retained_controls, "captures": captures, "gui_steps": trace["steps"],
              "native_exports": trace["native_exports"],
              "map_gestures": trace["selection_tests"], "table_gestures": trace["table_selection_tests"],
              "local_resource_complete": True, "remote_resource": "The WMS still requires network access; its imagery is not embedded"}
    (report_path or stage / "validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, default=json_value) + "\n")
    print(json.dumps({"ok": True, "counts": controls["counts"], "area_classes": controls["area_classes"],
                      "road_length_sum_km": controls["road_length_sum_km"], "reopened": reopened}, ensure_ascii=False, indent=2))
    return report


def publish(stage, replace_reviewed=False):
    report = json.loads((stage / "validation.json").read_text())
    provenance = json.loads((stage / "provenance.json").read_text())
    require(report.get("ok") is True, "Missing successful read-only verification")
    for name, expected in report["files"].items():
        require(sha(stage / "sandbox" / name) == expected, "Output changed after verification")
    for name, expected in report["evidence_hashes"].items():
        require(sha(stage / name) == expected, "Evidence changed after verification")
    for path, expected in provenance["authoritative_sources"].items():
        require(sha(ROOT / path) == expected, "Source changed after verification")
    for shot, manifest in report["captures"].items():
        image = stage / "captures" / f"qgis-c05-{shot}.png"
        require(sha(image) == manifest["png_sha256"], "Capture changed after verification")
        require(sha(image.with_suffix(".annotations.svg")) == manifest["svg_sha256"], "Annotation SVG changed")
        require(json.loads(image.with_suffix(".manifest.yml").read_text()) == manifest["manifest"], "Capture manifest changed")
    target = ROOT / "assets/projectes/vila-seca/pr3-guia"
    items = [(stage / "sandbox" / f"{STEM}{suffix}", target / f"{STEM}{suffix}") for suffix in (".gpkg", ".qgz")]
    items += [(stage / name, target / name) for name in ("provenance.json", "validation.json")]
    items += [(stage / "captures" / f"qgis-c05-{shot}{suffix}", ROOT / "assets/img/qgis" / f"qgis-c05-{shot}{suffix}")
              for shot in SHOTS for suffix in (".png", ".annotations.svg", ".manifest.yml")]
    for source, destination in items:
        require(source.is_file() and (replace_reviewed or not destination.exists()), f"Missing source or retained output already exists: {destination}")
        require(not destination.is_symlink(), "Refusing a symlink destination")
    if replace_reviewed:
        archive = stage / "previous-retained"
        require(not archive.exists(), "Previous revision archive already exists")
        for _, destination in items:
            if destination.exists():
                backup = archive / destination.relative_to(ROOT)
                backup.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(destination, backup)
    target.mkdir(parents=True, exist_ok=True)
    for source, destination in items:
        shutil.copyfile(source, destination)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("download", "prepare", "capture", "finalize", "check", "publish"))
    parser.add_argument("--stage", type=Path)
    parser.add_argument("--report", type=Path, help="Separate report path for a read-only relocated stage")
    parser.add_argument("--annotation-wheel", type=Path)
    parser.add_argument("--replace-reviewed", action="store_true", help="Retain the previous local revision before the author-requested replacement")
    args = parser.parse_args()
    if args.action == "download":
        download()
    else:
        require(args.stage is not None, "--stage is required")
        if args.action in {"prepare", "check"}:
            initialize()
        if args.action == "capture":
            require(args.annotation_wheel is not None, "--annotation-wheel is required")
            capture_bundle(args.stage.resolve(), args.annotation_wheel.resolve())
        elif args.action == "publish":
            publish(args.stage.resolve(), args.replace_reviewed)
        elif args.action == "check":
            check(args.stage.resolve(), args.report)
        else:
            {"prepare": prepare, "finalize": finalize}[args.action](args.stage.resolve())


if __name__ == "__main__":
    main()
