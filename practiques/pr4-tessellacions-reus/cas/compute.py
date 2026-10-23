"""Reus: regular grids, Delaunay distance graphs, postal Voronoi and atlas design.

The course owns these scientific choices and checks. The public practice-v2
producer owns QGIS execution, project reopening, captures and sealed products.
"""
import csv
import hashlib
import json
import math
from pathlib import Path
import shutil
import tempfile
import zipfile

INITIAL = ["municipi_reus", "portals_entorn", "generadors"]
DERIVED = ["domini", "malla_500m", "malla_1000m", "cobertura_atlas", "triangles", "arestes",
           "arestes_25m", "arestes_50m", "arestes_100m", "grups_25m", "grups_50m", "grups_100m",
           "voronoi", "zones_postals"]
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_SHA = "ae7b7855e115a5966d8b1b3f80f254ccc117ec86f9965e202ee2940453837280"


def require(value, message):
    if not value:
        raise ValueError(message)


def digest(path):
    result = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def vector(path, name):
    from qgis.core import QgsVectorLayer
    layer = QgsVectorLayer(str(path) + "|layername=" + name, name, "ogr")
    require(layer.isValid(), "Invalid layer: " + name)
    return layer


def run(context, algorithm, **parameters):
    return context.processing(algorithm, dict(parameters, OUTPUT="TEMPORARY_OUTPUT"))["OUTPUT"]


def memory(name, geometry, fields, rows):
    from qgis.core import QgsFeature, QgsVectorLayer
    # The memory provider otherwise defaults to five decimal places on export.
    fields = [field.replace(":double", ":double(24,10)") for field in fields]
    layer = QgsVectorLayer(geometry + "?crs=EPSG:25831&" + "&".join("field=" + f for f in fields), name, "memory")
    result = []
    for attributes, geom in rows:
        f = QgsFeature(layer.fields())
        f.setAttributes(attributes)
        if geom is not None:
            f.setGeometry(geom)
        result.append(f)
    require(layer.dataProvider().addFeatures(result)[0], "Cannot populate " + name)
    layer.updateExtents()
    return layer


def save(context, layer, name, product="resolved-data"):
    if layer.fields().indexFromName("fid") >= 0:
        layer = run(context, "native:deletecolumn", INPUT=layer, COLUMN=["fid"])
    context.processing("native:savefeatures", dict(INPUT=layer, OUTPUT=context.output(product), LAYER_NAME=name,
        ACTION_ON_EXISTING_FILE=1 if Path(context.output(product)).exists() else 0,
        DATASOURCE_OPTIONS="", LAYER_OPTIONS=""))


def table(context, name, fields, rows, product="resolved-data"):
    save(context, memory(name, "None", fields, [(row, None) for row in rows]), name, product)


def one(layer):
    rows = list(layer.getFeatures())
    require(len(rows) == 1, "Expected one feature: " + layer.name())
    return rows[0].geometry()


def components(count, edges):
    parent = list(range(count))
    sizes = [1] * count

    def root(index):
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    for first, second in edges:
        a, b = root(int(first)), root(int(second))
        if a != b:
            if sizes[a] < sizes[b]:
                a, b = b, a
            parent[b] = a
            sizes[a] += sizes[b]
    return [root(i) for i in range(count)]


def canonical_groups(labels, ids):
    smallest = {}
    for label, identity in zip(labels, ids):
        smallest[label] = min(identity, smallest.get(label, identity))
    return [smallest[label] for label in labels]


