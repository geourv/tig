"""CNIG ROI teaching case. The shared producer owns execution and sealed bundles.

`prepare` only retains declared author inputs in a new ignored staging directory.
`compute` and `verify` run in the pinned QGIS worker through practice-run.
"""

import csv
import hashlib
import json
import math
from pathlib import Path
import shutil
import tempfile
import zipfile


FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_SHA = "ae7b7855e115a5966d8b1b3f80f254ccc117ec86f9965e202ee2940453837280"
INITIAL = ["municipi_treball", "termes_candidats", "portals_candidats", "vies_candidats", "illes_candidates"]
DERIVED = [
    "municipi_caixa", "municipi_rectangle_orientat", "municipi_cercle_minim", "municipi_convexa",
    "municipi_buffer_500m", "roi", "rectangle_orientat", "envolupant_convexa", "cercle_minim",
    "termes_roi", "terra_roi", "mar_complement", "mar_context", "portals_roi", "viari_roi", "illes_roi",
    "urbans_roi", "buffer_carrers_5m", "buffer_carrers_10m", "peces_carrers_5m", "peces_carrers_10m",
    "peces_individuals_5m", "peces_individuals_10m", "centroides_illes", "centroides_linies",
    "punts_superficie_illes", "vertices_illes", "vertices_linies", "extrems_linies",
]


def require(value, message):
    if not value:
        raise ValueError(message)


def digest(path):
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def vector(path, name):
    from qgis.core import QgsVectorLayer
    layer = QgsVectorLayer(str(path) + "|layername=" + name, name, "ogr")
    require(layer.isValid(), "Invalid layer: " + name)
    return layer


def run(context, algorithm, **parameters):
    return context.processing(algorithm, dict(parameters, OUTPUT="TEMPORARY_OUTPUT"))["OUTPUT"]


def save(context, layer, name, product="resolved-data"):
    if layer.fields().indexFromName("fid") >= 0:
        layer = run(context, "native:deletecolumn", INPUT=layer, COLUMN=["fid"])
    context.processing("native:savefeatures", dict(
        INPUT=layer, OUTPUT=context.output(product), LAYER_NAME=name,
        ACTION_ON_EXISTING_FILE=1 if Path(context.output(product)).exists() else 0,
        DATASOURCE_OPTIONS="", LAYER_OPTIONS=""))


def one(layer):
    rows = list(layer.getFeatures())
    require(len(rows) == 1, "Expected one feature: " + layer.name())
    return rows[0].geometry()


def memory(name, geometry, fields, rows):
    from qgis.core import QgsFeature, QgsVectorLayer
    layer = QgsVectorLayer(geometry + "?crs=EPSG:25831&" + "&".join("field=" + f for f in fields), name, "memory")
    features = []
    for attributes, geom in rows:
        feature = QgsFeature(layer.fields())
        feature.setAttributes(attributes)
        if geom is not None:
            feature.setGeometry(geom)
        features.append(feature)
    require(layer.dataProvider().addFeatures(features)[0], "Cannot populate " + name)
    layer.updateExtents()
    return layer


def limits(path, directory):
    from qgis.core import QgsVectorLayer
    stem = "recintos_municipales_inspire_peninbal_etrs89"
    with zipfile.ZipFile(path) as archive:
        for suffix in (".shp", ".shx", ".dbf", ".prj", ".cpg"):
            Path(directory, stem + suffix).write_bytes(archive.read(f"SHP_ETRS89/{stem}/{stem}{suffix}"))
    layer = QgsVectorLayer(str(Path(directory, stem + ".shp")), "Recintes CNIG", "ogr")
    require(layer.isValid(), "Invalid municipal catalogue")
    return layer


