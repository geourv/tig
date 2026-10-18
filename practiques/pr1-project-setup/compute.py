"""PR1 selection/export and editable local map base; shared producer owns delivery."""

import csv
import hashlib
import math
from pathlib import Path
import shutil


INPUT_HASHES = {
    "municipis-source": "069f755f253f7af969e80403f6e81fa2cadefbd4c40ffd2f825f30e167bf2b2d",
    "cnig-source": "46aa316b88ec9f6eac559ca4f2037f1e142a997d3c0722febb8912a9a03654dd",
    "ortho-source": "8cfdb39b6fce124844644087bc39a365da9bcef6401286644590b60c4fd07ad0",
}
FONT_FILE = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_HASH = "ae7b7855e115a5966d8b1b3f80f254ccc117ec86f9965e202ee2940453837280"
PARAMETERS = {
    "municipality_code": "431711", "municipality_name": "Vila-seca",
    "catalogue_count": 947, "map_scale": 60000, "locator_scale": 400000,
}


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _hash(path):
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def _vector(path, name, table=None):
    from qgis.core import QgsVectorLayer
    uri = str(path) + ("|layername=" + table if table else "")
    layer = QgsVectorLayer(uri, name, "ogr")
    _require(layer.isValid(), "Invalid vector: " + name)
    return layer


def _one(layer):
    features = list(layer.getFeatures())
    _require(len(features) == 1, "Expected one feature in " + layer.name())
    return features[0]


def _save(context, source, product, table, append=False):
    return context.processing("native:savefeatures", {
        "INPUT": source, "OUTPUT": context.output(product), "LAYER_NAME": table,
        "ACTION_ON_EXISTING_FILE": 1 if append else 0,
        "DATASOURCE_OPTIONS": "", "LAYER_OPTIONS": "",
    })


def _source_table(context, product, resolved):
    from qgis.core import QgsFeature, QgsProject, QgsVectorFileWriter, QgsVectorLayer
    fields = ("id", "producte", "productor", "llicencia", "url", "sha256", "observacions")
    table = QgsVectorLayer("None?" + "&".join("field=" + field + ":string" for field in fields),
                           "Fonts de les dades", "memory")
    rows = [
        ["icgc-municipis", "Municipis 1:5.000 · 20/01/2026", "ICGC", "CC BY 4.0",
         "https://datacloud.icgc.cat/datacloud/divisions-administratives/fgb_unzip_EPSG25831/divisions-administratives-v2r2-municipis-5000-20260120.fgb",
         INPUT_HASHES["municipis-source"], "947 municipis; geometries i atributs conservats."],
        ["icgc-ortofoto", "Ortofoto Territorial 2025 · extracte local de context", "ICGC", "CC BY 4.0",
         "https://geoserveis.icgc.cat/servei/catalunya/orto-territorial/wms",
         INPUT_HASHES["ortho-source"], "Resposta WMS retinguda i georeferenciada; no és una descàrrega analítica a 25 cm ni cobertura de tot Catalunya."],
        ["dejavu", "DejaVu Sans", "DejaVu / Bitstream", "Llicència retinguda amb la font",
         "https://dejavu-fonts.github.io/License.html", FONT_HASH,
         "El text de copyright i permisos es conserva a data/fonts/DejaVuSans-licence.csv."],
    ]
    if resolved:
        rows.append(["cnig-municipi", "Unitat administrativa 1172246 · consulta 08/09/2026", "IGN/CNIG",
                     "CC BY 4.0 ign.es", "https://api-features.ign.es/collections/administrativeunit/items/1172246?f=json",
                     INPUT_HASHES["cnig-source"], "Només s’exporta el vector municipal; el projecte històric amb WMS es conserva a l’original."])
    for values in rows:
        feature = QgsFeature(table.fields())
        feature.setAttributes(values)
        _require(table.dataProvider().addFeatures([feature])[0], "Cannot create provenance row")
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "GPKG"
    options.layerName = "fonts_dades"
    options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer
    result = QgsVectorFileWriter.writeAsVectorFormatV3(
        table, context.output(product), QgsProject.instance().transformContext(), options)
    _require(result[0] == QgsVectorFileWriter.NoError, "Cannot save provenance: " + str(result))