def compute(context):
    from collections import Counter
    from qgis.core import (Qgis, QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsFeature,
        QgsFeatureRequest, QgsField, QgsGeometry, QgsPointXY, QgsProject, QgsRectangle, QgsVectorLayer)
    from qgis.PyQt.QtCore import QVariant
    require(context.parameters["municipality_code"] == "34094343123", "This reference case is Reus")
    for item in context.parameters["sources"]:
        require(digest(context.input(item["id"])) == item["sha256"], "Changed original")
    require(digest(FONT) == FONT_SHA, "Font differs")
    shutil.copyfile(FONT, context.output("font-regular"))
    with Path(context.output("font-licence")).open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["component", "notice"])
        writer.writerow(["DejaVu Sans", Path("/usr/share/doc/fonts-dejavu-core/copyright").read_text()])
    Path(context.output("font-licence-types")).write_text('"String","String"\n')
    with tempfile.TemporaryDirectory(prefix="reus-tesselles-") as temporary:
        stem = "recintos_municipales_inspire_peninbal_etrs89"
        with zipfile.ZipFile(context.input("limits")) as archive:
            for suffix in (".shp", ".shx", ".dbf", ".prj", ".cpg"):
                Path(temporary, stem + suffix).write_bytes(archive.read(f"SHP_ETRS89/{stem}/{stem}{suffix}"))
        catalogue = QgsVectorLayer(str(Path(temporary, stem + ".shp")), "Recintes", "ogr")
        municipality = catalogue.materialize(QgsFeatureRequest().setFilterExpression('"NATCODE" = \'34094343123\''))
        require(municipality.featureCount() == 1 and next(municipality.getFeatures())["NAMEUNIT"] == "Reus", "Municipal identity differs")
        municipality = run(context, "native:reprojectlayer", INPUT=municipality, TARGET_CRS="EPSG:25831")
    boundary = one(municipality)
    box = boundary.boundingBox()
    margin = context.parameters["margin_m"]
    domain = QgsRectangle(math.floor((box.xMinimum() - margin) / 1000) * 1000,
                          math.floor((box.yMinimum() - margin) / 1000) * 1000,
                          math.ceil((box.xMaximum() + margin) / 1000) * 1000,
                          math.ceil((box.yMaximum() + margin) / 1000) * 1000)
    source = vector(context.input("cartociudad"), "portalpk_publi")
    require(source.setSubsetString('"tipo" = \'Portal\''), "Portal filter failed")
    target = QgsCoordinateReferenceSystem("EPSG:25831")
    forward = QgsCoordinateTransform(source.crs(), target, QgsProject.instance())
    reverse = QgsCoordinateTransform(target, source.crs(), QgsProject.instance())
    candidates = source.getFeatures(QgsFeatureRequest().setFilterRect(reverse.transformBoundingBox(domain)))
    raw = QgsVectorLayer("Point?crs=EPSG:25831", "portals_entorn", "memory")
    raw.dataProvider().addAttributes(list(source.fields()) + [QgsField("id_font", QVariant.String)])
    raw.updateFields()
    copied, positions = [], {}
    for original in candidates:
        geom = QgsGeometry(original.geometry())
        geom.transform(forward)
        point = geom.asPoint()
        if not domain.contains(point):
            continue
        f = QgsFeature(raw.fields())
        f.setAttributes(original.attributes() + [str(original.id())])
        f.setGeometry(geom)
        copied.append(f)
        positions.setdefault((point.x(), point.y()), []).append(original)
    require(raw.dataProvider().addFeatures(copied)[0] and len(positions) >= 3, "Insufficient portals")
    raw.updateExtents()
    rows, links = [], []
    for (x, y), originals in sorted(positions.items()):
        identity = "g" + hashlib.sha256((x.hex() + ":" + y.hex()).encode()).hexdigest()[:16]
        codes = {str(f["cod_postal"]).strip() for f in originals}
        codes = {"__sense_codi__" if code in {"", "NULL", "None"} else code for code in codes}
        code = next(iter(codes)) if len(codes) == 1 else "__conflicte__"
        rows.append(([identity, code, len(originals)], QgsGeometry.fromPointXY(QgsPointXY(x, y))))
        links.extend([[str(f.id()), str(f["id_porpk"]), identity, str(f["cod_postal"])] for f in originals])
    generators = memory("generadors", "Point", ["id_generador:string", "cod_postal:string", "n_portals:integer"], rows)
    for product in ("initial-data", "resolved-data"):
        for name, layer in (("municipi_reus", municipality), ("portals_entorn", raw), ("generadors", generators)):
            save(context, layer, name, product)
        table(context, "correspondencia", ["id_font:string", "id_porpk:string", "id_generador:string", "cod_postal:string"], links, product)
        table(context, "fonts_dades", ["id:string", "sha256:string", "credit:string"],
              [[item["id"], item["sha256"], "IGN/CNIG; CC BY 4.0"] for item in context.parameters["sources"]], product)
    save(context, memory("domini", "Polygon", ["marge_minim_m:double"], [([margin], QgsGeometry.fromRect(domain))]), "domini")
    metrics = []
    for spacing in (500, 1000):
        grid = run(context, "native:creategrid", TYPE=2, EXTENT=domain, HSPACING=spacing,
                   VSPACING=spacing, HOVERLAY=0, VOVERLAY=0, CRS=target)
        counts, addresses = Counter(), Counter()
        columns, nrows = round(domain.width() / spacing), round(domain.height() / spacing)
        for values, geometry in rows:
            p = geometry.asPoint()
            key = (min(columns - 1, math.floor((p.x() - domain.xMinimum()) / spacing)),
                   min(nrows - 1, math.floor((p.y() - domain.yMinimum()) / spacing)))
            counts[key] += 1
            addresses[key] += values[2]
        cells = []
        for f in grid.getFeatures():
            p = f.geometry().centroid().asPoint()
            col = math.floor((p.x() - domain.xMinimum()) / spacing)
            row = math.floor((p.y() - domain.yMinimum()) / spacing)
            identity = f"g{spacing}_r{row:03d}_c{col:03d}"
            cells.append(([identity, row, col, counts[col, row], addresses[col, row]], f.geometry()))
        fields = ["id_cella:string", "fila:integer", "columna:integer", "n_ubicacions:integer", "n_portals:integer"]
        save(context, memory("malla", "Polygon", fields, cells), f"malla_{spacing}m")
        if spacing == 1000:
            cover = sorted([(a, g) for a, g in cells if g.intersection(boundary).area() > 0], key=lambda item: (-item[0][1], item[0][2]))
            save(context, memory("cobertura_atlas", "Polygon", fields + ["pagina:integer"],
                [(attributes + [i], geom) for i, (attributes, geom) in enumerate(cover, 1)]), "cobertura_atlas")
            metrics.append(["pagines_atlas", len(cover), "count"])
    triangles = run(context, "native:delaunaytriangulation", INPUT=generators, TOLERANCE=0, ADD_ATTRIBUTES=True)
    ids = [a[0] for a, _ in rows]
    coordinates = [(g.asPoint().x(), g.asPoint().y()) for _, g in rows]
    lookup = {xy: i for i, xy in enumerate(coordinates)}
    triangle_rows, edge_set = [], set()
    for feature in triangles.getFeatures():
        vertices = list(feature.geometry().vertices())[:3]
        indices = [lookup[p.x(), p.y()] for p in vertices]
        triangle_rows.append(([ids[i] for i in indices], feature.geometry()))
        edge_set.update(tuple(sorted(pair)) for pair in zip(indices, indices[1:] + indices[:1]))
    save(context, memory("triangles", "Polygon", ["id_a:string", "id_b:string", "id_c:string"], triangle_rows), "triangles")
    edges = []
    for first, second in sorted(edge_set):
        a, b = coordinates[first], coordinates[second]
        length = math.hypot(b[0] - a[0], b[1] - a[1])
        edges.append((first, second, length, QgsGeometry.fromPolylineXY([QgsPointXY(*a), QgsPointXY(*b)])))
    edge_fields = ["id_a:string", "id_b:string", "distancia_m:double"]
    save(context, memory("arestes", "LineString", edge_fields,
         [([ids[a], ids[b], length], geom) for a, b, length, geom in edges]), "arestes")
    for threshold in (25, 50, 100):
        kept = [edge for edge in edges if edge[2] <= threshold]
        save(context, memory("arestes", "LineString", edge_fields,
             [([ids[a], ids[b], length], geom) for a, b, length, geom in kept]), f"arestes_{threshold}m")
        groups = canonical_groups(components(len(rows), [(a, b) for a, b, _, _ in kept]), ids)
        sizes = Counter(groups)
        totals = Counter()
        for group, (attributes, _) in zip(groups, rows):
            totals[group] += attributes[2]
        grouped = [(attributes + [group, sizes[group], totals[group], threshold], geometry)
                   for group, (attributes, geometry) in zip(groups, rows)]
        save(context, memory("grups", "Point", ["id_generador:string", "cod_postal:string", "n_portals:integer",
            "id_grup:string", "n_ubicacions:integer", "n_portals_grup:integer", "llindar_m:double"], grouped), f"grups_{threshold}m")
        metrics += [[f"arestes_{threshold}m", len(kept), "count"], [f"components_{threshold}m", len(sizes), "count"],
                    [f"aillats_{threshold}m", sum(n == 1 for n in sizes.values()), "count"]]
    cells = run(context, "native:voronoipolygons", INPUT=generators, BUFFER=100, TOLERANCE=0, COPY_ATTRIBUTES=True)
    clipped = run(context, "native:clip", INPUT=cells, OVERLAY=municipality)
    save(context, clipped, "voronoi")
    zones = run(context, "native:dissolve", INPUT=clipped, FIELD=["cod_postal"], SEPARATE_DISJOINT=False)
    save(context, memory("zones_postals", "MultiPolygon", ["cod_postal:string"],
        [([str(f["cod_postal"])], f.geometry()) for f in zones.getFeatures()]), "zones_postals")
    metrics += [["portals_entorn", len(copied), "count"], ["generadors", len(rows), "count"],
                ["triangles", len(triangle_rows), "count"], ["arestes", len(edges), "count"],
                ["voronoi_retallat", clipped.featureCount(), "count"], ["categories_postals", zones.featureCount(), "count"]]
    table(context, "resum", ["indicador:string", "valor:double", "unitat:string"], metrics)
    for role, product, stored, names in (("initial-project", "initial-data", "inicial", INITIAL),
                                       ("resolved-project", "resolved-data", "reus", INITIAL + DERIVED)):
        project = QgsProject()
        project.setCrs(target)
        project.setEllipsoid("GRS80")
        project.setFilePathStorage(Qgis.FilePathType.Relative)
        for name in names:
            project.addMapLayer(vector(context.output(product), name))
        compose(project, role, context.parameters, context.outputs)
        context.embed_project(product, stored, project)
        project.clear()