def candidates(source, roi):
    """Conservative source-CRS bbox, stable source FID, then explicit reprojection.

    This is a preparation, not an exact intersection. Whole features are retained.
    """
    from qgis.core import (QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsFeature,
                           QgsFeatureRequest, QgsField, QgsGeometry, QgsProject, QgsVectorLayer, QgsWkbTypes)
    from qgis.PyQt.QtCore import QVariant
    target = QgsCoordinateReferenceSystem("EPSG:25831")
    forward = QgsCoordinateTransform(source.crs(), target, QgsProject.instance())
    reverse = QgsCoordinateTransform(target, source.crs(), QgsProject.instance())
    box = roi.boundingBox()
    box.grow(1.0)
    request = QgsFeatureRequest().setFilterRect(reverse.transformBoundingBox(box))
    result = QgsVectorLayer(QgsWkbTypes.displayString(source.wkbType()) + "?crs=EPSG:25831", source.name(), "memory")
    require(source.fields().indexFromName("id_font") < 0, "Source already has id_font")
    fields = list(source.fields()) + [QgsField("id_font", QVariant.String)]
    result.dataProvider().addAttributes(fields)
    result.updateFields()
    rows = []
    for original in source.getFeatures(request):
        feature = QgsFeature(result.fields())
        feature.setAttributes(original.attributes() + [str(original.id())])
        geometry = QgsGeometry(original.geometry())
        geometry.transform(forward)
        feature.setGeometry(geometry)
        rows.append(feature)
    require(result.dataProvider().addFeatures(rows)[0] and rows, "No usable candidates")
    result.updateExtents()
    return result


def buffer(context, source, distance, dissolve=False):
    return run(context, "native:buffer", INPUT=source, DISTANCE=distance, SEGMENTS=8,
               END_CAP_STYLE=0, JOIN_STYLE=0, MITER_LIMIT=2, DISSOLVE=dissolve, SEPARATE_DISJOINT=False)