def compute(context):
    from qgis.core import Qgis, QgsCoordinateReferenceSystem, QgsProject, QgsRasterLayer

    _require(context.parameters == PARAMETERS, "Unexpected PR1 parameters")
    for identity, expected in INPUT_HASHES.items():
        _require(_hash(context.input(identity)) == expected, "Reviewed input differs: " + identity)
    _require(_hash(FONT_FILE) == FONT_HASH, "The pinned font differs")

    shutil.copyfile(context.input("ortho-source"), context.output("local-orthophoto"))
    shutil.copyfile(FONT_FILE, context.output("font-regular"))
    licence = Path("/usr/share/doc/fonts-dejavu-core/copyright").read_text(encoding="utf-8")
    _require("Bitstream" in licence and "permission" in licence.lower(), "Missing font licence notice")
    with Path(context.output("font-licence")).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["component", "notice"])
        writer.writerow(["DejaVu Sans", licence])
    Path(context.output("font-licence-types")).write_text('"String","String"\n', encoding="utf-8")

    for product in ("initial-data", "resolved-data"):
        _save(context, context.input("municipis-source"), product, "municipis_icgc")

    selected = _vector(context.input("municipis-source"), "Selecció ICGC")
    _require(selected.setSubsetString('"CODIMUNI" = \'431711\''), "Cannot apply municipality filter")
    feature = _one(selected)
    _require(str(feature["NOMMUNI"]) == "Vila-seca", "Unexpected selected municipality")
    _save(context, selected.source(), "resolved-data", "municipi_treball", append=True)
    selected = None
    _save(context, context.input("cnig-source") + "|layername=municipi_treball",
          "resolved-data", "municipi_cnig", append=True)
    _source_table(context, "initial-data", False)
    _source_table(context, "resolved-data", True)

    products = {key: str(value) for key, value in context.outputs.items()}
    for identity, product, stored_name in (
        ("initial-project", "initial-data", "inicial"),
        ("resolved-project", "resolved-data", "pr1"),
        ("resolved-project", "resolved-data", "comparacio"),
    ):
        project = QgsProject()
        project.setCrs(QgsCoordinateReferenceSystem("EPSG:25831"))
        project.setEllipsoid("GRS80")
        project.setFilePathStorage(Qgis.FilePathType.Relative)
        raster = QgsRasterLayer(context.output("local-orthophoto"), "Ortofoto local 2025", "gdal")
        _require(raster.isValid(), "Invalid local orthophoto")
        project.addMapLayer(raster)
        project.addMapLayer(_vector(context.output(product), "Municipis ICGC", "municipis_icgc"))
        if identity == "resolved-project":
            project.addMapLayer(_vector(context.output(product), "Municipi CNIG", "municipi_cnig"))
            project.addMapLayer(_vector(context.output(product), "Municipi de treball", "municipi_treball"))
        compose(project, identity, context.parameters, products)
        if stored_name == "comparacio":
            project.setTitle("Vila-seca · comparació de fonts ICGC/CNIG")
        context.embed_project(product, stored_name, project)
        project.clear()
        raster = None


