"""TIG municipal teaching cases; calculation and cartography owned by the course.

The shared practice-v2 producer owns execution, native resource inspection,
project snapshots, capture, export, relocation and sealing. This source neither
assembles delivery ZIPs nor declares unexecuted results to be verified.
"""

import csv
import hashlib
import json
import math
from pathlib import Path
import shutil
import sqlite3
import tempfile
import zipfile


IMAGE = "sha256:1003721d96abe9607d8337b36851f9b29f84c2f8f92b377d1a73ff03c9d15cd2"
FONT_FILE = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_HASH = "ae7b7855e115a5966d8b1b3f80f254ccc117ec86f9965e202ee2940453837280"
PALETTE = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#a65628",
           "#f781bf", "#999999", "#66c2a5", "#c59d00", "#a6d854", "#e5c494", "#8da0cb", "#e78ac3", "#1b9e77", "#666666"]
LIMIT_STEM = "recintos_municipales_inspire_peninbal_etrs89"
LIMIT_MEMBER = f"SHP_ETRS89/{LIMIT_STEM}/{LIMIT_STEM}"
SLUGS = {
    "pr1": "pr1-project-setup", "pr2": "pr2-digitalitzacio",
    "pr3": "pr3-consultes", "pr4": "pr4-geoprocessament",
    "reus": "pr4-tessellacions-reus", "pr5": "pr5-raster",
    "pr6": "pr6-sintesi", "bonus": "bonus-pyqgis-sql",
}
TITLES = {
    "pr1": "Descàrrega CNIG i projecte municipal", "pr2": "Captura · exemple sintètic",
    "pr3": "Consultes municipals", "pr4": "Buffers, superposicions i ROI",
    "reus": "Reus · proximitat postal estimada", "pr5": "Relleu i graelles comparables",
    "pr6": "Model de ROI i síntesi", "bonus": "Reproducció PyQGIS i SQLite",
}
ADDED = {
    "pr1": ["municipi_treball"],
    "pr2": ["fanals", "carrils_bici", "plaques_solars"],
    "pr3": ["municipi_consulta", "municipis_tarragona", "portals_municipi", "illes_municipi",
            "illes_intersectants", "transport_candidats_c06", "vies_secundaries"],
    "pr4": ["fanals_sintetics", "buffers_fanals_10m", "buffers_fanals_30m", "buffers_fanals_50m",
            "buffers_segments_4", "buffers_segments_16", "buffer_linia_arrodonit",
            "buffer_linia_pla", "buffer_linia_quadrat", "buffer_unio_bisell",
            "buffer_unio_mitra", "buffers_dissolts", "unio_buffers_bruta", "zones_solapament",
            "vies_retallades", "vies_interseccio", "vies_exteriors", "municipi_buffer_500m",
            "roi", "rectangle_orientat", "envolupant_convexa", "cercle_minim"],
    "pr5": ["zones_cota_baixa", "estadistiques_raster"],
    "pr6": ["buffer_manual_500m", "roi_manual_500m", "buffer_lot_250m", "roi_lot_250m",
            "buffer_lot_500m", "roi_lot_500m", "buffer_lot_750m", "roi_lot_750m",
            "buffer_model_500m", "roi_model_500m", "buffer_transferencia_reus", "roi_transferencia_reus"],
    "bonus": ["buffer_pyqgis_500m", "roi_pyqgis_500m", "portals_per_codi"],
    "reus": ["portals_generadors", "generadors_entorn_ampli", "portals_validacio",
             "correspondencia_portals", "delaunay_portals", "voronoi_portals",
             "zones_cp_estimades", "zones_cp_entorn_ampli", "validacio_postal"],
}
TABLES = {"fonts_dades", "estadistiques_raster", "portals_per_codi", "correspondencia_portals", "validacio_postal"}
RASTERS = [f"pr5_{variable}_{size}{suffix}.tif" for size in ("25m", "200m")
           for variable, suffix in (("elevacio", ""), ("pendent", "_graus"),
                                    ("orientacio", "_graus"), ("elevacio_classes", ""),
                                    ("mascara_elevacio_pendent", ""))]
DEMO_RASTERS = ["mdt25_mosaic.tif", "mdt25_mascara_municipal.tif", "pendent_percent.tif",
                "orientacio_sectors.tif", "cotes_baixes.tif"]
PREVIOUS = {"pr2": "pr1", "pr3": "pr2", "pr4": "pr3", "pr5": "pr4", "pr6": "pr5", "bonus": "pr6"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def inherited(stage):
    if stage == "pr1":
        return ["recintes_cnig"]
    if stage == "reus":
        return ["recintes_cnig", "municipi_treball", "portals_entorn"]
    prior = PREVIOUS[stage]
    return inherited(prior) + ADDED[prior]


def raster_id(name):
    return name.removesuffix(".tif").replace("_", "-")


def request(stage, root):
    """Materialise one authorised request with actual input hashes, never placeholders."""
    inputs = {"limits-original": "inputs/lineas_limite_cnig_20260728.zip"}
    if stage != "reus":
        inputs.update({"pnoa-image": "inputs/pnoa_vilaseca_context.png",
                       "pnoa-metadata": "inputs/pnoa_vilaseca_procedencia.json",
                       "pnoa-capabilities": "inputs/pnoa_capabilities.xml"})
    if stage in PREVIOUS:
        inputs["previous"] = f"inputs/{SLUGS[PREVIOUS[stage]]}-exemple.gpkg"
    if stage == "pr2":
        inputs["synthetic-original"] = "inputs/pr2_sintetic_original.gpkg"
    if stage in {"pr3", "pr4", "reus", "pr5", "pr6", "bonus"}:
        inputs["cartociudad-original"] = "inputs/cartociudad_tarragona_202604.zip"
    if stage in {"pr3", "reus"}:
        inputs["cartociudad"] = "inputs/tarragona.gpkg"
    if stage in {"pr3", "pr4", "pr5", "pr6", "bonus"}:
        inputs["transport-original"] = "inputs/transport_tarragona_202607.zip"
    if stage == "pr3":
        inputs["transport"] = "inputs/red_viaria.gpkg"
    if stage in {"pr5", "pr6", "bonus"}:
        inputs.update({"mdt25-0472": "inputs/mdt25_0472.tif", "mdt25-0473": "inputs/mdt25_0473.tif",
                       "mdt200-original": "inputs/mdt200_tarragona.tif"})
    if stage in {"pr6", "bonus"}:
        inputs.update({"prior-" + raster_id(name): "inputs/" + name for name in RASTERS})
    if stage == "pr6":
        inputs["roi-model"] = "pr6_roi_municipal.model3"
    if stage == "bonus":
        inputs.update({"bonus-code": "bonus_roi.py", "bonus-sql": "bonus_portals.sql",
                       "postgis-source": "bonus_postgis.sql", "roi-model": "pr6_roi_municipal.model3",
                       "prior-pr6-slope": "inputs/pr6_pendent_roi_graus.tif"})
    for name in inputs.values():
        require((root / name).is_file() and not (root / name).is_symlink(), "Missing regular input: " + name)
    hashes = {identity: digest(root / path) for identity, path in inputs.items()}
    raster_products = []
    initial_rasters = []
    if stage != "reus":
        raster_products.append(dict(id="ortho", path="data/pnoa_context.tif", role="initial-data", format="geotiff", depends_on=[]))
        initial_rasters.append("ortho")
    if stage == "pr5":
        for name in RASTERS + DEMO_RASTERS:
            identity = raster_id(name)
            role = "initial-data" if name == "mdt25_mosaic.tif" else "resolved-data"
            raster_products.append(dict(id=identity, path="data/" + name, role=role, format="geotiff", depends_on=[]))
        initial_rasters.append("mdt25-mosaic")
    elif stage in {"pr6", "bonus"}:
        for name in RASTERS:
            raster_products.append(dict(id=raster_id(name), path="data/" + name, role="initial-data", format="geotiff", depends_on=[]))
            initial_rasters.append(raster_id(name))
        raster_products.append(dict(id="pr6-slope", path="data/pr6_pendent_roi_graus.tif",
                                    role="initial-data" if stage == "bonus" else "resolved-data", format="geotiff", depends_on=[]))
        if stage == "bonus":
            initial_rasters.append("pr6-slope")
    all_rasters = [item["id"] for item in raster_products]
    products = []
    for identity, layers, stored, role, rasters in (
        ("initial-data", inherited(stage), "inicial", "initial-data", initial_rasters),
        ("resolved-data", inherited(stage) + ADDED[stage], stage if stage != "reus" else "reus", "resolved-data", all_rasters),
    ):
        products.append(dict(id=identity,
            path="data/" + ("entrada_docent.gpkg" if identity == "initial-data" else SLUGS[stage] + "-exemple.gpkg"),
            role=role, format="geopackage", depends_on=["font-regular", *rasters],
            members=[dict(kind="table" if name in TABLES else "vector", name=name,
                          role="metadata" if name in TABLES else role) for name in [*layers, "fonts_dades"]]
                    + [dict(kind="project", name=stored, role="initial-project" if identity == "initial-data" else "resolved-project")]))
    products += raster_products + [
        dict(id="font-regular", path="data/fonts/DejaVuSans.ttf", role="initial-data", format="font", depends_on=[]),
        dict(id="font-licence", path="data/fonts/DejaVuSans-licence.csv", role="initial-data", format="csv", depends_on=["font-licence-types"]),
        dict(id="font-licence-types", path="data/fonts/DejaVuSans-licence.csvt", role="initial-data", format="csvt", depends_on=[]),
    ]
    parameters = dict(stage=stage, municipality_code="34094343123" if stage == "reus" else "34094343171",
                      municipality_name="Reus" if stage == "reus" else "Vila-seca", input_hashes=hashes,
                      buffer_distance_m=500, segments=8, initial_rasters=initial_rasters, all_rasters=all_rasters)
    if stage == "reus":
        parameters.update(reus_margins_m=[1500, 3000], holdout_block_m=500,
                          holdout_rule="(floor(x/500) + 2*floor(y/500)) modulo 5 = 0")
    return dict(schema_version=2, kind="qgis-practice-request-v2",
        activity=dict(id=SLUGS[stage], version="0.2.0", title=TITLES[stage]), qgis_image=IMAGE,
        script="compute.py", inputs=[dict(id=key, path=value, sha256=hashes[key]) for key, value in inputs.items()],
        parameters=parameters, products=products,
        fonts=[dict(file="font-regular", family="DejaVu Sans")],
        projects=[dict(id=role, path="projects/" + ("inicial.qgz" if role == "initial-project" else SLUGS[stage] + "-exemple.qgz"),
                       role=role, source_product=product, source_project=stored, compose=True,
                       capture=role == "resolved-project",
                       scene={"setup": [{"action": "close_transients"}, {"action": "show_panel", "title": "Layers"}, {"action": "clear_message_bar"}],
                              "presentation": {"checks": {"project_crs": "EPSG:25831"}}})
                  for role, product, stored in (("initial-project", "initial-data", "inicial"),
                                                ("resolved-project", "resolved-data", stage if stage != "reus" else "reus"))],
        exports=[dict(id="map-pdf", path="figures/mapa-revisio.pdf", format="pdf", project="resolved-project", layout="Mapa de revisió")],
        timeout_seconds=600, locale="ca_ES")


def vector(source, name="Dades", table=None):
    from qgis.core import QgsVectorLayer
    if isinstance(source, QgsVectorLayer):
        return source
    result = QgsVectorLayer(str(source) + ("|layername=" + table if table else ""), name, "ogr")
    require(result.isValid(), "Invalid vector: " + str(source))
    return result


def run(context, algorithm, **parameters):
    return context.processing(algorithm, dict(parameters, OUTPUT="TEMPORARY_OUTPUT"))["OUTPUT"]


def save(context, source, name, product="resolved-data"):
    source = vector(source)
    if source.fields().indexFromName("fid") >= 0:
        source = run(context, "native:deletecolumn", INPUT=source, COLUMN=["fid"])
    return context.processing("native:savefeatures", dict(INPUT=source, OUTPUT=context.output(product),
        LAYER_NAME=name, ACTION_ON_EXISTING_FILE=1 if Path(context.output(product)).exists() else 0,
        DATASOURCE_OPTIONS="", LAYER_OPTIONS=""))


def memory(name, geometry, fields, rows, crs="EPSG:25831"):
    from qgis.core import QgsFeature, QgsVectorLayer
    layer = QgsVectorLayer(geometry + "?crs=" + crs + "&" + "&".join("field=" + field for field in fields), name, "memory")
    require(layer.isValid(), "Invalid memory layer: " + name)
    features = []
    for values, geom in rows:
        feature = QgsFeature(layer.fields())
        feature.setAttributes(list(values))
        if geom is not None:
            feature.setGeometry(geom)
        features.append(feature)
    require(layer.dataProvider().addFeatures(features)[0], "Cannot add features: " + name)
    layer.updateExtents()
    return layer


def one(layer):
    features = list(layer.getFeatures())
    require(len(features) == 1, "Expected one feature: " + layer.name())
    return features[0]


def selected(layer, expression):
    from qgis.core import QgsFeatureRequest
    ids = [feature.id() for feature in layer.getFeatures(QgsFeatureRequest().setFilterExpression(expression))]
    layer.selectByIds(ids)
    return layer.materialize(QgsFeatureRequest().setFilterFids(ids))


def limits(context, folder):
    with zipfile.ZipFile(context.input("limits-original")) as archive:
        for suffix in (".shp", ".shx", ".dbf", ".prj", ".cpg"):
            raw = archive.read(LIMIT_MEMBER + suffix)
            (Path(folder) / (LIMIT_STEM + suffix)).write_bytes(raw)
    return vector(Path(folder) / (LIMIT_STEM + ".shp"), "Recintes CNIG")


def municipal(context, catalogue):
    result = selected(catalogue, f'"NATCODE" = \'{context.parameters["municipality_code"]}\'')
    require(str(one(result)["NAMEUNIT"]) == context.parameters["municipality_name"], "Municipal identity differs")
    result = run(context, "native:reprojectlayer", INPUT=result, TARGET_CRS="EPSG:25831")
    return run(context, "native:fieldcalculator", INPUT=result, FIELD_NAME="codi_muni", FIELD_TYPE=2,
               FIELD_LENGTH=5, FIELD_PRECISION=0, FORMULA='right("NATCODE", 5)')


def buffer(context, layer, distance, segments=8, cap=0, join=0, dissolve=False):
    return run(context, "native:buffer", INPUT=layer, DISTANCE=distance, SEGMENTS=segments,
               END_CAP_STYLE=cap, JOIN_STYLE=join, MITER_LIMIT=2, DISSOLVE=dissolve, SEPARATE_DISJOINT=False)


def table(context, name, fields, rows, product="resolved-data"):
    save(context, memory(name, "None", fields, [(row, None) for row in rows]), name, product)


def resources(context):
    from osgeo import gdal
    require(digest(FONT_FILE) == FONT_HASH, "Pinned font changed")
    shutil.copyfile(FONT_FILE, context.output("font-regular"))
    licence = Path("/usr/share/doc/fonts-dejavu-core/copyright").read_text()
    require("Bitstream" in licence and "permission" in licence.lower(), "Font licence missing")
    with Path(context.output("font-licence")).open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["component", "notice"])
        writer.writerow(["DejaVu Sans", licence])
    Path(context.output("font-licence-types")).write_text('"String","String"\n')
    if "ortho" in context.outputs:
        metadata = json.loads(Path(context.input("pnoa-metadata")).read_text())
        require(digest(context.input("pnoa-image")) == metadata["getmap"]["sha256"], "PNOA provenance differs")
        source = gdal.Open(context.input("pnoa-image"), gdal.GA_ReadOnly)
        require(source is not None and source.RasterCount in (3, 4), "Expected RGB PNOA response")
        if source.RasterCount == 4:
            require((source.GetRasterBand(4).ReadAsArray() == 255).all(), "Unexpected transparent GetMap response")
        west, south, east, north = metadata["bounds"]
        output = gdal.Translate(context.output("ortho"), source, format="GTiff", bandList=[1, 2, 3],
                                outputSRS=metadata["crs"], outputBounds=[west, north, east, south],
                                creationOptions=["COMPRESS=DEFLATE", "TILED=YES"])
        require(output is not None, "Cannot georeference the retained GetMap response")
        output = source = None