def compute(context):
    from qgis.core import QgsFeatureRequest, QgsGeometry, QgsPointXY
    for item in context.parameters["sources"]:
        require(digest(context.input(item["id"])) == item["sha256"], "Changed original " + item["id"])
    require(digest(FONT) == FONT_SHA, "Changed font")
    shutil.copyfile(FONT, context.output("font-regular"))
    with Path(context.output("font-licence")).open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["component", "notice"])
        writer.writerow(["DejaVu Sans", Path("/usr/share/doc/fonts-dejavu-core/copyright").read_text()])
    Path(context.output("font-licence-types")).write_text('"String","String"\n')
    with tempfile.TemporaryDirectory(prefix="tig-roi-") as temporary:
        catalogue = limits(context.input("limits-original"), temporary)
        municipality = catalogue.materialize(QgsFeatureRequest().setFilterExpression('"NATCODE" = \'34094343171\''))
        require(municipality.featureCount() == 1, "Municipal identity is not unique")
        require(next(municipality.getFeatures())["NAMEUNIT"] == "Vila-seca", "Wrong municipality")
        municipality = run(context, "native:reprojectlayer", INPUT=municipality, TARGET_CRS="EPSG:25831")
        municipal_buffer = buffer(context, municipality, 500)
        roi = run(context, "native:boundingboxes", INPUT=municipal_buffer)
        roi = run(context, "native:fieldcalculator", INPUT=roi, FIELD_NAME="id_roi", FIELD_TYPE=2,
                  FIELD_LENGTH=24, FIELD_PRECISION=0, FORMULA="'roi_vilaseca_500m'")
        geometrical_roi = one(roi)
        initial = {
            "municipi_treball": municipality,
            "termes_candidats": candidates(catalogue, geometrical_roi),
            "portals_candidats": candidates(vector(context.input("cartociudad"), "portalpk_publi"), geometrical_roi),
            "vies_candidats": candidates(vector(context.input("transport"), "rt_tramo_vial"), geometrical_roi),
            "illes_candidates": candidates(vector(context.input("cartociudad"), "manzana"), geometrical_roi),
        }
        for name, layer in initial.items():
            for product in ("initial-data", "resolved-data"):
                save(context, layer, name, product)
    save(context, municipal_buffer, "municipi_buffer_500m")
    save(context, roi, "roi")
    for geometry_type, name in enumerate(("municipi_caixa", "municipi_rectangle_orientat", "municipi_cercle_minim", "municipi_convexa")):
        save(context, run(context, "qgis:minimumboundinggeometry", INPUT=municipality, FIELD=None, TYPE=geometry_type), name)
    for algorithm, name in (("native:orientedminimumboundingbox", "rectangle_orientat"),
                            ("native:convexhull", "envolupant_convexa"),
                            ("native:minimumenclosingcircle", "cercle_minim")):
        kwargs = {"SEGMENTS": 720} if name == "cercle_minim" else {}
        save(context, run(context, algorithm, INPUT=municipal_buffer, **kwargs), name)
    data = context.output("resolved-data")
    portals = vector(data, "portals_candidats")
    require(portals.setSubsetString('"tipo" = \'Portal\''), "Portal filter failed")
    save(context, run(context, "native:clip", INPUT=portals, OVERLAY=roi), "portals_roi")
    for original, result, algorithm in (
        ("vies_candidats", "viari_roi", "native:clip"),
        ("illes_candidates", "illes_roi", "native:intersection"),
        ("termes_candidats", "termes_roi", "native:clip"),
    ):
        parameters = {"OVERLAY_FIELDS": ["id_roi"]} if algorithm == "native:intersection" else {}
        save(context, run(context, algorithm, INPUT=vector(data, original), OVERLAY=roi, **parameters), result)
    land = run(context, "native:dissolve", INPUT=vector(data, "termes_roi"), FIELD=[], SEPARATE_DISJOINT=False)
    save(context, land, "terra_roi")
    complement = run(context, "native:difference", INPUT=roi, OVERLAY=land)
    save(context, complement, "mar_complement")
    parts = list(run(context, "native:multiparttosingleparts", INPUT=complement).getFeatures())
    require(parts, "No marine-context candidate")
    box = geometrical_roi.boundingBox()
    witnesses = [QgsGeometry.fromPointXY(QgsPointXY(x, box.yMinimum() + 1))
                 for x in (box.xMinimum() + 1, box.xMaximum() - 1)]
    marine_parts = [f.geometry() for f in parts if any(f.geometry().contains(p) for p in witnesses)]
    marine = QgsGeometry.unaryUnion(marine_parts)
    require(all(marine.contains(p) for p in witnesses), "Marine reference points require geographical review")
    marine.convertToMultiType()
    save(context, memory("mar_context", "MultiPolygon", ["criteri:string"],
         [(["components_amb_referencies_marines_sud_oest_i_sud_est; context_derivat"], marine)]), "mar_context")
    streets = vector(data, "viari_roi")
    require(streets.setSubsetString('"clased" = \'Urbano\''), "Urban-road filter failed")
    save(context, streets, "urbans_roi")
    for distance in (5, 10):
        corridor = buffer(context, streets, distance, dissolve=True)
        save(context, corridor, f"buffer_carrers_{distance}m")
        pieces = run(context, "native:difference", INPUT=land, OVERLAY=corridor)
        pieces = run(context, "native:fieldcalculator", INPUT=pieces, FIELD_NAME="id_origen", FIELD_TYPE=2,
                     FIELD_LENGTH=32, FIELD_PRECISION=0, FORMULA=f"'terra_menys_carrers_{distance}m'")
        save(context, pieces, f"peces_carrers_{distance}m")
        single = run(context, "native:multiparttosingleparts", INPUT=pieces)
        single = run(context, "native:fieldcalculator", INPUT=single, FIELD_NAME="id_peca", FIELD_TYPE=1,
                     FIELD_LENGTH=10, FIELD_PRECISION=0, FORMULA="$id + 1")
        single = run(context, "native:fieldcalculator", INPUT=single, FIELD_NAME="area_m2", FIELD_TYPE=0,
                     FIELD_LENGTH=20, FIELD_PRECISION=6, FORMULA="area($geometry)")
        save(context, single, f"peces_individuals_{distance}m")
    blocks = vector(data, "illes_roi")
    lines = vector(data, "urbans_roi")
    for source, algorithm, name, parameters in (
        (blocks, "native:centroids", "centroides_illes", {"ALL_PARTS": False}),
        (lines, "native:centroids", "centroides_linies", {"ALL_PARTS": False}),
        (blocks, "native:pointonsurface", "punts_superficie_illes", {"ALL_PARTS": False}),
        (blocks, "native:extractvertices", "vertices_illes", {}),
        (lines, "native:extractvertices", "vertices_linies", {}),
        (lines, "native:extractspecificvertices", "extrems_linies", {"VERTICES": "0,-1"}),
    ):
        save(context, run(context, algorithm, INPUT=source, **parameters), name)
    for product in ("initial-data", "resolved-data"):
        rows = [([s["id"], s["repository_path"], s["sha256"], "IGN/CNIG; CC BY 4.0"], None)
                for s in context.parameters["sources"]]
        save(context, memory("fonts_dades", "None", ["id:string", "origen:string", "sha256:string", "credit:string"], rows),
             "fonts_dades", product)
    rows = []
    for name in INITIAL + DERIVED:
        layer = vector(data, name)
        dimension = layer.geometryType()
        measure = sum(f.geometry().area() if dimension == 2 else f.geometry().length() if dimension == 1 else 1
                      for f in layer.getFeatures())
        rows.append(([name, layer.featureCount(), measure, "m2" if dimension == 2 else "m" if dimension == 1 else "count"], None))
    save(context, memory("resum_resultats", "None", ["capa:string", "n_entitats:integer", "mesura:double", "unitat:string"], rows), "resum_resultats")
    author_projects(context)