def atlas_layout(project):
    from qgis.core import (QgsLayoutItemLabel, QgsLayoutItemMap, QgsLayoutPoint,
                           QgsLayoutSize, QgsPrintLayout)
    from qgis.PyQt.QtGui import QFont
    for old in list(project.layoutManager().layouts()):
        project.layoutManager().removeLayout(old)
    layout = QgsPrintLayout(project)
    layout.initializeDefaults()
    layout.setName("Atlas de tessel·les de Reus")
    layout.pageCollection().pages()[0].setPageSize(QgsLayoutSize(210, 297))
    coverage = project.mapLayersByName("cobertura_atlas")[0]
    frame = QgsLayoutItemMap(layout)
    layout.addLayoutItem(frame)
    frame.setId("mapa_atlas")
    frame.attemptMove(QgsLayoutPoint(5, 40))
    frame.attemptResize(QgsLayoutSize(200, 200))
    frame.setCrs(project.crs())
    frame.setLayers([project.mapLayersByName(name)[0] for name in ("generadors", "municipi_reus", "malla_1000m")])
    frame.setKeepLayerSet(True)
    frame.zoomToExtent(next(coverage.getFeatures()).geometry().boundingBox())
    frame.setScale(5000)
    frame.setAtlasDriven(True)
    frame.setAtlasScalingMode(QgsLayoutItemMap.Fixed)
    atlas = layout.atlas()
    atlas.setCoverageLayer(coverage)
    atlas.setEnabled(True)
    atlas.setPageNameExpression('"id_cella"')
    atlas.setSortFeatures(True)
    atlas.setSortExpression('"pagina"')
    atlas.setSortAscending(True)
    atlas.setFilenameExpression("'reus_' || \"id_cella\"")
    for identity, text, y, size in (
        ("titol", "Reus · Tessel·la [% @atlas_pagename %]", 10, 13),
        ("escala", "Escala 1:5.000 · EPSG:25831 · Nord a la part superior", 247, 9),
        ("font", "Fonts: IGN/CNIG · CartoCiudad 04/2026 i límits 07/2026", 258, 8),
        ("pagina", "Pàgina [% @atlas_featurenumber %] de [% @atlas_totalfeatures %]", 270, 9),
    ):
        label = QgsLayoutItemLabel(layout)
        layout.addLayoutItem(label)
        label.setId(identity)
        label.setText(text)
        label.setFont(QFont("DejaVu Sans", size))
        label.attemptMove(QgsLayoutPoint(5, y))
        label.attemptResize(QgsLayoutSize(200, 12))
    project.layoutManager().addLayout(layout)
    return layout, frame