def provenance(context, product):
    rows = []
    for identity, path in context.inputs.items():
        note = "Entrada original o snapshot de fase; procedència conservada al bundle."
        owner = "IGN/CNIG" if identity.startswith(("limits", "cartociudad", "transport", "mdt")) else "TIG"
        licence = "CC BY 4.0 ign.es" if owner == "IGN/CNIG" else "Vegeu la font retinguda"
        url = "https://centrodedescargas.cnig.es/CentroDescargas/" if owner == "IGN/CNIG" else ""
        if identity.startswith("pnoa"):
            owner, licence, url = "IGN/PNOA · SCNE", "CC BY 4.0 scne.es", "https://www.ign.es/wms-inspire/pnoa-ma?"
            note = "Context de visualització reescalat; dates i petició a pnoa_vilaseca_procedencia.json."
        if identity == "synthetic-original":
            note = "Només es reutilitzen fanals/carrils/plaques sintètics; es conserva no_apte_per_analisi."
        rows.append([identity, Path(path).name, owner, licence, url, context.parameters["input_hashes"][identity], note])
    rows.append(["font", "DejaVu Sans", "DejaVu / Bitstream", "Llicència adjunta", "https://dejavu-fonts.github.io/License.html", FONT_HASH, "Tipografia local declarada"])
    table(context, "fonts_dades", [field + ":string" for field in ("id", "producte", "productor", "llicencia", "url", "sha256", "observacions")], rows, product)


def compute(context):
    stage = context.parameters["stage"]
    require(stage in SLUGS, "Unknown stage")
    for identity, expected in context.parameters["input_hashes"].items():
        require(digest(context.input(identity)) == expected, "Input changed: " + identity)
    resources(context)
    with tempfile.TemporaryDirectory(prefix="tig-municipal-") as temporary:
        catalogue = limits(context, temporary)
        if stage in ("pr1", "reus"):
            for product in ("initial-data", "resolved-data"):
                save(context, catalogue, "recintes_cnig", product)
            mun = municipal(context, catalogue)
            save(context, mun, "municipi_treball")
            if stage == "reus":
                save(context, mun, "municipi_treball", "initial-data")
        else:
            for name in inherited(stage):
                for product in ("initial-data", "resolved-data"):
                    save(context, vector(context.input("previous"), name, name), name, product)
        if stage == "pr2":
            for name in ADDED[stage]:
                save(context, vector(context.input("synthetic-original"), name, name), name)
        elif stage == "pr3":
            compute_queries(context, catalogue)
        elif stage == "pr4":
            compute_overlays(context)
        elif stage == "reus":
            compute_reus(context)
        elif stage == "pr5":
            compute_rasters(context, temporary)
        elif stage == "pr6":
            compute_model(context, temporary)
        elif stage == "bonus":
            compute_bonus(context)
        for product in ("initial-data", "resolved-data"):
            provenance(context, product)
        author_projects(context)


def author_projects(context):
    from qgis.core import Qgis, QgsCoordinateReferenceSystem, QgsProject, QgsRasterLayer
    stage = context.parameters["stage"]
    products = {key: str(value) for key, value in context.outputs.items()}
    for identity, product, names, stored, rasters in (
        ("initial-project", "initial-data", inherited(stage), "inicial", context.parameters["initial_rasters"]),
        ("resolved-project", "resolved-data", inherited(stage) + ADDED[stage], stage, context.parameters["all_rasters"]),
    ):
        project = QgsProject()
        project.setCrs(QgsCoordinateReferenceSystem("EPSG:25831"))
        project.setEllipsoid("GRS80")
        project.setFilePathStorage(Qgis.FilePathType.Relative)
        for name in rasters:
            layer = QgsRasterLayer(context.output(name), name, "gdal")
            require(layer.isValid(), "Invalid raster: " + name)
            project.addMapLayer(layer)
        for name in [*names, "fonts_dades"]:
            project.addMapLayer(vector(context.output(product), name, name))
        compose(project, identity, context.parameters, products)
        context.embed_project(product, stored, project)
        project.clear()


def signature(layer):
    names = [field.name() for field in layer.fields() if field.name() != "fid"]
    rows = []
    for feature in layer.getFeatures():
        attributes = [str(feature[name]) for name in names]
        geometry = bytes(feature.geometry().asWkb()).hex() if feature.hasGeometry() else ""
        rows.append(json.dumps([attributes, geometry], ensure_ascii=False))
    return hashlib.sha256("\n".join(sorted(rows)).encode()).hexdigest()