def author_projects(context):
    from qgis.core import Qgis, QgsCoordinateReferenceSystem, QgsProject
    for identity, product, stored, names in (
        ("initial-project", "initial-data", "inicial", INITIAL),
        ("resolved-project", "resolved-data", "pr4_roi", INITIAL + DERIVED),
    ):
        project = QgsProject()
        project.setCrs(QgsCoordinateReferenceSystem("EPSG:25831"))
        project.setEllipsoid("GRS80")
        project.setFilePathStorage(Qgis.FilePathType.Relative)
        for name in names + ["fonts_dades"]:
            project.addMapLayer(vector(context.output(product), name))
        compose(project, identity, context.parameters, context.outputs)
        context.embed_project(product, stored, project)
        project.clear()


def compose(project, project_id, parameters, products):
    if project_id == "capture-online":
        compose_capture(project, parameters, products)
        return
    from qgis.core import (QgsFillSymbol, QgsLineSymbol, QgsMarkerSymbol, QgsRectangle,
                           QgsReferencedRectangle, QgsSingleSymbolRenderer, QgsTextFormat)
    from qgis.PyQt.QtGui import QFont
    text = QgsTextFormat()
    text.setFont(QFont("DejaVu Sans"))
    text.setSize(10)
    project.styleSettings().setDefaultTextFormat(text)
    layers = {layer.name(): layer for layer in project.mapLayers().values()}
    colours = {"roi": "#277a52", "municipi_treball": "#96315e", "municipi_buffer_500m": "#346eab",
               "mar_context": "#a7cfe6", "terra_roi": "#eee9de"}
    for name, layer in layers.items():
        if name == "fonts_dades":
            continue
        colour = colours.get(name, "#a37736" if "illes" in name or "peces" in name else "#346eab")
        if layer.geometryType() == 2:
            fill = colour if name in {"mar_context", "terra_roi", "illes_roi"} or "peces_individuals" in name else "255,255,255,0"
            symbol = QgsFillSymbol.createSimple({"color": fill, "outline_color": colour, "outline_width": "0.35"})
        elif layer.geometryType() == 1:
            symbol = QgsLineSymbol.createSimple({"line_color": colour, "line_width": "0.3"})
        else:
            symbol = QgsMarkerSymbol.createSimple({"name": "circle", "color": colour, "size": "1.4", "outline_style": "no"})
        layer.setRenderer(QgsSingleSymbolRenderer(symbol))
        layer.setLabelsEnabled(False)
    visible = {"municipi_treball", "roi", "municipi_buffer_500m"}
    for name, layer in layers.items():
        node = project.layerTreeRoot().findLayer(layer.id())
        node.setItemVisibilityChecked(name in visible)
        node.setExpanded(False)
    extent = QgsRectangle(layers.get("roi", layers["municipi_treball"]).extent())
    extent.scale(1.15)
    project.viewSettings().setDefaultViewExtent(QgsReferencedRectangle(extent, project.crs()))
    project.setTitle("Vila-seca · ROI CNIG · cas docent de revisió")