def compose(project, project_id, parameters, products):
    if project_id == "capture-online":
        compose_online(project, parameters, products)
        return
    from qgis.core import (QgsFillSymbol, QgsLineSymbol, QgsMarkerSymbol, QgsRectangle,
                           QgsReferencedRectangle, QgsSingleSymbolRenderer, QgsTextFormat)
    from qgis.PyQt.QtGui import QFont
    text = QgsTextFormat()
    text.setFont(QFont("DejaVu Sans"))
    text.setSize(9)
    project.styleSettings().setDefaultTextFormat(text)
    layers = {layer.name(): layer for layer in project.mapLayers().values()}
    for name, layer in layers.items():
        colour = "#bd2976" if name == "municipi_reus" else "#277da8"
        if layer.geometryType() == 2:
            symbol = QgsFillSymbol.createSimple({"style": "no", "outline_color": colour, "outline_width": ".3"})
        elif layer.geometryType() == 1:
            symbol = QgsLineSymbol.createSimple({"line_color": colour, "line_width": ".2"})
        else:
            symbol = QgsMarkerSymbol.createSimple({"color": colour, "size": "1", "outline_style": "no"})
        layer.setRenderer(QgsSingleSymbolRenderer(symbol))
        node = project.layerTreeRoot().findLayer(layer.id())
        node.setItemVisibilityChecked(name in {"municipi_reus", "generadors"})
        node.setExpanded(False)
    extent = QgsRectangle(layers["municipi_reus"].extent())
    extent.scale(1.15)
    project.viewSettings().setDefaultViewExtent(QgsReferencedRectangle(extent, project.crs()))
    project.setTitle("Reus · tessel·lacions i proximitat · cas docent")
    if project_id == "resolved-project" and parameters.get("include_atlas", True):
        atlas_layout(project)