def verify(context):
    """Reopen outputs and compare independently by identity, attributes and geometry."""
    from osgeo import gdal
    from qgis.core import QgsWkbTypes

    _require(context.parameters == PARAMETERS, "Unexpected verification parameters")
    source = _vector(context.input("municipis-source"), "Font ICGC")
    original = {str(feature["CODIMUNI"]): feature for feature in source.getFeatures()}
    _require(len(original) == PARAMETERS["catalogue_count"], "Source IDs are not unique/complete")
    by_name = [feature for feature in original.values() if str(feature["NOMMUNI"]) == "Vila-seca"]
    _require(len(by_name) == 1, "Independent name lookup is not unique")
    expected = by_name[0]
    field_names = [field.name() for field in source.fields()]
    checks = []

    def check(identity, actual, wanted, tolerance=0, units="count"):
        checks.append(dict(id=identity, actual=float(actual), expected=float(wanted),
                           tolerance=float(tolerance), units=units))

    for product in ("initial-data", "resolved-data"):
        catalogue = _vector(context.output(product), product, "municipis_icgc")
        rows = {str(feature["CODIMUNI"]): feature for feature in catalogue.getFeatures()}
        check(product + "-count", sum(1 for _ in catalogue.getFeatures()), 947)
        check(product + "-ids", int(set(rows) == set(original)), 1, units="boolean")
        check(product + "-crs", int(catalogue.crs().authid() == "EPSG:25831"), 1, units="boolean")
        equal_attributes = equal_geometries = valid_geometries = 0
        for key, feature in rows.items():
            if key not in original:
                continue
            equal_attributes += all(feature[name] == original[key][name] for name in field_names)
            geometry = feature.geometry()
            equal_geometries += geometry.isGeosEqual(original[key].geometry())
            valid_geometries += not geometry.isEmpty() and geometry.isGeosValid()
        check(product + "-attributes", equal_attributes, 947)
        check(product + "-geometries", equal_geometries, 947)
        check(product + "-valid", valid_geometries, 947)
        metadata = _vector(context.output(product), "Fonts", "fonts_dades")
        check(product + "-provenance", metadata.featureCount(), 3 if product == "initial-data" else 4)

    municipal = _vector(context.output("resolved-data"), "Municipi", "municipi_treball")
    result = _one(municipal)
    geometry = result.geometry()
    check("municipality-count", municipal.featureCount(), 1)
    check("municipality-code", int(str(result["CODIMUNI"]) == "431711"), 1, units="boolean")
    check("municipality-name", int(str(result["NOMMUNI"]) == "Vila-seca"), 1, units="boolean")
    check("municipality-crs", int(municipal.crs().authid() == "EPSG:25831"), 1, units="boolean")
    check("municipality-geometry", int(geometry.isGeosEqual(expected.geometry())), 1, units="boolean")
    check("municipality-attributes", int(all(result[name] == expected[name] for name in field_names)), 1, units="boolean")
    check("municipality-valid", int(not geometry.isEmpty() and geometry.isGeosValid()), 1, units="boolean")
    check("municipality-polygon", int(geometry.type() == QgsWkbTypes.PolygonGeometry), 1, units="boolean")
    _require(math.isfinite(geometry.area()) and geometry.area() > 0, "Invalid municipality area")
    check("municipality-area", geometry.area(), expected.geometry().area(), .000001, "m2")

    cnig_source = _vector(context.input("cnig-source"), "Font CNIG", "municipi_treball")
    cnig = _vector(context.output("resolved-data"), "CNIG", "municipi_cnig")
    a, b = _one(cnig_source), _one(cnig)
    check("cnig-count", cnig.featureCount(), 1)
    check("cnig-crs", int(cnig.crs().authid() == "EPSG:25831"), 1, units="boolean")
    check("cnig-identity", int(str(b["nom_muni"]) == "Vila-seca" and str(b["codi_muni"]) == "43171"), 1, units="boolean")
    check("cnig-attributes", int(all(a[field.name()] == b[field.name()] for field in cnig_source.fields())), 1, units="boolean")
    check("cnig-geometry", int(a.geometry().isGeosEqual(b.geometry())), 1, units="boolean")
    raster = gdal.Open(context.output("local-orthophoto"), gdal.GA_ReadOnly)
    _require(raster is not None, "Cannot reopen local raster")
    check("ortho-bands", raster.RasterCount, 3)
    check("ortho-bytes", int(_hash(context.output("local-orthophoto")) == INPUT_HASHES["ortho-source"]), 1, units="boolean")
    check("font-bytes", int(_hash(context.output("font-regular")) == FONT_HASH), 1, units="boolean")
    with Path(context.output("font-licence")).open(encoding="utf-8", newline="") as stream:
        licences = list(csv.DictReader(stream))
    check("font-licence", int(len(licences) == 1 and "Bitstream" in licences[0]["notice"]), 1, units="boolean")
    for identity, wanted in INPUT_HASHES.items():
        check(identity + "-preserved", int(_hash(context.input(identity)) == wanted), 1, units="boolean")
    return checks