def compose_capture(project, parameters, products):
    """Live cartographic context through the public native composition callback.

    This scene opens the verified local project and adds an actual WMS layer.
    It is used for screenshots, without saving an offline native checkpoint or
    changing the sealed scientific project. The URL/layer are explicit recipe
    parameters; the shared renderer still owns GUI execution and image capture.
    """
    from qgis.core import (QgsDataSourceUri, QgsFillSymbol, QgsLineSymbol, QgsMarkerSymbol,
                           QgsRasterLayer, QgsSimpleFillSymbolLayer, QgsSingleSymbolRenderer, QgsVectorLayer)
    from qgis.PyQt.QtCore import Qt
    root = project.layerTreeRoot()
    originals = root.insertGroup(1, "Originals CNIG · capes disponibles")
    for identity, table, name in (
        ("cartociudad", "portalpk_publi", "CartoCiudad · portals i PK"),
        ("cartociudad", "manzana", "CartoCiudad · illes"),
        ("transport", "rt_tramo_vial", "CNIG · trams viaris"),
    ):
        layer = vector(products[identity], table)
        layer.setName(name)
        project.addMapLayer(layer, False)
        node = originals.addLayer(layer)
        node.setItemVisibilityChecked(False)
        node.setExpanded(False)
    originals.setExpanded(False)
    declaration = parameters["wms"]
    uri = QgsDataSourceUri()
    for key, value in declaration.items():
        if key != "name":
            uri.setParam(key, value)
    ortho = QgsRasterLayer(bytes(uri.encodedUri()).decode("utf-8"), declaration["name"], "wms")
    require(ortho.isValid(), "IGN/PNOA WMS could not be loaded")
    project.addMapLayer(ortho, False)
    background = root.addGroup("Context · servei WMS")
    background.addLayer(ortho).setExpanded(False)
    background.setExpanded(True)
    for name, colour in (("roi", "#00a86b"), ("municipi_treball", "#d12b7c"), ("municipi_buffer_500m", "#178fe0"),
                         ("municipi_caixa", "#00a86b"), ("municipi_rectangle_orientat", "#178fe0"),
                         ("municipi_cercle_minim", "#e39a00"), ("municipi_convexa", "#9b40c5")):
        layer = project.mapLayersByName(name)[0]
        symbol = QgsFillSymbol.createSimple({"color": "255,255,255,0", "outline_color": "#ffffff", "outline_width": "0.85"})
        overlay = QgsFillSymbol.createSimple({"color": "255,255,255,0", "outline_color": colour, "outline_width": "0.45"})
        symbol.appendSymbolLayer(overlay.takeSymbolLayer(0))
        layer.setRenderer(QgsSingleSymbolRenderer(symbol))
    for name, colour, shape, size in (
        ("portals_roi", "#ffe45c", "circle", ".7"),
        ("vertices_illes", "#177cba", "circle", ".9"),
        ("centroides_illes", "#d7191c", "triangle", "2.6"),
        ("punts_superficie_illes", "#00a65a", "diamond", "1.8"),
    ):
        layer = project.mapLayersByName(name)[0]
        layer.setRenderer(QgsSingleSymbolRenderer(QgsMarkerSymbol.createSimple(
            {"name": shape, "color": colour, "size": size, "outline_color": "#ffffff", "outline_width": ".12"})))
    project.mapLayersByName("viari_roi")[0].setRenderer(QgsSingleSymbolRenderer(
        QgsLineSymbol.createSimple({"line_color": "#d73027", "line_width": ".23"})))
    project.mapLayersByName("illes_roi")[0].setRenderer(QgsSingleSymbolRenderer(
        QgsFillSymbol.createSimple({"color": "255,255,255,0", "outline_color": "#f2c94c", "outline_width": ".4"})))
    # The live orthophoto is a visual reference: polygon interiors must not tint it.
    for layer in project.mapLayers().values():
        if isinstance(layer, QgsVectorLayer) and layer.geometryType() == 2:
            symbol = layer.renderer().symbol()
            for part in symbol.symbolLayers():
                if isinstance(part, QgsSimpleFillSymbolLayer):
                    part.setBrushStyle(Qt.NoBrush)
    project.setTitle("Vila-seca · ROI CNIG i context IGN/PNOA")