def compose_online(project, parameters, products):
    """Authored map appearance and live WMS context, through the public callback."""
    from qgis.core import (QgsCategorizedSymbolRenderer, QgsDataSourceUri, QgsFillSymbol,
        QgsGraduatedSymbolRenderer, QgsLineSymbol, QgsMarkerSymbol, QgsPalLayerSettings,
        QgsRasterLayer, QgsRendererCategory, QgsRendererRange, QgsSingleSymbolRenderer,
        QgsTextBufferSettings, QgsTextFormat, QgsVectorLayerSimpleLabeling)
    from qgis.PyQt.QtGui import QColor, QFont
    layers = {layer.name(): layer for layer in project.mapLayers().values()}
    for name, layer in layers.items():
        if layer.geometryType() == 2:
            colour = "#d12b7c" if name == "municipi_reus" else "#f4f4f4"
            layer.setRenderer(QgsSingleSymbolRenderer(QgsFillSymbol.createSimple(
                {"style": "no", "outline_color": colour, "outline_width": ".45" if name == "municipi_reus" else ".2"})))
        elif layer.geometryType() == 1:
            layer.setRenderer(QgsSingleSymbolRenderer(QgsLineSymbol.createSimple(
                {"line_color": "#20a4db", "line_width": ".25"})))
        else:
            layer.setRenderer(QgsSingleSymbolRenderer(QgsMarkerSymbol.createSimple(
                {"color": "#ffc233", "size": ".8", "outline_color": "#ffffff", "outline_width": ".1"})))
        layer.setLabelsEnabled(False)
    text = QgsTextFormat()
    text.setFont(QFont("DejaVu Sans"))
    text.setSize(9)
    text.setColor(QColor("#202020"))
    halo = QgsTextBufferSettings()
    halo.setEnabled(True)
    halo.setSize(.9)
    halo.setColor(QColor("#ffffff"))
    text.setBuffer(halo)
    for name, field in (("cobertura_atlas", "pagina"), ("zones_postals", "cod_postal")):
        settings = QgsPalLayerSettings()
        settings.fieldName = field
        settings.setFormat(text)
        layers[name].setLabeling(QgsVectorLayerSimpleLabeling(settings))
        layers[name].setLabelsEnabled(True)
    palette = ["#d73027", "#4575b4", "#1a9850", "#984ea3", "#f46d43", "#66a61e", "#e7298a", "#00a6a6", "#a6761d", "#666666", "#e6ab02", "#7570b3", "#1b9e77", "#e41a1c", "#377eb8"]
    categories = []
    for index, code in enumerate(sorted({str(f["cod_postal"]) for f in layers["zones_postals"].getFeatures()})):
        symbol = QgsFillSymbol.createSimple({"style": "no", "outline_color": palette[index % len(palette)], "outline_width": ".65"})
        categories.append(QgsRendererCategory(code, symbol, code))
    layers["zones_postals"].setRenderer(QgsCategorizedSymbolRenderer("cod_postal", categories))
    for distance in (25, 50, 100):
        ranges = []
        for lower, upper, colour, size, title in ((.5, 1.5, "#777777", "1.1", "Aïllat"),
            (1.5, 9.5, "#377eb8", ".9", "2–9 ubicacions"), (9.5, 99.5, "#00a651", ".95", "10–99 ubicacions"),
            (99.5, 100000, "#d52c83", "1.0", "100 o més ubicacions")):
            symbol = QgsMarkerSymbol.createSimple({"color": colour, "size": size, "outline_color": "#ffffff", "outline_width": ".12"})
            ranges.append(QgsRendererRange(lower, upper, symbol, title))
        layers[f"grups_{distance}m"].setRenderer(QgsGraduatedSymbolRenderer("n_ubicacions", ranges))
    original = vector(products["cartociudad"], "portalpk_publi")
    original.setName("CartoCiudad · font provincial")
    project.addMapLayer(original, False)
    group = project.layerTreeRoot().addGroup("Original provincial")
    group.addLayer(original).setItemVisibilityChecked(False)
    group.setExpanded(False)
    uri = QgsDataSourceUri()
    for key, value in parameters["wms"].items():
        if key != "name":
            uri.setParam(key, value)
    ortho = QgsRasterLayer(bytes(uri.encodedUri()).decode(), parameters["wms"]["name"], "wms")
    require(ortho.isValid(), "PNOA WMS not available")
    project.addMapLayer(ortho, False)
    background = project.layerTreeRoot().addGroup("Context WMS")
    background.addLayer(ortho).setExpanded(False)
    layout = project.layoutManager().layoutByName("Atlas de tessel·les de Reus")
    require(layout is not None, "Verified atlas layout is missing")
    frame = layout.itemById("mapa_atlas")
    frame.setLayers([layers[name] for name in ("generadors", "municipi_reus", "malla_1000m")] + [ortho])