def verify(context):
    """Reopen persisted outputs; geometry/attributes and analytical controls are independent."""
    from qgis.core import QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsGeometry, QgsProject
    stage = context.parameters["stage"]
    checks = []

    def check(name, actual, expected=1, tolerance=0, units="boolean"):
        checks.append(dict(id=name, actual=float(actual), expected=float(expected), tolerance=float(tolerance), units=units))

    for identity, expected in context.parameters["input_hashes"].items():
        check("input-" + identity, digest(context.input(identity)) == expected)
    check("font", digest(context.output("font-regular")) == FONT_HASH)
    for product, names in (("initial-data", inherited(stage)), ("resolved-data", inherited(stage) + ADDED[stage])):
        valid_layers = crs_layers = vector_layers = 0
        for name in names:
            layer = vector(context.output(product), name, name)
            if name not in TABLES:
                vector_layers += 1
                valid_layers += all(not f.geometry().isEmpty() and f.geometry().isGeosValid() for f in layer.getFeatures())
                crs_layers += layer.crs().authid() == ("EPSG:4258" if name == "recintes_cnig" else "EPSG:25831")
            if stage in PREVIOUS and name in inherited(stage):
                previous = vector(context.input("previous"), name, name)
                check(product + "-" + name + "-inherited", signature(layer) == signature(previous))
        check(product + "-valid-layers", valid_layers, vector_layers, units="count")
        check(product + "-correct-crs", crs_layers, vector_layers, units="count")
    with tempfile.TemporaryDirectory(prefix="tig-verify-") as temporary:
        catalogue = limits(context, temporary)
        reference = selected(catalogue, f'"NAMEUNIT" = \'{context.parameters["municipality_name"]}\'')
        expected = one(reference)
        check("municipal-source-identity", str(expected["NATCODE"]) == context.parameters["municipality_code"])
        result = one(vector(context.output("resolved-data"), "Municipi", "municipi_treball"))
        check("municipal-identity", str(result["NATCODE"]) == str(expected["NATCODE"]))
        geometry = QgsGeometry(expected.geometry())
        geometry.transform(QgsCoordinateTransform(catalogue.crs(), QgsCoordinateReferenceSystem("EPSG:25831"), QgsProject.instance()))
        check("municipal-transformation", result.geometry().symDifference(geometry).area(), 0, .001, "m2")
        if stage == "pr1":
            for product in ("initial-data", "resolved-data"):
                output = vector(context.output(product), "Catàleg", "recintes_cnig")
                originals = {str(f["NATCODE"]): f for f in catalogue.getFeatures()}
                rows = {str(f["NATCODE"]): f for f in output.getFeatures()}
                check(product + "-catalogue-count", len(rows), 8132, units="count")
                check(product + "-catalogue-identities", set(rows) == set(originals))
                check(product + "-catalogue-geometries", all(f.geometry().isGeosEqual(originals[key].geometry()) for key, f in rows.items()))
                check(product + "-catalogue-attributes", all(all(f[field.name()] == originals[key][field.name()] for field in catalogue.fields()) for key, f in rows.items()))
    if stage == "pr2":
        for name, count in zip(ADDED[stage], (3, 3, 2)):
            layer = vector(context.output("resolved-data"), name, name)
            check(name + "-count", layer.featureCount(), count, units="count")
            check(name + "-original", signature(layer) == signature(vector(context.input("synthetic-original"), name, name)))
            check(name + "-synthetic", all(str(f["estat_rev"]) == "no_apte_per_analisi" for f in layer.getFeatures()))
    elif stage == "pr3":
        verify_queries(context, check)
    elif stage == "pr4":
        verify_overlays(context, check)
    elif stage == "reus":
        verify_reus(context, check)
    elif stage == "pr5":
        verify_rasters(context, check)
    elif stage == "pr6":
        verify_model(context, check)
    elif stage == "bonus":
        verify_bonus(context, check)
    return checks