def verify(context):
    """Independent checks on reopened data, original identities and geometric invariants."""
    from qgis.core import (QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsFeatureRequest,
                           QgsGeometry, QgsPointXY, QgsProject)
    checks = []

    def check(name, actual, expected=1, tolerance=0, units="boolean"):
        checks.append(dict(id=name, actual=float(actual), expected=float(expected), tolerance=float(tolerance), units=units))

    data = context.output("resolved-data")
    layers = {name: vector(data, name) for name in INITIAL + DERIVED}
    for name, layer in layers.items():
        features = list(layer.getFeatures())
        check(name + "-valid", bool(features) and all(f.geometry().isGeosValid() and not f.geometry().isEmpty() for f in features))
        check(name + "-crs", layer.crs().authid() == "EPSG:25831")
    for item in context.parameters["sources"]:
        check("original-" + item["id"], digest(context.input(item["id"])) == item["sha256"])
    check("font-hash", digest(context.output("font-regular")) == FONT_SHA)
    roi = one(layers["roi"])
    mun = one(layers["municipi_treball"])
    buf = one(layers["municipi_buffer_500m"])
    check("municipal-box-extents", one(layers["municipi_caixa"]).symDifference(QgsGeometry.fromRect(mun.boundingBox())).area(), 0, .001, "m2")
    for name in ("municipi_rectangle_orientat", "municipi_convexa", "municipi_cercle_minim"):
        envelope = one(layers[name])
        tolerance = .001
        if name == "municipi_cercle_minim":
            segments = len(list(envelope.vertices())) - 1
            radius = float(next(layers[name].getFeatures())["radius"])
            tolerance += radius * (1 - math.cos(math.pi / segments))
        check(name + "-covers", mun.difference(envelope.buffer(tolerance, 16)).area(), 0, .01, "m2")
    check("municipality-code", next(layers["municipi_treball"].getFeatures())["NATCODE"] == "34094343171")
    check("roi-box", roi.symDifference(QgsGeometry.fromRect(buf.boundingBox())).area(), 0, .001, "m2")
    check("buffer-contains-municipality", mun.difference(buf).area(), 0, .001, "m2")
    check("buffer-expands", buf.area() > mun.area())
    boundary = QgsGeometry(buf.constGet().boundary())
    sampled = [QgsGeometry.fromPointXY(QgsPointXY(p)) for p in buf.vertices()]
    sampled += [boundary.interpolate(d) for d in range(0, math.ceil(boundary.length()), 25)]
    distances = [mun.distance(point) for point in sampled]
    # GEOS partial fillets round the segment count, unlike a regular 32-gon.
    # The derivation is retained in the earlier geos-validation.md; this is a
    # sampled check of this new source, not a claim of a continuous certificate.
    lower = 500 * math.cos(3 * math.pi / (8 * 8)) - .01
    check("buffer-sampled-distance", all(lower <= d <= 500.01 for d in distances))
    check("buffer-sampled-maximum", max(distances), 500, .01, "m")
    for name in ("rectangle_orientat", "envolupant_convexa", "cercle_minim"):
        envelope = one(layers[name])
        check(name + "-encloses", buf.difference(envelope.buffer(.1, 8)).area(), 0, .001, "m2")
    originals = [("portals_candidats", "cartociudad", "portalpk_publi"),
                 ("vies_candidats", "transport", "rt_tramo_vial"), ("illes_candidates", "cartociudad", "manzana")]
    with tempfile.TemporaryDirectory(prefix="tig-roi-check-") as temporary:
        catalogue = limits(context.input("limits-original"), temporary)
        sources = [("termes_candidats", catalogue)] + [(name, vector(context.input(identity), table)) for name, identity, table in originals]
        for name, source in sources:
            target = QgsCoordinateReferenceSystem("EPSG:25831")
            forward = QgsCoordinateTransform(source.crs(), target, QgsProject.instance())
            reverse = QgsCoordinateTransform(target, source.crs(), QgsProject.instance())
            box = roi.boundingBox()
            box.grow(1)
            original_rows = {str(f.id()): f for f in source.getFeatures(QgsFeatureRequest().setFilterRect(reverse.transformBoundingBox(box)))}
            prepared = {str(f["id_font"]): f for f in layers[name].getFeatures()}
            check(name + "-source-ids", set(original_rows) == set(prepared) and len(prepared) == layers[name].featureCount())
            good = True
            for identity, feature in original_rows.items():
                geometry = QgsGeometry(feature.geometry())
                geometry.transform(forward)
                good &= identity in prepared and geometry.isGeosEqual(prepared[identity].geometry())
            check(name + "-whole-geometries", good)
    for name in INITIAL:
        before = list(vector(context.output("initial-data"), name).getFeatures())
        after = list(layers[name].getFeatures())
        check(name + "-initial-preserved", len(before) == len(after) and all(a.attributes() == b.attributes() and a.geometry().isGeosEqual(b.geometry()) for a, b in zip(before, after)))
    for source_name, result_name in (("portals_candidats", "portals_roi"), ("vies_candidats", "viari_roi"),
                                     ("illes_candidates", "illes_roi"), ("termes_candidats", "termes_roi")):
        wanted = {}
        for feature in layers[source_name].getFeatures():
            if result_name == "portals_roi" and str(feature["tipo"]) != "Portal":
                continue
            geometry = feature.geometry().intersection(roi)
            if not geometry.isEmpty() and geometry.type() == layers[source_name].geometryType():
                wanted[str(feature["id_font"])] = geometry
        actual = {str(f["id_font"]): f.geometry() for f in layers[result_name].getFeatures()}
        check(result_name + "-ids", set(actual) == set(wanted))
        check(result_name + "-support", all(k in actual and actual[k].hausdorffDistance(g) <= .001 for k, g in wanted.items()))
        if layers[result_name].geometryType() in (1, 2):
            measure = "length" if layers[result_name].geometryType() == 1 else "area"
            check(result_name + "-measure", sum(getattr(g, measure)() for g in actual.values()),
                  sum(getattr(g, measure)() for g in wanted.values()), .01, "m" if measure == "length" else "m2")
    check("intersection-keeps-overlay-field", all(f["id_roi"] == "roi_vilaseca_500m" for f in layers["illes_roi"].getFeatures()))
    land = one(layers["terra_roi"])
    sea = one(layers["mar_complement"])
    reference_land = QgsGeometry.unaryUnion([f.geometry() for f in layers["termes_candidats"].getFeatures()]).intersection(roi)
    check("land-all-municipalities", land.symDifference(reference_land).area(), 0, .01, "m2")
    check("land-sea-area", land.area() + sea.area(), roi.area(), .01, "m2")
    check("land-sea-disjoint", land.intersection(sea).area(), 0, .01, "m2")
    marine = one(layers["mar_context"])
    check("marine-part-of-complement", marine.difference(sea).area(), 0, .01, "m2")
    corner = QgsPointXY(roi.boundingBox().xMaximum() - 1, roi.boundingBox().yMinimum() + 1)
    check("marine-southeast-reference", marine.contains(QgsGeometry.fromPointXY(corner)))
    corner = QgsPointXY(roi.boundingBox().xMinimum() + 1, roi.boundingBox().yMinimum() + 1)
    check("marine-southwest-reference", marine.contains(QgsGeometry.fromPointXY(corner)))
    check("urban-domain", all(f["clased"] == "Urbano" for f in layers["urbans_roi"].getFeatures()))
    for distance in (5, 10):
        corridor = one(layers[f"buffer_carrers_{distance}m"])
        pieces = one(layers[f"peces_carrers_{distance}m"])
        single = list(layers[f"peces_individuals_{distance}m"].getFeatures())
        check(f"streets-{distance}-partition", pieces.area() + land.intersection(corridor).area(), land.area(), .01, "m2")
        check(f"streets-{distance}-disjoint", pieces.intersection(corridor).area(), 0, .01, "m2")
        check(f"parts-{distance}-single", all(not f.geometry().isMultipart() for f in single))
        check(f"parts-{distance}-coverage", QgsGeometry.unaryUnion([f.geometry() for f in single]).symDifference(pieces).area(), 0, .01, "m2")
        check(f"parts-{distance}-areas", sum(float(f["area_m2"]) for f in single), pieces.area(), .01, "m2")
        check(f"parts-{distance}-identities", len({f["id_peca"] for f in single}), len(single), units="count")
    check("buffer-width-monotonic", one(layers["buffer_carrers_5m"]).difference(one(layers["buffer_carrers_10m"])).area(), 0, .01, "m2")
    for source, centre, vertices in (("illes_roi", "centroides_illes", "vertices_illes"),
                                     ("urbans_roi", "centroides_linies", "vertices_linies")):
        geometries = {str(f["id_font"]): f.geometry() for f in layers[source].getFeatures()}
        check(centre + "-count", layers[centre].featureCount(), len(geometries), units="count")
        check(centre + "-positions", all(f.geometry().distance(geometries[str(f["id_font"])].centroid()) < .00001 for f in layers[centre].getFeatures()))
        expected_vertices = {k: list(g.vertices()) for k, g in geometries.items()}
        check(vertices + "-count", layers[vertices].featureCount(), sum(len(v) for v in expected_vertices.values()), units="count")
        check(vertices + "-positions", all(f.geometry().distance(QgsGeometry.fromPointXY(QgsPointXY(expected_vertices[str(f["id_font"])][int(f["vertex_index"])]))) < .00001 for f in layers[vertices].getFeatures()))
    polygons = {str(f["id_font"]): f.geometry() for f in layers["illes_roi"].getFeatures()}
    check("surface-points-count", layers["punts_superficie_illes"].featureCount(), len(polygons), units="count")
    check("surface-points-contained", all(polygons[str(f["id_font"])].intersects(f.geometry()) for f in layers["punts_superficie_illes"].getFeatures()))
    check("line-endpoints-count", layers["extrems_linies"].featureCount(), 2 * layers["urbans_roi"].featureCount(), units="count")
    summary = list(vector(data, "resum_resultats").getFeatures())
    check("summary-layers", {f["capa"] for f in summary} == set(layers))
    check("summary-counts", all(int(f["n_entitats"]) == layers[f["capa"]].featureCount() for f in summary))
    print(json.dumps({"buffer_sample_min_m": min(distances), "buffer_sample_max_m": max(distances),
                      "roi_bounds": roi.boundingBox().toString(6),
                      "municipalities": [str(f["NAMEUNIT"]) for f in layers["termes_roi"].getFeatures()],
                      "centroids_outside_blocks": sum(not polygons[str(f["id_font"])].intersects(f.geometry()) for f in layers["centroides_illes"].getFeatures()),
                      "marine_complement_parts": len(sea.asGeometryCollection()) if sea.isMultipart() else 1,
                      "marine_component_areas_m2": [g.area() for g in sea.asGeometryCollection()],
                      "marine_context_area_m2": marine.area()}, ensure_ascii=False))
    return checks