def verify(context):
    from collections import Counter
    import numpy as np
    from scipy.spatial import cKDTree
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components
    from qgis.core import QgsCoordinateReferenceSystem, QgsGeometry, QgsProject
    checks = []

    def check(identity, actual, expected=1, tolerance=0, units="boolean"):
        checks.append(dict(id=identity, actual=float(actual), expected=float(expected), tolerance=float(tolerance), units=units))

    data = context.output("resolved-data")
    layers = {name: vector(data, name) for name in INITIAL + DERIVED}
    for name, layer in layers.items():
        check(name + "-valid", layer.featureCount() > 0 and all(f.geometry().isGeosValid() and not f.geometry().isEmpty() for f in layer.getFeatures()))
        check(name + "-crs", layer.crs().authid() == "EPSG:25831")
    for item in context.parameters["sources"]:
        check("input-" + item["id"], digest(context.input(item["id"])) == item["sha256"])
    generators = list(layers["generadors"].getFeatures())
    ids = [str(f["id_generador"]) for f in generators]
    index = {identity: i for i, identity in enumerate(ids)}
    xy = np.array([(f.geometry().asPoint().x(), f.geometry().asPoint().y()) for f in generators])
    check("generator-identities", len(set(ids)) == len(ids) == len(set(map(tuple, xy))))
    check("source-record-count", sum(int(f["n_portals"]) for f in generators), layers["portals_entorn"].featureCount(), units="count")
    for name in INITIAL:
        initial = list(vector(context.output("initial-data"), name).getFeatures())
        solved = list(layers[name].getFeatures())
        check(name + "-initial-preserved", len(initial) == len(solved) and all(a.attributes() == b.attributes() and a.geometry().isGeosEqual(b.geometry()) for a, b in zip(initial, solved)))
    domain = one(layers["domini"])
    for size in (500, 1000):
        cells = list(layers[f"malla_{size}m"].getFeatures())
        union = QgsGeometry.unaryUnion([f.geometry() for f in cells])
        check(f"grid-{size}-coverage", union.symDifference(domain).area(), 0, .01, "m2")
        check(f"grid-{size}-area", sum(f.geometry().area() for f in cells), domain.area(), .01, "m2")
        check(f"grid-{size}-cell-area", all(abs(f.geometry().area() - size * size) < .001 for f in cells))
        check(f"grid-{size}-points", sum(int(f["n_ubicacions"]) for f in cells), len(generators), units="count")
        check(f"grid-{size}-addresses", sum(int(f["n_portals"]) for f in cells), layers["portals_entorn"].featureCount(), units="count")
    edges = list(layers["arestes"].getFeatures())
    keys = {(str(f["id_a"]), str(f["id_b"])) for f in edges}
    check("unique-undirected-edges", len(keys), len(edges), units="count")
    check("edge-endpoint-identities", all(a in index and b in index and a != b for a, b in keys))
    check("edge-lengths", all(abs(float(f["distancia_m"]) - math.dist(xy[index[str(f["id_a"])]], xy[index[str(f["id_b"])]])) < .000001 for f in edges))
    multiplicity = Counter()
    for f in layers["triangles"].getFeatures():
        vertices = [str(f[name]) for name in ("id_a", "id_b", "id_c")]
        for a, b in zip(vertices, vertices[1:] + vertices[:1]):
            multiplicity[tuple(sorted((a, b)))] += 1
    check("triangle-edge-multiplicity", set(multiplicity.values()) <= {1, 2})
    check("all-triangle-edges", {tuple(sorted(pair)) for pair in keys} == set(multiplicity))
    tree = cKDTree(xy)
    component_counts = []
    for threshold in (25, 50, 100):
        potential = int((tree.count_neighbors(tree, threshold) - len(xy)) / 2)
        require(potential <= 5000000, "Independent radius-graph check exceeds its declared memory budget")
        pairs = tree.query_pairs(threshold, output_type="ndarray")
        graph = coo_matrix((np.ones(len(pairs), dtype=np.uint8), (pairs[:, 0], pairs[:, 1])), shape=(len(xy), len(xy))).tocsr()
        count, labels = connected_components(graph, directed=False)
        expected = dict(zip(ids, canonical_groups(labels.tolist(), ids)))
        actual = {str(f["id_generador"]): str(f["id_grup"]) for f in layers[f"grups_{threshold}m"].getFeatures()}
        check(f"groups-{threshold}-all-points", set(actual) == set(ids))
        check(f"groups-{threshold}-independent-radius-graph", actual == expected)
        subset = list(layers[f"arestes_{threshold}m"].getFeatures())
        wanted = {(str(f["id_a"]), str(f["id_b"])) for f in edges if float(f["distancia_m"]) <= threshold}
        check(f"edges-{threshold}-subset", {(str(f["id_a"]), str(f["id_b"])) for f in subset} == wanted)
        component_counts.append(count)
    check("components-monotonic", component_counts == sorted(component_counts, reverse=True))
    # A GUI-accessible route for students: MIN_SIZE=1 makes every location a
    # core point. Check its components, rather than claiming default DBSCAN is
    # equivalent to an edge-threshold graph.
    qgis_groups = run(context, "native:dbscanclustering", INPUT=layers["generadors"], MIN_SIZE=1, EPS=50, DBSCAN_STAR=False)
    qgis_rows = list(qgis_groups.getFeatures())
    require(qgis_groups.fields().indexFromName("CLUSTER_ID") >= 0, "Unexpected QGIS clustering fields")
    qgis_ids = [str(f["id_generador"]) for f in qgis_rows]
    qgis_labels = [int(f["CLUSTER_ID"]) for f in qgis_rows]
    qgis_canonical = dict(zip(qgis_ids, canonical_groups(qgis_labels, qgis_ids)))
    expected_50 = {str(f["id_generador"]): str(f["id_grup"]) for f in layers["grups_50m"].getFeatures()}
    check("qgis-min-one-distance-components", qgis_canonical == expected_50)
    boundary = one(layers["municipi_reus"])
    cells = list(layers["voronoi"].getFeatures())
    union = QgsGeometry.unaryUnion([f.geometry() for f in cells])
    check("voronoi-coverage", union.symDifference(boundary).area(), 0, .01, "m2")
    check("voronoi-disjoint", sum(f.geometry().area() for f in cells), union.area(), .01, "m2")
    zones = list(layers["zones_postals"].getFeatures())
    check("postal-coverage", QgsGeometry.unaryUnion([f.geometry() for f in zones]).symDifference(boundary).area(), 0, .01, "m2")
    check("postal-disjoint", sum(f.geometry().area() for f in zones), boundary.area(), .01, "m2")
    coverage = list(layers["cobertura_atlas"].getFeatures())
    check("atlas-whole-cells", all(abs(f.geometry().area() - 1000000) < .001 for f in coverage))
    check("atlas-page-identities", sorted(int(f["pagina"]) for f in coverage) == list(range(1, len(coverage) + 1)))
    check("atlas-municipal-coverage", boundary.difference(QgsGeometry.unaryUnion([f.geometry() for f in coverage])).area(), 0, .01, "m2")
    project = QgsProject()
    project.setCrs(QgsCoordinateReferenceSystem("EPSG:25831"))
    for name in ("municipi_reus", "generadors", "malla_1000m", "cobertura_atlas"):
        project.addMapLayer(vector(data, name))
    layout, frame = atlas_layout(project)
    atlas = layout.atlas()
    require(atlas.beginRender(), "Cannot begin native atlas iteration")
    check("atlas-native-count", atlas.count(), len(coverage), units="count")
    visited = []
    footprints = []
    for i in range(atlas.count()):
        require(atlas.seekTo(i), "Cannot seek atlas feature")
        layout.refresh()
        visited.append(atlas.currentFilename())
        current = layout.reportContext().feature()
        footprints.append(QgsGeometry.fromRect(frame.extent()).symDifference(current.geometry()).area())
    atlas.endRender()
    check("atlas-unique-filenames", len(set(visited)), len(coverage), units="count")
    check("atlas-page-order", visited == ["reus_" + str(f["id_cella"]) for f in sorted(coverage, key=lambda f: int(f["pagina"]))])
    check("atlas-page-footprints", max(footprints), 0, .01, "m2")
    check("atlas-map-width", frame.sizeWithUnits().width(), 200, .001, "mm")
    check("atlas-map-height", frame.sizeWithUnits().height(), 200, .001, "mm")
    print(json.dumps({"atlas_pages": len(coverage), "atlas_max_footprint_difference_m2": max(footprints), "radius_graph_components": component_counts}))
    project.clear()
    return checks


def prepare(destination):
    source = Path(__file__).resolve()
    root = source.parents[3]
    target = (root / destination).resolve()
    require(target.is_relative_to(root / "sandbox/practiques/pr4-tessellacions-reus") and not target.exists(), "Use a fresh Reus sandbox destination")
    request = json.loads(source.with_name("activity.json").read_text())
    for item in request["parameters"]["sources"]:
        require(digest(root / item["repository_path"]) == item["sha256"], "Original differs")
    target.mkdir(parents=True)
    (target / "inputs").mkdir()
    for item, declared in zip(request["parameters"]["sources"], request["inputs"]):
        require(item["id"] == declared["id"], "Input mapping differs")
        shutil.copyfile(root / item["repository_path"], target / declared["path"])
    shutil.copyfile(source, target / "compute.py")
    shutil.copyfile(source.with_name("activity.json"), target / "activity.json")
    print(json.dumps({"prepared": str(target.relative_to(root)), "request_sha256": digest(target / "activity.json")}))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["prepare"])
    parser.add_argument("destination")
    args = parser.parse_args()
    prepare(args.destination)