def compose(project, project_id, parameters, products):
    """Editable review map in the provider-supported map/text subset."""
    from qgis.core import (QgsCoordinateTransform, QgsFeatureRequest, QgsFillSymbol, QgsLayoutItemLabel,
        QgsLayoutItemMap, QgsLayoutPoint, QgsLayoutSize, QgsLineSymbol, QgsMapThemeCollection,
        QgsMarkerSymbol, QgsPalLayerSettings, QgsPrintLayout, QgsRectangle, QgsReferencedRectangle,
        QgsSingleSymbolRenderer, QgsTextFormat, QgsVectorLayerSimpleLabeling)
    from qgis.PyQt.QtGui import QColor, QFont
    stage = parameters["stage"]
    solved = project_id == "resolved-project"
    layers = {layer.name(): layer for layer in project.mapLayers().values()}
    text = QgsTextFormat()
    text.setFont(QFont("DejaVu Sans"))
    text.setSize(9)
    project.styleSettings().setDefaultTextFormat(text)
    for name, layer in layers.items():
        if layer.type() != 0 or name in TABLES:
            continue
        colour = "#555555" if name == "recintes_cnig" else "#2166ac"
        if name in {"municipi_treball", "municipi_consulta"}:
            colour = "#a50f7f"
        if layer.geometryType() == 2:
            layer.setRenderer(QgsSingleSymbolRenderer(QgsFillSymbol.createSimple({"color": "255,255,255,0", "outline_color": colour, "outline_width": "0.35", "outline_width_unit": "MM"})))
        elif layer.geometryType() == 1:
            layer.setRenderer(QgsSingleSymbolRenderer(QgsLineSymbol.createSimple({"line_color": colour, "line_width": "0.35", "line_width_unit": "MM"})))
        else:
            layer.setRenderer(QgsSingleSymbolRenderer(QgsMarkerSymbol.createSimple({"name": "circle", "color": colour, "size": "1.8", "outline_style": "no"})))
        layer.setLabelsEnabled(False)
    label_layer = layers.get("municipi_treball", layers["recintes_cnig"])
    labels = QgsPalLayerSettings()
    labels.fieldName = "NAMEUNIT"
    labels.setFormat(text)
    label_layer.setLabeling(QgsVectorLayerSimpleLabeling(labels))
    label_layer.setLabelsEnabled(True)
    if "municipi_treball" in layers:
        municipality = layers["municipi_treball"]
        extent = QgsRectangle(one(municipality).geometry().boundingBox())
    else:
        catalogue = layers["recintes_cnig"]
        feature = next(catalogue.getFeatures(QgsFeatureRequest().setFilterExpression(f'"NATCODE" = \'{parameters["municipality_code"]}\'')))
        extent = QgsCoordinateTransform(catalogue.crs(), project.crs(), project).transformBoundingBox(feature.geometry().boundingBox())
    extent.scale(1.15)
    main = [layers[name] for name in ("municipi_treball", "recintes_cnig", "ortho") if name in layers]
    if stage == "pr2" and solved:
        main = [layers[name] for name in ("fanals", "carrils_bici", "plaques_solars", "ortho")]
        extent = QgsRectangle(344200, 4551680, 344550, 4552070)
    elif stage == "pr3" and solved:
        main = [layers[name] for name in ("municipi_treball", "transport_candidats_c06", "vies_secundaries", "portals_municipi", "illes_municipi", "ortho")]
    elif stage == "pr4" and solved:
        main = [layers[name] for name in ("roi", "municipi_treball", "municipi_buffer_500m", "ortho")]
        extent = QgsRectangle(one(layers["roi"]).geometry().boundingBox())
        extent.scale(1.1)
    elif stage == "reus":
        main = [layers[name] for name in (("municipi_treball", "portals_generadors", "zones_cp_estimades") if solved else ("municipi_treball", "portals_entorn"))]
    elif stage in {"pr5", "pr6", "bonus"}:
        background = "pr5-elevacio-25m" if solved or stage != "pr5" else "mdt25-mosaic"
        main = [layers[name] for name in ("municipi_treball", "roi", background) if name in layers]
    style_case_layers(layers, stage)
    for layer in layers.values():
        project.layerTreeRoot().findLayer(layer.id()).setItemVisibilityChecked(layer in main)
    project.viewSettings().setDefaultViewExtent(QgsReferencedRectangle(extent, project.crs()))
    project.setTitle(TITLES[stage] + " · " + ("cas resolt de revisió" if solved else "checkpoint docent"))
    for old in list(project.layoutManager().layouts()):
        project.layoutManager().removeLayout(old)
    if not solved:
        return
    layout = QgsPrintLayout(project)
    layout.initializeDefaults()
    layout.setName("Mapa de revisió")
    layout.pageCollection().pages()[0].setPageSize(QgsLayoutSize(297, 210))

    def label(identity, value, x, y, width, height, size=9, colour="#202020"):
        item = QgsLayoutItemLabel(layout)
        layout.addLayoutItem(item)
        item.setId(identity)
        item.setText(value)
        item.setFont(QFont("DejaVu Sans", size))
        item.setFontColor(QColor(colour))
        item.attemptMove(QgsLayoutPoint(x, y))
        item.attemptResize(QgsLayoutSize(width, height))

    label("title", TITLES[stage], 10, 7, 277, 12, 16)
    label("status", "TIG · candidat de revisió docent · EPSG:25831", 10, 21, 277, 8, 10)
    if stage == "pr5":
        shared_extent = QgsRectangle(one(layers["roi"]).geometry().boundingBox())
        shared_extent.scale(1.1)
        scale = math.ceil(max(shared_extent.width() / .131, shared_extent.height() / .13) / 5000) * 5000
        for size, x in ((25, 10), (200, 156)):
            label(f"grid-title-{size}", f"Elevació · cel·la de {size} m", x, 31, 131, 8, 11)
            panel = QgsLayoutItemMap(layout)
            layout.addLayoutItem(panel)
            panel.setId(f"elevacio-{size}m")
            panel.attemptMove(QgsLayoutPoint(x, 42))
            panel.attemptResize(QgsLayoutSize(131, 130))
            panel.setCrs(project.crs())
            panel.setLayers([layers["municipi_treball"], layers[f"pr5-elevacio-{size}m"]])
            panel.setKeepLayerSet(True)
            panel.zoomToExtent(shared_extent)
            panel.setScale(scale)
        label("comparison", f"Mateix origen, extensió i escala 1:{int(scale)}. Altitud en metres: blau (baix) → ocre (alt); rang cromàtic comú 0–160 m.", 10, 175, 277, 8, 8)
        label("limit", "Base de revisió: llegenda nativa i escala gràfica pendents de suport verificat del productor.", 10, 183, 277, 7, 8)
        label("source", "Fonts: límits CNIG i MDT25 PNOA-LiDAR. Graelles 25/200 m derivades directament de la mateixa font. Docència TIG, URV.", 10, 192, 277, 7, 8)
        label("note", "NoData es conserva; el MDT200 publicat es reté com a font separada i no es confon amb aquest experiment.", 10, 200, 277, 7, 8)
        project.layoutManager().addLayout(layout)
        return
    frame = QgsLayoutItemMap(layout)
    layout.addLayoutItem(frame)
    frame.setId("principal")
    frame.attemptMove(QgsLayoutPoint(10, 35))
    frame.attemptResize(QgsLayoutSize(190, 150))
    frame.setCrs(project.crs())
    frame.setLayers(main)
    frame.setKeepLayerSet(True)
    frame.zoomToExtent(extent)
    scale = math.ceil(frame.scale() / (500 if stage == "pr2" else 5000)) * (500 if stage == "pr2" else 5000)
    frame.setScale(scale)
    label("scale", f"Escala numèrica 1:{int(scale):,}\nNord a la part superior".replace(",", "."), 210, 39, 77, 20)
    label("key", map_key(stage), 210, 65, 77, 74, 9)
    if stage == "reus":
        codes = sorted({str(f["cod_postal"]) for f in layers["zones_cp_estimades"].getFeatures()})
        rows_per_column = (len(codes) + 1) // 2
        for index, code in enumerate(codes):
            x = 210 + 39 * (index // rows_per_column)
            y = 103 + 5.5 * (index % rows_per_column)
            label("postal-colour-" + code, "■", x, y, 5, 6, 10, PALETTE[index])
            label("postal-" + code, code, x + 5, y, 32, 6, 9)
    label("limit", "Base editable de revisió.\nLlegenda nativa i escala gràfica:\npendent de suport verificat\ndel productor compartit.", 210, 150, 77, 34, 8)
    source_text = "Fonts: límits CNIG i portals de CartoCiudad; atribucions específiques als originals. Docència TIG, URV." if stage == "reus" else "Fonts: límits i dades IGN/CNIG; PNOA · SCNE. Atribucions i originals al bundle. Docència TIG, URV."
    label("source", source_text, 10, 190, 277, 8, 8)
    note = "Exemple sintètic; no acredita observacions de fanals, carrils o plaques." if stage == "pr2" else "Resultats de demostració: interpretar amb les entrades, els paràmetres i els controls retinguts."
    label("note", note, 10, 199, 277, 8, 8)
    project.layoutManager().addLayout(layout)


def map_key(stage):
    return {
        "pr1": "Contorn magenta: municipi CNIG.\nContorns grisos: recintes.\nPNOA: context de visualització.",
        "pr2": "Punts: fanals sintètics.\nLínies: carrils sintètics.\nPolígons: plaques sintètiques.\nEstat: no_apte_per_analisi.",
        "pr3": "Magenta: límit municipal.\nVermell: autovies/autopistes.\nBlau: vies secundàries.\nGris: illes contingudes.\nPunts: portals seleccionats.",
        "pr4": "Magenta: municipi.\nBlau: buffer de 500 m.\nVerd: ROI rectangular.\nVariants i solapaments\nal GeoPackage resolt.",
        "reus": "Colors: categories postals.\nPunts: generadors d’entrenament.\nFronteres estimades per proximitat,\nno límits postals oficials.\nValidació en blocs separats.",
        "pr5": "Elevació: blau (baixa) a ocre (alta).\nMagenta: límit municipal.\nGraelles de 25 i 200 m\namb origen i extensió comuns.\nNoData es conserva.",
        "pr6": "Municipi i ROI de referència.\nManual, lot i model extern\ncomparats geomètricament.\nDeu ràsters PR5 conservats.",
        "bonus": "Reproducció PyQGIS de la ROI.\nResum SQLite de portals.\nPostGIS: font opcional,\nexecució no acreditada aquí.",
    }[stage]


def style_case_layers(layers, stage):
    from qgis.core import (QgsCategorizedSymbolRenderer, QgsColorRampShader, QgsFillSymbol,
                          QgsLineSymbol, QgsMarkerSymbol, QgsRasterShader, QgsRendererCategory, QgsSingleBandPseudoColorRenderer)
    from qgis.PyQt.QtGui import QColor
    for name, colour in (("transport_candidats_c06", "#b2182b"), ("vies_secundaries", "#2166ac")):
        if name in layers:
            layers[name].renderer().setSymbol(QgsLineSymbol.createSimple({"line_color": colour, "line_width": "0.45"}))
    for name, colour in (("illes_municipi", "#d9d9d9"), ("municipi_buffer_500m", "#b3cde3")):
        if name in layers:
            layers[name].renderer().setSymbol(QgsFillSymbol.createSimple({"color": colour, "outline_color": "#666666", "outline_width": "0.15"}))
    if "roi" in layers:
        layers["roi"].renderer().setSymbol(QgsFillSymbol.createSimple({"color": "255,255,255,0", "outline_color": "#1b7837", "outline_width": "0.6"}))
    if "portals_municipi" in layers:
        layers["portals_municipi"].renderer().setSymbol(QgsMarkerSymbol.createSimple({"name": "circle", "color": "#333333", "size": "0.35", "outline_style": "no"}))
        layers["portals_municipi"].setOpacity(.6)
    if "zones_cp_estimades" in layers:
        layer = layers["zones_cp_estimades"]
        values = sorted({str(f["cod_postal"]) for f in layer.getFeatures()})
        require(len(values) <= len(PALETTE), "Define distinct review colours for the postal categories")
        categories = [QgsRendererCategory(value, QgsFillSymbol.createSimple({"color": PALETTE[index], "outline_color": "#ffffff", "outline_width": "0.1"}), value) for index, value in enumerate(values)]
        layer.setRenderer(QgsCategorizedSymbolRenderer("cod_postal", categories))
        for name in ("portals_generadors", "portals_entorn"):
            layers[name].renderer().setSymbol(QgsMarkerSymbol.createSimple({"name": "circle", "color": "#333333", "size": "0.35", "outline_style": "no"}))
            layers[name].setOpacity(.6)
    for name in ("pr5-elevacio-25m", "pr5-elevacio-200m", "mdt25-mosaic"):
        if name in layers:
            layer = layers[name]
            ramp = QgsColorRampShader(0, 160)
            ramp.setColorRampType(QgsColorRampShader.Interpolated)
            ramp.setColorRampItemList([QgsColorRampShader.ColorRampItem(value, QColor(colour), str(value)) for value, colour in ((0, "#4575b4"), (20, "#e0f3f8"), (80, "#fee090"), (160, "#a6611a"))])
            shader = QgsRasterShader(0, 160)
            shader.setRasterShaderFunction(ramp)
            layer.setRenderer(QgsSingleBandPseudoColorRenderer(layer.dataProvider(), 1, shader))


def compute_queries(context, catalogue):
    raw_municipality = selected(catalogue, f'"NATCODE" = \'{context.parameters["municipality_code"]}\'')
    save(context, municipal(context, catalogue), "municipi_consulta")
    province = selected(catalogue, '"CODNUT3" = \'ES514\'')
    province = run(context, "native:reprojectlayer", INPUT=province, TARGET_CRS="EPSG:25831")
    total_area = sum(feature.geometry().area() for feature in province.getFeatures())
    for name, formula in (("area_m2", "area($geometry)"), ("area_km2", "area($geometry) / 1000000"),
                          ("percent_area", f"100 * area($geometry) / {total_area:.15g}")):
        province = run(context, "native:fieldcalculator", INPUT=province, FIELD_NAME=name,
                       FIELD_TYPE=0, FIELD_LENGTH=20, FIELD_PRECISION=8, FORMULA=formula)
    save(context, province, "municipis_tarragona")
    for name, table_name, predicate, subset in (
        ("portals_municipi", "portalpk_publi", 0, '"tipo" = \'Portal\''),
        ("illes_municipi", "manzana", 6, None),
        ("illes_intersectants", "manzana", 0, None),
    ):
        source = vector(context.input("cartociudad"), name, table_name)
        if subset:
            require(source.setSubsetString(subset), "Cannot filter CartoCiudad")
        result = run(context, "native:extractbylocation", INPUT=source, PREDICATE=[predicate], INTERSECT=raw_municipality)
        result = run(context, "native:reprojectlayer", INPUT=result, TARGET_CRS="EPSG:25831")
        save(context, result, name)
    for name, classes in (
        ("transport_candidats_c06", ("Autopista libre / autovía", "Autopista de peaje")),
        ("vies_secundaries", ("Carretera convencional", "Carretera multicarril")),
    ):
        source = vector(context.input("transport"), name, "rt_tramo_vial")
        expression = '"clased" IN (' + ",".join("'" + value + "'" for value in classes) + ")"
        require(source.setSubsetString(expression), "Cannot filter road classes")
        identified = run(context, "native:fieldcalculator", INPUT=source, FIELD_NAME="id_font",
                         FIELD_TYPE=2, FIELD_LENGTH=32, FIELD_PRECISION=0, FORMULA="to_string($id)")
        result = run(context, "native:extractbylocation", INPUT=identified, PREDICATE=[0], INTERSECT=raw_municipality)
        result = run(context, "native:reprojectlayer", INPUT=result, TARGET_CRS="EPSG:25831")
        result = run(context, "native:fieldcalculator", INPUT=result, FIELD_NAME="longitud_m",
                     FIELD_TYPE=0, FIELD_LENGTH=20, FIELD_PRECISION=6, FORMULA="length($geometry)")
        save(context, result, name)


def verify_queries(context, check):
    from qgis.core import QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsFeatureRequest, QgsGeometry, QgsProject
    with tempfile.TemporaryDirectory(prefix="tig-query-check-") as temporary:
        catalogue = limits(context, temporary)
        municipality = one(selected(catalogue, '"NATCODE" = \'34094343171\'')).geometry()
        transform = QgsCoordinateTransform(catalogue.crs(), QgsCoordinateReferenceSystem("EPSG:25831"), QgsProject.instance())
        for name, table_name, key, predicate, subset, expected_count in (
            ("portals_municipi", "portalpk_publi", "id_porpk", "intersects", lambda f: str(f["tipo"]) == "Portal", 3584),
            ("illes_municipi", "manzana", "id_manz", "within", lambda f: True, 285),
            ("illes_intersectants", "manzana", "id_manz", "intersects", lambda f: True, 318),
            ("transport_candidats_c06", "rt_tramo_vial", "id_font", "intersects", lambda f: str(f["clased"]) in {"Autopista libre / autovía", "Autopista de peaje"}, 265),
            ("vies_secundaries", "rt_tramo_vial", "id_font", "intersects", lambda f: str(f["clased"]) in {"Carretera convencional", "Carretera multicarril"}, None),
        ):
            original = vector(context.input("transport" if table_name == "rt_tramo_vial" else "cartociudad"), name, table_name)
            wanted = {}
            for feature in original.getFeatures(QgsFeatureRequest().setFilterRect(municipality.boundingBox())):
                geometry = feature.geometry()
                matches = geometry.within(municipality) if predicate == "within" else geometry.intersects(municipality)
                if subset(feature) and matches:
                    identity = str(feature.id()) if key == "id_font" else str(feature[key])
                    require(identity not in wanted, "Source identity is not unique: " + name)
                    geometry = QgsGeometry(geometry)
                    geometry.transform(transform)
                    wanted[identity] = geometry
            layer = vector(context.output("resolved-data"), name, name)
            actual = {str(f[key]): f.geometry() for f in layer.getFeatures()}
            check(name + "-ids", set(actual) == set(wanted))
            check(name + "-source-geometries", all(actual[key].isGeosEqual(geometry) for key, geometry in wanted.items()))
            if expected_count is not None:
                check(name + "-reference-count", layer.featureCount(), expected_count, units="count")
        roads = vector(context.output("resolved-data"), "Vies", "transport_candidats_c06")
        check("road-distinct-sections", len({str(f["id_tramo"]) for f in roads.getFeatures()}), 185, units="count")
        check("road-lengths", all(abs(float(f["longitud_m"]) - f.geometry().length()) < .00001 for f in roads.getFeatures()))
        province = vector(context.output("resolved-data"), "Província", "municipis_tarragona")
        check("province-count", province.featureCount(), 184, units="count")
        check("province-area-fields", all(abs(float(f["area_m2"]) - f.geometry().area()) < .001 for f in province.getFeatures()))
        check("province-percent-sum", sum(float(f["percent_area"]) for f in province.getFeatures()), 100, .00001, "percent")


def compute_overlays(context):
    from qgis.core import QgsGeometry
    data = context.output("resolved-data")
    points = vector(data, "Fanals sintètics", "fanals")
    save(context, points, "fanals_sintetics")
    for distance in (10, 30, 50):
        save(context, buffer(context, points, distance), f"buffers_fanals_{distance}m")
    for segments in (4, 16):
        save(context, buffer(context, points, 30, segments=segments), f"buffers_segments_{segments}")
    lines = vector(data, "Carrils sintètics", "carrils_bici")
    for cap, name in enumerate(("arrodonit", "pla", "quadrat")):
        save(context, buffer(context, lines, 10, cap=cap), "buffer_linia_" + name)
    for join, name in ((2, "bisell"), (1, "mitra")):
        save(context, buffer(context, lines, 10, join=join), "buffer_unio_" + name)
    individual = vector(data, "Buffers", "buffers_fanals_50m")
    dissolved = run(context, "native:dissolve", INPUT=individual, FIELD=[], SEPARATE_DISJOINT=False)
    save(context, dissolved, "buffers_dissolts")
    union = run(context, "native:union", INPUT=individual)
    save(context, union, "unio_buffers_bruta")
    parts = run(context, "native:multiparttosingleparts", INPUT=union)
    unique = vector(run(context, "native:deleteduplicategeometries", INPUT=parts))
    buffers = list(individual.getFeatures())
    rows = []
    for index, feature in enumerate(unique.getFeatures(), 1):
        geometry = QgsGeometry(feature.geometry())
        interior = geometry.pointOnSurface()
        count = len({str(f["id_fanal"]) for f in buffers if f.geometry().contains(interior)})
        require(count > 0, "A union piece has no generating buffer")
        rows.append(([index, count, geometry.area()], geometry))
    save(context, memory("Peces", "Polygon", ["id_zona:integer", "n_fanals:integer", "area_m2:double"], rows), "zones_solapament")
    municipality = vector(data, "Municipi", "municipi_treball")
    roads = vector(data, "Vies", "transport_candidats_c06")
    for algorithm, name in (("native:clip", "vies_retallades"), ("native:intersection", "vies_interseccio"), ("native:difference", "vies_exteriors")):
        result = run(context, algorithm, INPUT=roads, OVERLAY=municipality)
        result = run(context, "native:fieldcalculator", INPUT=result, FIELD_NAME="longitud_resultat_m", FIELD_TYPE=0,
                     FIELD_LENGTH=20, FIELD_PRECISION=6, FORMULA="length($geometry)")
        save(context, result, name)
    municipal_buffer = buffer(context, municipality, 500)
    save(context, municipal_buffer, "municipi_buffer_500m")
    for algorithm, name in (("native:boundingboxes", "roi"), ("native:orientedminimumboundingbox", "rectangle_orientat"),
                            ("native:convexhull", "envolupant_convexa"), ("native:minimumenclosingcircle", "cercle_minim")):
        parameters = dict(INPUT=municipal_buffer)
        if name == "cercle_minim":
            parameters["SEGMENTS"] = 720
        save(context, run(context, algorithm, **parameters), name)


def verify_overlays(context, check):
    from qgis.core import QgsGeometry
    data = context.output("resolved-data")
    points = {str(f["id_fanal"]): f.geometry().asPoint() for f in vector(data, "Punts", "fanals_sintetics").getFeatures()}
    for distance, segments, name in ((10, 8, "buffers_fanals_10m"), (30, 8, "buffers_fanals_30m"),
                                     (50, 8, "buffers_fanals_50m"), (30, 4, "buffers_segments_4"), (30, 16, "buffers_segments_16")):
        layer = vector(data, name, name)
        rows = list(layer.getFeatures())
        expected_area = 4 * segments * distance ** 2 * math.sin(2 * math.pi / (4 * segments)) / 2
        check(name + "-count", len(rows), len(points), units="count")
        check(name + "-regular-area", max(abs(f.geometry().area() - expected_area) for f in rows), 0, .0001, "m2")
        check(name + "-radius", max(abs(math.hypot(v.x() - points[str(f["id_fanal"])].x(), v.y() - points[str(f["id_fanal"])].y()) - distance)
                                     for f in rows for v in f.geometry().vertices()), 0, .00001, "m")
    individual = [f.geometry() for f in vector(data, "Buffers", "buffers_fanals_50m").getFeatures()]
    pieces = list(vector(data, "Zones", "zones_solapament").getFeatures())
    footprint = QgsGeometry.unaryUnion(individual)
    rebuilt = QgsGeometry.unaryUnion([f.geometry() for f in pieces])
    check("union-coverage", footprint.symDifference(rebuilt).area(), 0, .0001, "m2")
    check("union-disjoint-interiors", sum(a.geometry().intersection(b.geometry()).area() for index, a in enumerate(pieces) for b in pieces[index + 1:]), 0, .0001, "m2")
    check("union-weighted-area", sum(int(f["n_fanals"]) * f.geometry().area() for f in pieces), sum(g.area() for g in individual), .0001, "m2")
    check("union-multiplicities", {int(f["n_fanals"]) for f in pieces} == {1, 2, 3})
    municipality = one(vector(data, "Municipi", "municipi_treball")).geometry()
    for name in ("vies_retallades", "vies_interseccio"):
        rows = list(vector(data, name, name).getFeatures())
        check(name + "-inside", max((f.geometry().difference(municipality).length() for f in rows), default=0), 0, .001, "m")
        check(name + "-lengths", all(abs(float(f["longitud_resultat_m"]) - f.geometry().length()) < .00001 for f in rows))
    inside = QgsGeometry.unaryUnion([f.geometry() for f in vector(data, "Interior", "vies_retallades").getFeatures()])
    outside = QgsGeometry.unaryUnion([f.geometry() for f in vector(data, "Exterior", "vies_exteriors").getFeatures()])
    original = QgsGeometry.unaryUnion([f.geometry() for f in vector(data, "Original", "transport_candidats_c06").getFeatures()])
    rebuilt_roads = inside.combine(outside)
    # Overlay intersections can differ by a floating-point ulp from their source
    # segment. Exact symmetric difference then counts a whole segment twice.
    # A 1 mm metric certificate is far below the source's cartographic precision;
    # preserve per-source-row length as a second, independent partition control.
    check("road-partition-hausdorff", original.hausdorffDistance(rebuilt_roads), 0, .001, "m")
    missing = original.difference(rebuilt_roads.buffer(.001, 8))
    excess = rebuilt_roads.difference(original.buffer(.001, 8))
    require(not missing.lastError() and not excess.lastError(), "Road support check failed")
    check("road-partition-support", missing.length() + excess.length(), 0, .000001, "m")
    lengths = {}
    for name in ("vies_retallades", "vies_exteriors"):
        for feature in vector(data, name, name).getFeatures():
            key = str(feature["id_font"])
            lengths[key] = lengths.get(key, 0) + feature.geometry().length()
    check("road-partition-per-id", max(abs(f.geometry().length() - lengths.get(str(f["id_font"]), 0))
                                         for f in vector(data, "Vies originals", "transport_candidats_c06").getFeatures()), 0, .000001, "m")
    buf = one(vector(data, "Buffer", "municipi_buffer_500m")).geometry()
    check("buffer-covers-municipality", municipality.difference(buf).area(), 0, .001, "m2")
    roi = one(vector(data, "ROI", "roi")).geometry()
    check("roi-exact-envelope", roi.isGeosEqual(QgsGeometry.fromRect(buf.boundingBox())))
    for name in ("rectangle_orientat", "envolupant_convexa"):
        geometry = one(vector(data, name, name)).geometry()
        check(name + "-contains", buf.difference(geometry).area(), 0, .01, "m2")
    circle = one(vector(data, "Cercle", "cercle_minim"))
    centre = circle.geometry().centroid().asPoint()
    radius = float(circle["radius"])
    check("minimum-circle-true-radius", max(math.hypot(v.x() - centre.x(), v.y() - centre.y()) for v in buf.vertices()) <= radius + .001)
    check("minimum-circle-discretisation", circle.geometry().area(), 720 * radius ** 2 * math.sin(2 * math.pi / 720) / 2, .1, "m2")


def raster_array(path):
    import numpy as np
    from osgeo import gdal
    dataset = gdal.Open(str(path), gdal.GA_ReadOnly)
    require(dataset is not None, "Cannot open raster: " + str(path))
    band = dataset.GetRasterBand(1)
    array = band.ReadAsArray()
    nodata = band.GetNoDataValue()
    valid = np.isfinite(array) & (array != nodata) if nodata is not None else np.isfinite(array)
    return dataset, array, valid


def write_raster(path, array, transform, projection, nodata=-32767):
    import numpy as np
    from osgeo import gdal
    integer = nodata == 255
    dataset = gdal.GetDriverByName("GTiff").Create(str(path), array.shape[1], array.shape[0], 1,
        gdal.GDT_Byte if integer else gdal.GDT_Float32,
        options=["COMPRESS=DEFLATE", "TILED=YES", "PREDICTOR=" + ("2" if integer else "3")])
    require(dataset is not None, "Cannot create raster")
    dataset.SetGeoTransform(transform)
    dataset.SetProjection(projection)
    dataset.GetRasterBand(1).SetNoDataValue(nodata)
    dataset.GetRasterBand(1).WriteArray(array.astype(np.uint8 if integer else np.float32))
    dataset.FlushCache()
    dataset = None


def cell_mask(geometry, shape, transform, projection):
    from osgeo import gdal, ogr, osr
    raster = gdal.GetDriverByName("MEM").Create("", shape[1], shape[0], 1, gdal.GDT_Byte)
    raster.SetGeoTransform(transform)
    raster.SetProjection(projection)
    datasource = ogr.GetDriverByName("Memory").CreateDataSource("")
    srs = osr.SpatialReference(wkt=projection)
    layer = datasource.CreateLayer("mask", srs, ogr.wkbMultiPolygon)
    feature = ogr.Feature(layer.GetLayerDefn())
    feature.SetGeometry(ogr.CreateGeometryFromWkb(bytes(geometry.asWkb())))
    require(layer.CreateFeature(feature) == 0, "Cannot prepare independent pixel mask")
    require(gdal.RasterizeLayer(raster, [1], layer, burn_values=[1]) == 0, "Cannot rasterise municipal mask")
    result = raster.GetRasterBand(1).ReadAsArray().astype(bool)
    raster = datasource = feature = None
    return result


def compute_rasters(context, temporary):
    import numpy as np
    from osgeo import gdal, ogr, osr
    gdal.UseExceptions()
    temporary = Path(temporary)
    vrt_path = temporary / "mosaic.vrt"
    vrt = gdal.BuildVRT(str(vrt_path), [context.input("mdt25-0472"), context.input("mdt25-0473")],
                        srcNodata=-32767, VRTNodata=-32767, resolution="highest")
    require(vrt is not None, "Mosaic failed")
    mosaic = gdal.Translate(context.output("mdt25-mosaic"), vrt, format="GTiff",
                            creationOptions=["COMPRESS=DEFLATE", "TILED=YES"])
    require(mosaic is not None, "Cannot persist mosaic")
    projection = mosaic.GetProjection()
    mosaic = None
    data = context.output("resolved-data")
    municipal_layer = vector(data, "Municipi", "municipi_treball")
    municipality = one(municipal_layer).geometry()
    roi = one(vector(data, "ROI", "roi")).geometry().boundingBox()
    west, south = math.floor(roi.xMinimum() / 200) * 200, math.floor(roi.yMinimum() / 200) * 200
    east, north = math.ceil(roi.xMaximum() / 200) * 200, math.ceil(roi.yMaximum() / 200) * 200
    for size in (25, 200):
        transform = (west, size, 0, north, 0, -size)
        halo_path = temporary / f"elevation_halo_{size}.tif"
        halo = gdal.Warp(str(halo_path), vrt, format="GTiff", dstSRS="EPSG:25831",
                         outputBounds=[west - size, south - size, east + size, north + size],
                         xRes=size, yRes=size, resampleAlg="average", srcNodata=-32767, dstNodata=-32767,
                         outputType=gdal.GDT_Float32)
        require(halo is not None, "Cannot create the common-source grid")
        halo.FlushCache()
        elevations = halo.GetRasterBand(1).ReadAsArray()[1:-1, 1:-1]
        valid = np.isfinite(elevations) & (elevations != -32767)
        write_raster(context.output(f"pr5-elevacio-{size}m"), elevations, transform, projection)
        derivatives = {}
        for operation in ("slope", "aspect"):
            path = temporary / f"{operation}_{size}.tif"
            options = dict(format="GTiff", alg="Horn", computeEdges=False)
            if operation == "slope":
                options.update(scale=1, slopeFormat="degree")
            derivative = gdal.DEMProcessing(str(path), halo, operation, **options)
            require(derivative is not None, "DEM derivative failed")
            derivative.FlushCache()
            band = derivative.GetRasterBand(1)
            array = band.ReadAsArray()[1:-1, 1:-1]
            good = np.isfinite(array) & (array != band.GetNoDataValue())
            array = np.where(good, array, -32767)
            derivatives[operation] = (array, good)
            name = "pendent" if operation == "slope" else "orientacio"
            write_raster(context.output(f"pr5-{name}-{size}m-graus"), array, transform, projection)
            derivative = None
        slope, slope_valid = derivatives["slope"]
        aspect, aspect_valid = derivatives["aspect"]
        classes = np.where(valid, np.digitize(elevations, [20, 50, 100]) + 1, 255)
        write_raster(context.output(f"pr5-elevacio-classes-{size}m"), classes, transform, projection, 255)
        combined = np.where(valid & slope_valid, ((elevations < 20) & (slope < 2)).astype(np.uint8), 255)
        write_raster(context.output(f"pr5-mascara-elevacio-pendent-{size}m"), combined, transform, projection, 255)
        if size == 25:
            mask = cell_mask(municipality, elevations.shape, transform, projection)
            write_raster(context.output("mdt25-mascara-municipal"), np.where(valid & mask, elevations, -32767), transform, projection)
            percentage = gdal.DEMProcessing(str(temporary / "slope_percent.tif"), halo, "slope",
                                            format="GTiff", alg="Horn", computeEdges=False, scale=1, slopeFormat="percent")
            require(percentage is not None, "Percentage slope failed")
            band = percentage.GetRasterBand(1)
            values = band.ReadAsArray()[1:-1, 1:-1]
            write_raster(context.output("pendent-percent"), np.where(values != band.GetNoDataValue(), values, -32767), transform, projection)
            percentage = None
            sectors = np.full(elevations.shape, 255, dtype=np.uint8)
            sectors[slope_valid & (slope < 2)] = 0
            steep = slope_valid & (slope >= 2) & aspect_valid
            for number, condition in ((1, (aspect >= 315) | (aspect < 45)), (2, (aspect >= 45) & (aspect < 135)),
                                      (3, (aspect >= 135) & (aspect < 225)), (4, (aspect >= 225) & (aspect < 315))):
                sectors[steep & condition] = number
            write_raster(context.output("orientacio-sectors"), sectors, transform, projection, 255)
            low = np.where(valid & mask, np.where(elevations < 2, 1, 2), 255)
            write_raster(context.output("cotes-baixes"), low, transform, projection, 255)
        halo = None
    vrt = None
    polygon_path = temporary / "cotes.gpkg"
    polygon_ds = ogr.GetDriverByName("GPKG").CreateDataSource(str(polygon_path))
    polygon_layer = polygon_ds.CreateLayer("cotes", osr.SpatialReference(wkt=projection), ogr.wkbPolygon)
    polygon_layer.CreateField(ogr.FieldDefn("classe", ogr.OFTInteger))
    raster = gdal.Open(context.output("cotes-baixes"))
    band = raster.GetRasterBand(1)
    require(gdal.Polygonize(band, band.GetMaskBand(), polygon_layer, 0, []) == 0, "Polygonisation failed")
    polygon_layer = polygon_ds = raster = None
    polygons = vector(polygon_path, "Cotes", "cotes")
    low_polygons = selected(polygons, '"classe" = 1')
    low_polygons = run(context, "native:fieldcalculator", INPUT=low_polygons, FIELD_NAME="area_m2", FIELD_TYPE=0,
                       FIELD_LENGTH=20, FIELD_PRECISION=6, FORMULA="area($geometry)")
    save(context, low_polygons, "zones_cota_baixa")
    statistics = []
    for name in RASTERS:
        identity = raster_id(name)
        result = vector(run(context, "native:zonalstatisticsfb", INPUT=municipal_layer,
                            INPUT_RASTER=context.output(identity), RASTER_BAND=1,
                            COLUMN_PREFIX="z_", STATISTICS=[0, 2, 5, 6]))
        feature = one(result)
        statistics.append([name, 25 if "_25m" in name else 200,
                           float(feature["z_count"]), float(feature["z_mean"]), float(feature["z_min"]), float(feature["z_max"]),
                           "QGIS zonalstatisticsfb; municipi CNIG"])
    table(context, "estadistiques_raster", ["variable:string", "resolucio:integer", "n_valides:double", "mitjana:double", "minim:double", "maxim:double", "regla:string"], statistics)


def verify_rasters(context, check):
    import numpy as np
    data = context.output("resolved-data")
    municipality = one(vector(data, "Municipi", "municipi_treball")).geometry()
    grids = {}
    for size in (25, 200):
        dataset, elevation, valid = raster_array(context.output(f"pr5-elevacio-{size}m"))
        transform, projection = dataset.GetGeoTransform(), dataset.GetProjection()
        grids[size] = (transform, elevation.shape)
        check(f"grid-{size}-crs", dataset.GetSpatialRef().GetAuthorityCode(None) == "25831")
        check(f"grid-{size}-resolution", transform[1] == size and transform[5] == -size and transform[2] == transform[4] == 0)
        check(f"grid-{size}-valid", int(valid.sum()) > 0)
        slope_ds, slope, good_slope = raster_array(context.output(f"pr5-pendent-{size}m-graus"))
        aspect_ds, aspect, good_aspect = raster_array(context.output(f"pr5-orientacio-{size}m-graus"))
        classes_ds, classes, good_classes = raster_array(context.output(f"pr5-elevacio-classes-{size}m"))
        mask_ds, mask, good_mask = raster_array(context.output(f"pr5-mascara-elevacio-pendent-{size}m"))
        check(f"grid-{size}-alignment", all(ds.GetGeoTransform() == transform and (ds.RasterYSize, ds.RasterXSize) == elevation.shape for ds in (slope_ds, aspect_ds, classes_ds, mask_ds)))
        check(f"classes-{size}", np.array_equal(good_classes, valid) and np.array_equal(classes[valid], np.digitize(elevation[valid], [20, 50, 100]) + 1))
        check(f"mask-{size}", np.array_equal(good_mask, valid & good_slope) and np.array_equal(mask[good_mask], ((elevation < 20) & (slope < 2))[good_mask]))
        nine = [elevation[y:y + elevation.shape[0] - 2, x:x + elevation.shape[1] - 2].astype(float) for y in range(3) for x in range(3)]
        usable = np.logical_and.reduce([np.isfinite(a) & (a != -32767) for a in nine])
        a, b, c, d, e, f, g, h, i = nine
        dx = (c + 2 * f + i - a - 2 * d - g) / (8 * size)
        dy = (g + 2 * h + i - a - 2 * b - c) / (8 * size)
        expected_slope = np.degrees(np.arctan(np.hypot(dx, dy)))
        require(usable.any(), "No independent Horn controls")
        check(f"horn-slope-{size}", float(np.max(np.abs(slope[1:-1, 1:-1][usable] - expected_slope[usable]))), 0, .0001, "degrees")
        sloped = usable & (expected_slope >= 2)
        expected_aspect = np.degrees(np.arctan2(-dx, dy)) % 360
        error = np.abs((aspect[1:-1, 1:-1] - expected_aspect + 180) % 360 - 180)
        # GDAL's float32 Horn window has cancellation error, especially near flat
        # terrain. Bound eight elementary float32 operations by gamma_8 times
        # the weighted absolute inputs, then propagate the gradient error to
        # angular error. Compare directions only in the declared non-flat class.
        epsilon = np.finfo(np.float32).eps
        gamma = 8 * epsilon / (1 - 8 * epsilon)
        bx = gamma * (abs(c) + 2 * abs(f) + abs(i) + abs(a) + 2 * abs(d) + abs(g)) / (8 * size)
        by = gamma * (abs(g) + 2 * abs(h) + abs(i) + abs(a) + 2 * abs(b) + abs(c)) / (8 * size)
        gradient_error = np.hypot(bx, by)
        gradient = np.hypot(dx, dy)
        ratio = np.divide(gradient_error, gradient, out=np.ones_like(gradient), where=gradient > 0)
        bound = np.where(ratio < 1, np.degrees(np.arcsin(np.minimum(ratio, 1))), 180) + .00005
        require(sloped.any(), "No non-flat aspect controls")
        check(f"horn-aspect-{size}-domain", np.all(good_aspect[1:-1, 1:-1][sloped]))
        check(f"horn-aspect-{size}-roundoff", max(0, float((error - bound)[sloped].max())), 0, .0000001, "degrees")
        municipal_mask = cell_mask(municipality, elevation.shape, transform, projection)
        for name, values, domain in (("elevacio", elevation, valid), ("pendent", slope, good_slope), ("orientacio", aspect, good_aspect)):
            filename = f"pr5_{name}_{size}m" + ("_graus" if name != "elevacio" else "") + ".tif"
            recorded = [f for f in vector(data, "Estadístiques", "estadistiques_raster").getFeatures() if str(f["variable"]) == filename]
            require(len(recorded) == 1, "Missing zonal statistics")
            selected_values = values[municipal_mask & domain]
            check(f"zonal-count-{name}-{size}", float(recorded[0]["n_valides"]), len(selected_values), units="cells")
            check(f"zonal-mean-{name}-{size}", float(recorded[0]["mitjana"]), float(selected_values.mean(dtype=np.float64)), .0001, "value")
        if size == 25:
            _, percentage, percent_valid = raster_array(context.output("pendent-percent"))
            check("slope-percent-domain", np.array_equal(percent_valid, good_slope))
            check("slope-degree-percent", float(np.max(np.abs(percentage[percent_valid] - 100 * np.tan(np.radians(slope[percent_valid].astype(float)))))), 0, .0001, "percent")
            _, masked, masked_valid = raster_array(context.output("mdt25-mascara-municipal"))
            check("municipal-nodata-mask", np.array_equal(masked_valid, valid & municipal_mask) and np.array_equal(masked[masked_valid], elevation[masked_valid]))
            _, low, low_valid = raster_array(context.output("cotes-baixes"))
            check("low-elevation-domain", np.array_equal(low_valid, masked_valid))
            check("low-elevation-classes", np.array_equal(low[low_valid], np.where(elevation[low_valid] < 2, 1, 2)))
            area = sum(f.geometry().area() for f in vector(data, "Cotes", "zones_cota_baixa").getFeatures())
            check("low-polygon-pixel-area", area, int((low == 1).sum()) * 625, .001, "m2")
            _, sectors, sector_valid = raster_array(context.output("orientacio-sectors"))
            check("flat-orientation", np.all(sectors[good_slope & (slope < 2)] == 0))
        dataset = slope_ds = aspect_ds = classes_ds = mask_ds = None
    fine, coarse = grids[25], grids[200]
    check("nested-grid-origin", fine[0][0] == coarse[0][0] and fine[0][3] == coarse[0][3])
    check("nested-grid-shape", fine[1][0] == 8 * coarse[1][0] and fine[1][1] == 8 * coarse[1][1])


def copy_pr5(context):
    for name in RASTERS:
        shutil.copyfile(context.input("prior-" + raster_id(name)), context.output(raster_id(name)))


def compute_model(context, temporary):
    import numpy as np
    from osgeo import gdal
    from qgis.core import QgsApplication, QgsProcessingModelAlgorithm, QgsProcessingProvider
    copy_pr5(context)
    municipal_layer = vector(context.output("resolved-data"), "Municipi", "municipi_treball")
    for distance, prefix in ((500, "manual"), (250, "lot"), (500, "lot"), (750, "lot")):
        buffered = buffer(context, municipal_layer, distance)
        save(context, buffered, f"buffer_{prefix}_{distance}m")
        save(context, run(context, "native:boundingboxes", INPUT=buffered), f"roi_{prefix}_{distance}m")

    class MunicipalModelProvider(QgsProcessingProvider):
        def id(self):
            return "tig_review"

        def name(self):
            return "TIG · model de ROI"

        def loadAlgorithms(self):
            model = QgsProcessingModelAlgorithm()
            require(model.fromFile(context.input("roi-model")), "Cannot open the authored model")
            require({child.algorithmId() for child in model.childAlgorithms().values()} == {"native:buffer", "native:boundingboxes"}, "Unexpected model graph")
            require(len(model.childAlgorithms()) == 2, "Expected the two-node ROI model")
            self.addAlgorithm(model)

    registry = QgsApplication.processingRegistry()
    provider = MunicipalModelProvider()
    require(registry.addProvider(provider), "Cannot register the scoped authored model")
    try:
        algorithm = "tig_review:pr6_roi_municipal"
        require(registry.algorithmById(algorithm) is not None, "Authored model is unavailable")
        for layer, suffix in ((municipal_layer, "model_500m"),):
            results = context.processing(algorithm, {"MUNICIPI": layer, "DISTANCIA": 500,
                                                      "buffer:BUFFER": "TEMPORARY_OUTPUT", "caixa:ROI": "TEMPORARY_OUTPUT"})
            save(context, results["buffer:BUFFER"], "buffer_" + suffix)
            save(context, results["caixa:ROI"], "roi_" + suffix)
        catalogue = limits(context, temporary)
        reus = selected(catalogue, '"NATCODE" = \'34094343123\'')
        require(str(one(reus)["NAMEUNIT"]) == "Reus", "Transfer municipality differs")
        reus = run(context, "native:reprojectlayer", INPUT=reus, TARGET_CRS="EPSG:25831")
        results = context.processing(algorithm, {"MUNICIPI": reus, "DISTANCIA": 500,
                                                  "buffer:BUFFER": "TEMPORARY_OUTPUT", "caixa:ROI": "TEMPORARY_OUTPUT"})
        save(context, results["buffer:BUFFER"], "buffer_transferencia_reus")
        save(context, results["caixa:ROI"], "roi_transferencia_reus")
    finally:
        registry.removeProvider(provider)
    # Re-execute the terrain branch from the two original MDT25 tiles. The grid
    # is the common PR5 grid, itself aligned to the model's 500 m rectangular ROI.
    reference = gdal.Open(context.output("pr5-elevacio-25m"))
    transform, projection = reference.GetGeoTransform(), reference.GetProjection()
    west, north, size = transform[0], transform[3], transform[1]
    east = west + size * reference.RasterXSize
    south = north - size * reference.RasterYSize
    vrt = gdal.BuildVRT(str(Path(temporary) / "model_mosaic.vrt"), [context.input("mdt25-0472"), context.input("mdt25-0473")], srcNodata=-32767, VRTNodata=-32767)
    halo = gdal.Warp(str(Path(temporary) / "model_halo.tif"), vrt, format="GTiff", dstSRS="EPSG:25831",
                     outputBounds=[west - size, south - size, east + size, north + size],
                     xRes=size, yRes=size, resampleAlg="average", srcNodata=-32767, dstNodata=-32767, outputType=gdal.GDT_Float32)
    derivative = gdal.DEMProcessing(str(Path(temporary) / "model_slope.tif"), halo, "slope",
                                    format="GTiff", alg="Horn", computeEdges=False, scale=1, slopeFormat="degree")
    require(derivative is not None, "Integrated terrain branch failed")
    band = derivative.GetRasterBand(1)
    values = band.ReadAsArray()[1:-1, 1:-1]
    write_raster(context.output("pr6-slope"), np.where(values != band.GetNoDataValue(), values, -32767), transform, projection)
    reference = vrt = halo = derivative = None


def verify_model(context, check):
    import numpy as np
    from qgis.core import QgsGeometry
    data = context.output("resolved-data")
    for name in RASTERS:
        check("retained-" + raster_id(name), digest(context.output(raster_id(name))) == digest(context.input("prior-" + raster_id(name))))
    buffers = {key: one(vector(data, key, "buffer_" + key)).geometry() for key in ("manual_500m", "lot_250m", "lot_500m", "lot_750m", "model_500m", "transferencia_reus")}
    boxes = {key: one(vector(data, key, "roi_" + key)).geometry() for key in buffers}
    for key in buffers:
        check("box-" + key, boxes[key].isGeosEqual(QgsGeometry.fromRect(buffers[key].boundingBox())))
    for key in ("lot_500m", "model_500m"):
        check("buffer-equivalence-" + key, buffers[key].isGeosEqual(buffers["manual_500m"]))
        check("box-equivalence-" + key, boxes[key].isGeosEqual(boxes["manual_500m"]))
    check("margin-monotonic", boxes["lot_250m"].within(boxes["lot_500m"]) and boxes["lot_500m"].within(boxes["lot_750m"]))
    check("pr4-roi-equivalence", boxes["model_500m"].isGeosEqual(one(vector(data, "ROI PR4", "roi")).geometry()))
    transfer = one(vector(data, "Transferència", "roi_transferencia_reus"))
    check("model-transfer-identity", str(transfer["NATCODE"]) == "34094343123")
    reference, original, original_valid = raster_array(context.input("prior-pr5-pendent-25m-graus"))
    result, values, valid = raster_array(context.output("pr6-slope"))
    check("terrain-grid", result.GetGeoTransform() == reference.GetGeoTransform() and values.shape == original.shape)
    check("terrain-domain", np.array_equal(valid, original_valid))
    check("terrain-reexecution", float(np.max(np.abs(values[valid] - original[valid]))), 0, .000001, "degrees")


def compute_bonus(context):
    import importlib.util
    copy_pr5(context)
    shutil.copyfile(context.input("prior-pr6-slope"), context.output("pr6-slope"))
    spec = importlib.util.spec_from_file_location("tig_bonus_roi", context.input("bonus-code"))
    example = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(example)
    municipal_layer = vector(context.output("resolved-data"), "Municipi", "municipi_treball")
    buffered, box = example.make_roi(context.processing, municipal_layer)
    save(context, buffered, "buffer_pyqgis_500m")
    save(context, box, "roi_pyqgis_500m")
    with sqlite3.connect("file:" + context.input("previous") + "?mode=ro&immutable=1", uri=True) as connection:
        connection.execute("PRAGMA query_only=ON")
        rows = connection.execute(Path(context.input("bonus-sql")).read_text()).fetchall()
    table(context, "portals_per_codi", ["cod_postal:string", "n_portals:integer"], rows)


def verify_bonus(context, check):
    from collections import Counter
    data = context.output("resolved-data")
    for name in RASTERS:
        check("retained-" + raster_id(name), digest(context.output(raster_id(name))) == digest(context.input("prior-" + raster_id(name))))
    check("retained-pr6-slope", digest(context.output("pr6-slope")) == digest(context.input("prior-pr6-slope")))
    for kind in ("buffer", "roi"):
        actual = one(vector(data, kind, kind + "_pyqgis_500m")).geometry()
        expected = one(vector(data, kind, kind + "_model_500m")).geometry()
        check("pyqgis-" + kind, actual.isGeosEqual(expected))
    original = vector(data, "Portals", "portals_municipi")
    expected = Counter(str(feature["cod_postal"]) for feature in original.getFeatures())
    actual = {str(feature["cod_postal"]): int(feature["n_portals"]) for feature in vector(data, "Resum", "portals_per_codi").getFeatures()}
    check("sql-postal-groups", dict(expected) == actual)
    check("sql-total", sum(actual.values()), original.featureCount(), units="count")


def compute_reus(context):
    from collections import Counter
    import numpy as np
    from scipy.spatial import cKDTree
    from qgis.core import QgsFeatureRequest, QgsGeometry, QgsPointXY, QgsRectangle
    data = context.output("resolved-data")
    municipality = one(vector(data, "Reus", "municipi_treball")).geometry()
    inner = QgsRectangle(municipality.boundingBox())
    outer = QgsRectangle(inner)
    inner.grow(context.parameters["reus_margins_m"][0])
    outer.grow(context.parameters["reus_margins_m"][1])
    original = vector(context.input("cartociudad"), "Portals provincials", "portalpk_publi")
    require(original.setSubsetString('"tipo" = \'Portal\''), "Cannot filter portals")
    projected = vector(run(context, "native:reprojectlayer", INPUT=original, TARGET_CRS="EPSG:25831"))
    regional = projected.materialize(QgsFeatureRequest().setFilterRect(outer))
    save(context, regional, "portals_entorn", "initial-data")
    save(context, regional, "portals_entorn")
    groups = {}
    for feature in regional.getFeatures():
        point = feature.geometry().asPoint()
        groups.setdefault((point.x(), point.y()), []).append(feature)
    fields = ["id_generador:string", "cod_postal:string", "n_portals:integer", "particio:string"]
    narrow_rows, wide_rows, validation_rows, correspondence = [], [], [], []
    for (x, y), records in sorted(groups.items()):
        identity = "g" + hashlib.sha256((x.hex() + ":" + y.hex()).encode()).hexdigest()[:16]
        codes = {str(f["cod_postal"]).strip() for f in records}
        codes = {"__sense_codi__" if value in {"", "NULL", "None"} else value for value in codes}
        code = next(iter(codes)) if len(codes) == 1 else "__conflicte__"
        held_out = (math.floor(x / 500) + 2 * math.floor(y / 500)) % 5 == 0
        partition = "validacio" if held_out else "entrenament"
        point = QgsPointXY(x, y)
        geometry = QgsGeometry.fromPointXY(point)
        attributes = [identity, code, len(records), partition]
        for record in records:
            correspondence.append([str(record["id_porpk"]), identity, str(record["cod_postal"]), partition])
        if held_out:
            if municipality.contains(geometry):
                validation_rows.append((attributes, geometry))
        else:
            wide_rows.append((attributes, geometry))
            if inner.contains(point):
                narrow_rows.append((attributes, geometry))
    require(len(narrow_rows) >= 3 and validation_rows, "Insufficient independent training/validation points")
    narrow = memory("Generadors", "Point", fields, narrow_rows)
    wide = memory("Entorn ampli", "Point", fields, wide_rows)
    save(context, narrow, "portals_generadors")
    save(context, wide, "generadors_entorn_ampli")
    table(context, "correspondencia_portals", ["id_porpk:string", "id_generador:string", "cod_postal_original:string", "particio:string"], correspondence)
    triangles = vector(run(context, "native:delaunaytriangulation", INPUT=narrow, TOLERANCE=0))
    identities = {(row[1].asPoint().x(), row[1].asPoint().y()): row[0][0] for row in narrow_rows}
    triangle_rows = []
    for feature in triangles.getFeatures():
        coordinates = list(feature.geometry().vertices())[:3]
        keys = [(point.x(), point.y()) for point in coordinates]
        require(all(key in identities for key in keys), "Delaunay vertex is not a retained generator")
        triangle_rows.append(([identities[key] for key in keys], feature.geometry()))
    save(context, memory("Delaunay", "Polygon", ["id_a:string", "id_b:string", "id_c:string"], triangle_rows), "delaunay_portals")
    municipality_layer = vector(data, "Municipi", "municipi_treball")
    for generators, name in ((narrow, "zones_cp_estimades"), (wide, "zones_cp_entorn_ampli")):
        cells = run(context, "native:voronoipolygons", INPUT=generators, BUFFER=100, TOLERANCE=0, COPY_ATTRIBUTES=True)
        clipped = run(context, "native:clip", INPUT=cells, OVERLAY=municipality_layer)
        if name == "zones_cp_estimades":
            save(context, clipped, "voronoi_portals")
        dissolved = run(context, "native:dissolve", INPUT=clipped, FIELD=["cod_postal"], SEPARATE_DISJOINT=False)
        # Keep categorical identity only: other attributes of one surviving
        # generator are not aggregate statistics for a dissolved postal zone.
        dissolved = vector(dissolved)
        rows = [([str(f["cod_postal"])], f.geometry()) for f in dissolved.getFeatures()]
        save(context, memory(name, "MultiPolygon", ["cod_postal:string"], rows), name)
    tree = cKDTree(np.array([(geometry.asPoint().x(), geometry.asPoint().y()) for _, geometry in narrow_rows]))
    test_xy = np.array([(geometry.asPoint().x(), geometry.asPoint().y()) for _, geometry in validation_rows])
    distances, indices = tree.query(test_xy, k=2)
    statistics = {}
    predictions = []
    for index, (attributes, geometry) in enumerate(validation_rows):
        tie = abs(float(distances[index, 0]) - float(distances[index, 1])) <= .000001
        predicted = "__empat__" if tie else narrow_rows[int(indices[index, 0])][0][1]
        code = attributes[1]
        evaluable = not code.startswith("__") and not predicted.startswith("__")
        correct = evaluable and code == predicted
        predictions.append((attributes + [predicted, int(evaluable), int(correct), float(distances[index, 0])], geometry))
        totals = statistics.setdefault(code, [0, 0, 0])
        totals[0] += 1
        totals[1] += int(evaluable)
        totals[2] += int(correct)
    save(context, memory("Validació", "Point", fields + ["codi_estimat:string", "avaluable:integer", "coincideix:integer", "distancia_m:double"], predictions), "portals_validacio")
    zones = {str(f["cod_postal"]): f.geometry() for f in vector(data, "Zones", "zones_cp_estimades").getFeatures()}
    expanded = {str(f["cod_postal"]): f.geometry() for f in vector(data, "Entorn ampli", "zones_cp_entorn_ampli").getFeatures()}
    rows, changes = [], []
    for code in sorted(set(zones) | set(expanded) | set(statistics)):
        first, second = zones.get(code), expanded.get(code)
        change = first.symDifference(second).area() if first is not None and second is not None else (first.area() if first is not None else second.area() if second is not None else 0)
        changes.append(change)
        total, evaluable, correct = statistics.get(code, [0, 0, 0])
        rows.append([code, total, evaluable, correct, correct / evaluable if evaluable else None, change])
    totals = [sum(values[index] for values in statistics.values()) for index in range(3)]
    rows.append(["__TOTAL__", *totals, totals[2] / totals[1] if totals[1] else None, sum(changes) / 2])
    table(context, "validacio_postal", ["codi:string", "n_ubicacions:integer", "n_avaluables:integer", "n_encerts:integer", "proporcio:double", "canvi_area_m2:double"], rows)


def verify_reus(context, check):
    from collections import Counter
    import numpy as np
    from scipy.spatial import cKDTree
    from qgis.core import QgsGeometry, QgsSpatialIndex, QgsPointXY
    data = context.output("resolved-data")
    initial = vector(context.output("initial-data"), "Originals", "portals_entorn")
    regional = vector(data, "Entorn", "portals_entorn")
    check("regional-preserved", signature(initial) == signature(regional))
    correspondence = list(vector(data, "Correspondència", "correspondencia_portals").getFeatures())
    check("original-portals-trace", {str(f["id_porpk"]) for f in correspondence} == {str(f["id_porpk"]) for f in regional.getFeatures()})
    check("correspondence-count", len(correspondence), regional.featureCount(), units="count")
    training = list(vector(data, "Generadors", "portals_generadors").getFeatures())
    validation = list(vector(data, "Validació", "portals_validacio").getFeatures())
    trained_ids = {str(f["id_generador"]) for f in training}
    held_ids = {str(f["id_generador"]) for f in validation}
    train_xy = [(f.geometry().asPoint().x(), f.geometry().asPoint().y()) for f in training]
    check("unique-generators", len(trained_ids) == len(training) == len(set(train_xy)))
    check("no-location-leakage", trained_ids.isdisjoint(held_ids))
    check("block-partition", all((math.floor(f.geometry().asPoint().x() / 500) + 2 * math.floor(f.geometry().asPoint().y() / 500)) % 5 != 0 for f in training)
                              and all((math.floor(f.geometry().asPoint().x() / 500) + 2 * math.floor(f.geometry().asPoint().y() / 500)) % 5 == 0 for f in validation))
    check("unique-source-partition", all(str(f["particio"]) == "entrenament" for f in correspondence if str(f["id_generador"]) in trained_ids)
                                     and all(str(f["particio"]) == "validacio" for f in correspondence if str(f["id_generador"]) in held_ids))
    triangles = list(vector(data, "Delaunay", "delaunay_portals").getFeatures())
    coordinates = set(train_xy)
    check("delaunay-source-vertices", all((v.x(), v.y()) in coordinates for f in triangles for v in f.geometry().vertices()))
    edges = Counter()
    for feature in triangles:
        ids = [str(feature[name]) for name in ("id_a", "id_b", "id_c")]
        for first, second in zip(ids, ids[1:] + ids[:1]):
            edges[tuple(sorted((first, second)))] += 1
    check("delaunay-manifold", set(edges.values()) <= {1, 2})
    hull = QgsGeometry.fromMultiPointXY([QgsPointXY(x, y) for x, y in train_xy]).convexHull()
    check("delaunay-hull-area", sum(f.geometry().area() for f in triangles), hull.area(), max(.01, hull.area() * 1e-10), "m2")
    municipality = one(vector(data, "Reus", "municipi_treball")).geometry()
    cells = list(vector(data, "Voronoi", "voronoi_portals").getFeatures())
    union = QgsGeometry.unaryUnion([f.geometry() for f in cells])
    require(not union.lastError(), "Voronoi union failed")
    check("voronoi-coverage", union.symDifference(municipality).area(), 0, .01, "m2")
    check("voronoi-disjoint-area", sum(f.geometry().area() for f in cells), union.area(), .01, "m2")
    for name in ("zones_cp_estimades", "zones_cp_entorn_ampli"):
        zones = list(vector(data, name, name).getFeatures())
        combined = QgsGeometry.unaryUnion([f.geometry() for f in zones])
        check(name + "-coverage", combined.symDifference(municipality).area(), 0, .01, "m2")
        check(name + "-disjoint", sum(f.geometry().area() for f in zones), combined.area(), .01, "m2")
    tree = cKDTree(np.array(train_xy))
    test_xy = np.array([(f.geometry().asPoint().x(), f.geometry().asPoint().y()) for f in validation])
    distances, indices = tree.query(test_xy, k=2)
    matching = 0
    for index, feature in enumerate(validation):
        tie = abs(float(distances[index, 0]) - float(distances[index, 1])) <= .000001
        predicted = "__empat__" if tie else str(training[int(indices[index, 0])]["cod_postal"])
        matching += predicted == str(feature["codi_estimat"])
    check("persisted-predictions", matching, len(validation), units="count")
    spatial = QgsSpatialIndex()
    by_id = {}
    for feature in cells:
        spatial.addFeature(feature)
        by_id[feature.id()] = feature
    compatible = 0
    for feature in validation:
        predicted = str(feature["codi_estimat"])
        if predicted == "__empat__":
            compatible += 1
            continue
        rectangle = feature.geometry().boundingBox()
        rectangle.grow(.001)
        compatible += any(str(by_id[identity]["cod_postal"]) == predicted and by_id[identity].geometry().distance(feature.geometry()) <= .001 for identity in spatial.intersects(rectangle))
    check("voronoi-nearest-independent", compatible, len(validation), units="count")
    totals = [f for f in vector(data, "Validació", "validacio_postal").getFeatures() if str(f["codi"]) == "__TOTAL__"]
    require(len(totals) == 1, "Missing validation summary")
    check("validation-summary-count", int(totals[0]["n_ubicacions"]), len(validation), units="count")
    check("validation-summary-correct", int(totals[0]["n_encerts"]), sum(int(f["coincideix"]) for f in validation), units="count")