def compose(project, project_id, parameters, products):
    """Author cartography only; native inspection, saving and exports stay shared."""
    from qgis.core import (QgsFeatureRequest, QgsFillSymbol, QgsLayoutItemLabel,
                          QgsLayoutItemMap, QgsLayoutPoint, QgsLayoutSize,
                          QgsMapThemeCollection, QgsPalLayerSettings, QgsPrintLayout,
                          QgsRectangle, QgsReferencedRectangle, QgsTextFormat,
                          QgsVectorLayerSimpleLabeling)
    from qgis.PyQt.QtGui import QColor, QFont

    _require(parameters == PARAMETERS, "Unexpected presentation parameters")
    resolved = project_id == "resolved-project"
    layers = {layer.name(): layer for layer in project.mapLayers().values()}
    catalogue, ortho = layers["Municipis ICGC"], layers["Ortofoto local 2025"]
    text = QgsTextFormat()
    text.setFont(QFont("DejaVu Sans"))
    text.setSize(9)
    project.styleSettings().setDefaultTextFormat(text)

    def style(layer, field, colour, width, size):
        layer.renderer().setSymbol(QgsFillSymbol.createSimple({
            "color": "255,255,255,0", "outline_color": colour,
            "outline_width": str(width), "outline_width_unit": "MM",
        }))
        if field:
            labels = QgsPalLayerSettings()
            labels.fieldName = field
            label_format = QgsTextFormat(text)
            label_format.setSize(size)
            label_format.setColor(QColor("#202020"))
            labels.setFormat(label_format)
            layer.setLabeling(QgsVectorLayerSimpleLabeling(labels))
            layer.setLabelsEnabled(True)
        else:
            layer.setLabelsEnabled(False)

    style(catalogue, "NOMMUNI", "#666666", .22, 8)
    main_layers = [catalogue, ortho]
    reference_layers = [catalogue]
    if resolved:
        municipal, cnig = layers["Municipi de treball"], layers["Municipi CNIG"]
        style(municipal, "NOMMUNI", "#a50f7f", .65, 11)
        style(cnig, None, "#2166ac", .35, 9)
        main_layers = [municipal, cnig, ortho]
        reference_layers = [municipal, catalogue]
    for layer in project.mapLayers().values():
        project.layerTreeRoot().findLayer(layer.id()).setItemVisibilityChecked(layer in main_layers)
    feature = next(catalogue.getFeatures(QgsFeatureRequest().setFilterExpression('"CODIMUNI" = \'431711\'')))
    extent = QgsRectangle(feature.geometry().boundingBox())
    extent.scale(1.2)
    project.viewSettings().setDefaultViewExtent(QgsReferencedRectangle(extent, project.crs()))
    project.setTitle("PR1 · Vila-seca · " + ("selecció resolta" if resolved else "municipis inicials"))
    for name, selected in (("Principal", main_layers), ("Localitzador", reference_layers)):
        record = QgsMapThemeCollection.MapThemeRecord()
        for layer in selected:
            entry = QgsMapThemeCollection.MapThemeLayerRecord(layer)
            entry.isVisible = True
            record.addLayerRecord(entry)
        project.mapThemeCollection().insert(name, record)
    if not resolved:
        return

    for old in list(project.layoutManager().layouts()):
        project.layoutManager().removeLayout(old)
    layout = QgsPrintLayout(project)
    layout.initializeDefaults()
    layout.setName("Base municipal")
    layout.pageCollection().pages()[0].setPageSize(QgsLayoutSize(297, 210))

    def label(identity, text_value, x, y, w, h, size=9, colour="#202020"):
        item = QgsLayoutItemLabel(layout)
        layout.addLayoutItem(item)
        item.setId(identity)
        item.setText(text_value)
        item.setFont(QFont("DejaVu Sans", size))
        item.setFontColor(QColor(colour))
        item.attemptMove(QgsLayoutPoint(x, y))
        item.attemptResize(QgsLayoutSize(w, h))

    label("titol", "Vila-seca · projecte municipal", 10, 6, 277, 12, 16)
    label("subtitol", "Base editable de composició · PR1 · EPSG:25831", 10, 20, 277, 8, 10)
    for identity, x, y, w, h, scale, theme, selected in (
        ("principal", 10, 35, 190, 150, parameters["map_scale"], "Principal", main_layers),
        ("localitzador", 212, 35, 75, 60, parameters["locator_scale"], "Localitzador", reference_layers),
    ):
        frame = QgsLayoutItemMap(layout)
        layout.addLayoutItem(frame)
        frame.setId(identity)
        frame.attemptMove(QgsLayoutPoint(x, y))
        frame.attemptResize(QgsLayoutSize(w, h))
        frame.setCrs(project.crs())
        frame.setLayers(selected)
        frame.setFollowVisibilityPreset(True)
        frame.setFollowVisibilityPresetName(theme)
        frame.zoomToExtent(extent)
        frame.setScale(scale)
    label("icgc", "Contorn magenta: municipi ICGC", 212, 102, 75, 10, 9, "#a50f7f")
    label("cnig", "Contorn blau: municipi CNIG", 212, 114, 75, 10, 9, "#2166ac")
    label("escala", "Mapa principal 1:60.000\nLocalitzador 1:400.000\nNord a la part superior", 212, 128, 75, 30, 9)
    label("abast", "Base de treball: completar llegenda\ni escala gràfica a QGIS.", 212, 164, 75, 20, 9)
    label("fonts", "Fonts: municipis i ortofoto ICGC (CC BY 4.0); límit IGN/CNIG (CC BY 4.0 ign.es).", 10, 190, 277, 8, 8)
    label("nota", "Ortofoto: extracte local de context de 2025. Cas de demostració; autoria docent TIG, URV.", 10, 199, 277, 8, 8)
    project.layoutManager().addLayout(layout)