def prepare(destination):
    """Retain inputs and the exact author request for the shared CLI; never execute GIS."""
    source = Path(__file__).resolve()
    root = source.parents[3]
    target = (root / destination).resolve()
    require(target.is_relative_to(root / "sandbox/practiques/pr4-geoprocessament"), "Staging must remain in the ignored PR4 sandbox")
    require(not target.exists(), "Preserve existing preparation and choose a new destination")
    request = json.loads(source.with_name("activity.json").read_text())
    for item in request["parameters"]["sources"]:
        original = root / item["repository_path"]
        require(original.is_file() and not original.is_symlink() and digest(original) == item["sha256"], "Original differs: " + str(original))
    target.mkdir(parents=True)
    (target / "inputs").mkdir()
    for item, declared in zip(request["parameters"]["sources"], request["inputs"]):
        require(item["id"] == declared["id"] and item["sha256"] == declared["sha256"], "Request/input mapping differs")
        shutil.copyfile(root / item["repository_path"], target / declared["path"])
        require(digest(target / declared["path"]) == declared["sha256"], "Retained copy differs")
    shutil.copyfile(source, target / "compute.py")
    shutil.copyfile(source.with_name("activity.json"), target / "activity.json")
    print(json.dumps({"prepared": str(target.relative_to(root)), "inputs": len(request["inputs"]), "request_sha256": digest(target / "activity.json")}, indent=2))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["prepare"])
    parser.add_argument("destination")
    args = parser.parse_args()
    prepare(args.destination)
