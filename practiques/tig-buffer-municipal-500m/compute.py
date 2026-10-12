"""TIG: one municipal buffer and independent persisted-output controls.

The shared producer owns execution, snapshots, checkpoints, closure and captures.
This single-file source contains only the activity's model and presentation.
"""
import hashlib
import json
import math
from pathlib import Path
import shutil

INPUT_SHA256 = "46aa316b88ec9f6eac559ca4f2037f1e142a997d3c0722febb8912a9a03654dd"
FONT_SHA256 = "ae7b7855e115a5966d8b1b3f80f254ccc117ec86f9965e202ee2940453837280"
FONT_FILE = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
EXPECTED_IDENTITY = ("Vila-seca", "43171", "34094343171", "1172246")
IDENTITY_FIELDS = ("nom_muni", "codi_muni", "codi_oficial", "id_origen")
EXPECTED_GEOS = "3.13.1-CAPI-1.19.2"
LEGACY_CONTOUR_TOLERANCE_M = 3.0
PARAMETERS = {
    "distance_m": 500.0,
    "segments_per_quadrant": 8,
    "dissolve": False,
    "contour_sampling_step_m": 25.0,
    # Derived from GEOS 3.13.1 nearest-integer partial-fillet subdivision,
    # not fitted to the failed measurement. See geos-validation.md.
    "contour_distance_tolerance_m": 500.0 * (1.0 - math.cos(3.0 * math.pi / 64.0)) + 0.01,
    "numeric_distance_tolerance_m": 0.01,
    "coverage_tolerance_m2": 0.01,
}
MAX_SEGMENTS = 10000
MAX_SAMPLES = 20000
ARC_PROBE_ANGLES = (10.0, 15.0, 17.0)


def _parameters(context):
    if context.parameters != PARAMETERS:
        raise ValueError("This source requires the reviewed 500 m / 8-segment parameter set")
    return context.parameters


def _sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _load(path, table, name):
    from qgis.core import QgsVectorLayer
    layer = QgsVectorLayer(str(path) + "|layername=" + table, name, "ogr")
    if not layer.isValid() or layer.subsetString():
        raise ValueError("Invalid or unexpectedly filtered layer: " + table)
    return layer


def _one_feature(layer):
    rows = list(layer.getFeatures())
    if len(rows) != 1:
        raise ValueError(f"{layer.name()}: expected one persisted feature, found {len(rows)}")
    return rows[0]


def _identity(feature):
    return tuple(str(feature[field]) for field in IDENTITY_FIELDS)


def _usable_geometry(feature):
    from qgis.core import QgsWkbTypes
    geometry = feature.geometry()
    if (geometry.isNull() or geometry.isEmpty()
            or geometry.type() != QgsWkbTypes.PolygonGeometry
            or not geometry.isGeosValid()):
        raise ValueError("Expected a valid nonempty polygonal geometry")
    if not math.isfinite(geometry.area()) or geometry.area() <= 0:
        raise ValueError("Expected positive finite planar area")
    return geometry


def _segments(geometry):
    polygons = geometry.asMultiPolygon() if geometry.isMultipart() else [geometry.asPolygon()]
    result = []
    for polygon in polygons:
        for ring in polygon:
            points = [(point.x(), point.y()) for point in ring]
            if len(points) < 4 or points[0] != points[-1]:
                raise ValueError("Expected explicit closed polygon rings")
            if not all(math.isfinite(value) for point in points for value in point):
                raise ValueError("Non-finite contour coordinate")
            result.extend((a[0], a[1], b[0], b[1]) for a, b in zip(points, points[1:]) if a != b)
    if not result or len(result) > MAX_SEGMENTS:
        raise ValueError("Contour is empty or exceeds this activity's segment limit")
    return result


def point_segment_distance(point, segment):
    """Euclidean projection onto the original segment, independent of GEOS buffer."""
    px, py = point
    ax, ay, bx, by = segment
    if not all(math.isfinite(value) for value in (*point, *segment)):
        raise ValueError("Non-finite distance coordinate")
    dx, dy = bx - ax, by - ay
    length_squared = dx * dx + dy * dy
    t = 0.0 if length_squared == 0 else min(1.0, max(0.0, ((px-ax)*dx + (py-ay)*dy) / length_squared))
    return math.hypot(px - (ax + t*dx), py - (ay + t*dy))


def sample_contour(segments, step, limit=MAX_SAMPLES):
    """Include every vertex/midpoint and subdivisions no more than step metres apart."""
    if not math.isfinite(step) or step <= 0 or limit < 1:
        raise ValueError("Invalid contour sampling bound")
    points = []
    for ax, ay, bx, by in segments:
        if not all(math.isfinite(value) for value in (ax, ay, bx, by)):
            raise ValueError("Non-finite contour coordinate")
        pieces = max(2, math.ceil(math.hypot(bx-ax, by-ay) / step))
        needed = pieces + 1 + (pieces % 2)
        if len(points) + needed > limit:
            raise ValueError("Contour sampling exceeds the declared activity limit")
        points.extend((ax + (bx-ax)*index/pieces, ay + (by-ay)*index/pieces)
                      for index in range(pieces + 1))
        if pieces % 2:
            points.append(((ax+bx)/2, (ay+by)/2))
    if not points:
        raise ValueError("No contour samples")
    return points


def nominal_sagitta(radius=500.0, quadrant_segments=8):
    return radius * (1.0 - math.cos(math.pi / (4.0 * quadrant_segments)))


def partial_fillet_sagitta_bound(radius=500.0, quadrant_segments=8):
    return radius * (1.0 - math.cos(3.0 * math.pi / (8.0 * quadrant_segments)))


def segment_pair_distance(first, second):
    """Exact 2-D segment distance in floating arithmetic, including intersections."""
    a, b, c, d = first[:2], first[2:], second[:2], second[2:]
    def orientation(p, q, r):
        return (q[0]-p[0])*(r[1]-p[1]) - (q[1]-p[1])*(r[0]-p[0])
    def on_segment(p, q, r):
        return min(p[0], q[0]) <= r[0] <= max(p[0], q[0]) and min(p[1], q[1]) <= r[1] <= max(p[1], q[1])
    o1, o2 = orientation(a, b, c), orientation(a, b, d)
    o3, o4 = orientation(c, d, a), orientation(c, d, b)
    if ((o1*o2 < 0 and o3*o4 < 0)
            or (o1 == 0 and on_segment(a, b, c)) or (o2 == 0 and on_segment(a, b, d))
            or (o3 == 0 and on_segment(c, d, a)) or (o4 == 0 and on_segment(c, d, b))):
        return 0.0
    return min(point_segment_distance(a, second), point_segment_distance(b, second),
               point_segment_distance(c, first), point_segment_distance(d, first))


def continuous_minimum(output_segments, original_segments):
    if not output_segments or not original_segments or len(output_segments)*len(original_segments) > 2000000:
        raise ValueError("Continuous distance verification exceeds this activity's pair bound")
    return min(segment_pair_distance(output, original)
               for output in output_segments for original in original_segments)


def certify_continuous_upper(output_segments, original_segments, limit, max_cells=20000, max_depth=24):
    """Convex distance-to-one-segment certificate for every complete output interval.

    If one original segment is within limit of BOTH endpoints, all intermediate
    points are also within limit of that segment, hence of the original boundary.
    Nearest segments may differ across cells; unresolved cells are bisected,
    bounded and rejected on exhaustion, never silently accepted from samples.
    """
    if not output_segments or not original_segments or not math.isfinite(limit) or limit <= 0:
        raise ValueError("Invalid continuous upper-distance certificate inputs")
    pending = [(segment[:2], segment[2:], 0) for segment in output_segments]
    visited, certified, deepest, largest_bound = 0, 0, 0, 0.0
    while pending:
        a, b, depth = pending.pop()
        visited += 1
        if visited > max_cells:
            raise ValueError("Continuous upper-distance certificate exceeded its cell bound")
        witness = None
        for original in original_segments:
            bound = max(point_segment_distance(a, original), point_segment_distance(b, original))
            if bound <= limit:
                witness = bound
                break
        if witness is not None:
            certified += 1
            deepest = max(deepest, depth)
            largest_bound = max(largest_bound, witness)
        else:
            if depth >= max_depth:
                raise ValueError("An output interval cannot be certified below the fixed upper distance")
            midpoint = ((a[0]+b[0])/2, (a[1]+b[1])/2)
            pending.extend(((a, midpoint, depth+1), (midpoint, b, depth+1)))
    return dict(upper_bound_m=largest_bound, cells=certified, visited_cells=visited, depth=deepest)


def _compute_arc_probes(context):
    """Known convex triangles: no shallow concavity to conflate with arc rounding."""
    from qgis.core import QgsFeature, QgsGeometry, QgsPointXY, QgsProject, QgsVectorFileWriter, QgsVectorLayer
    layer = QgsVectorLayer("Polygon?crs=EPSG:25831&field=case_id:string&field=turn_deg:double",
                           "Analytical corner probes", "memory")
    features = []
    for index, degrees in enumerate(ARC_PROBE_ANGLES):
        x, y = 360000.0 + index * 12000.0, 4550000.0
        angle = math.radians(degrees)
        points = [QgsPointXY(x-5000, y), QgsPointXY(x, y),
                  QgsPointXY(x+5000*math.cos(angle), y+5000*math.sin(angle)), QgsPointXY(x-5000, y)]
        feature = QgsFeature(layer.fields())
        feature.setAttributes(["arc-" + str(int(degrees)), degrees])
        feature.setGeometry(QgsGeometry.fromPolygonXY([points]))
        features.append(feature)
    if not layer.dataProvider().addFeatures(features)[0]:
        raise ValueError("Could not materialise the analytical corner fixtures")
    layer.updateExtents()
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "GPKG"
    options.layerName = "arc_probe_input"
    written = QgsVectorFileWriter.writeAsVectorFormatV3(
        layer, context.output("arc-probe-input"), QgsProject.instance().transformContext(), options)
    if written[0] != QgsVectorFileWriter.NoError:
        raise ValueError("Could not persist the analytical fixtures: " + str(written))
    layer = None
    context.processing("native:buffer", {
        "INPUT": context.output("arc-probe-input") + "|layername=arc_probe_input",
        "DISTANCE": 500.0, "SEGMENTS": 8, "END_CAP_STYLE": 0, "JOIN_STYLE": 0,
        "MITER_LIMIT": 2.0, "DISSOLVE": False, "SEPARATE_DISJOINT": False,
        "OUTPUT": context.output("arc-probe-buffer"),
    })


def _arc_probe_measurements(context):
    """Match persisted native chords to elementary normals and rotation."""
    layer = _load(context.output("arc-probe-buffer"), "arc_probe_buffer", "Arc controls")
    features = {str(feature["case_id"]): feature for feature in layer.getFeatures()}
    if len(features) != len(ARC_PROBE_ANGLES) or layer.crs().authid() != "EPSG:25831":
        raise ValueError("Analytical fixture count/CRS changed")
    measurements = []
    for index, degrees in enumerate(ARC_PROBE_ANGLES):
        identity = "arc-" + str(int(degrees))
        geometry = _usable_geometry(features[identity])
        segments = _segments(geometry)
        center = (360000.0 + index*12000.0, 4550000.0)
        angle = math.radians(degrees)
        count = max(1, int(angle / (math.pi/16) + 0.5))
        expected = [(center[0]+500*math.sin(angle*i/count), center[1]-500*math.cos(angle*i/count))
                    for i in range(count+1)]
        errors, sagittae = [], []
        for start, end in zip(expected, expected[1:]):
            def mismatch(segment):
                a, b = segment[:2], segment[2:]
                return min(max(math.dist(a, start), math.dist(b, end)),
                           max(math.dist(b, start), math.dist(a, end)))
            segment = min(segments, key=mismatch)
            errors.append(mismatch(segment))
            midpoint = ((segment[0]+segment[2])/2, (segment[1]+segment[3])/2)
            sagittae.append(500 - math.dist(center, midpoint))
        measurements.append(dict(id=identity, turn_degrees=degrees, predicted_segments=count,
            predicted_sagitta_m=500*(1-math.cos(angle/(2*count))),
            measured_sagitta_m=max(sagittae), chord_endpoint_error_m=max(errors)))
    return measurements


def _original_fillet_matches(geometry, observed_segment, point, radius, quadrant_segments):
    """Analytical local witnesses, not a generated alternative buffer polygon."""
    polygons = geometry.asMultiPolygon() if geometry.isMultipart() else [geometry.asPolygon()]
    matches = []
    for polygon_index, polygon in enumerate(polygons):
        for ring_index, ring in enumerate(polygon):
            vertices = [(v.x(), v.y()) for v in ring[:-1]]
            x0, y0 = vertices[0]
            area2 = sum((a[0]-x0)*(b[1]-y0)-(b[0]-x0)*(a[1]-y0)
                        for a, b in zip(vertices, vertices[1:]+vertices[:1]))
            side = (-1 if area2 > 0 else 1) * (1 if ring_index == 0 else -1)
            for index, center in enumerate(vertices):
                before, after = vertices[index-1], vertices[(index+1) % len(vertices)]
                dx0, dy0 = center[0]-before[0], center[1]-before[1]
                dx1, dy1 = after[0]-center[0], after[1]-center[1]
                l0, l1 = math.hypot(dx0, dy0), math.hypot(dx1, dy1)
                if not l0 or not l1 or (dx0*dy1-dy0*dx1)*side >= 0:
                    continue
                n0, n1 = (-side*dy0/l0, side*dx0/l0), (-side*dy1/l1, side*dx1/l1)
                turn = math.atan2(n0[0]*n1[1]-n0[1]*n1[0], n0[0]*n1[0]+n0[1]*n1[1])
                count = max(1, int(abs(turn)/(math.pi/(2*quadrant_segments)) + 0.5))
                for part in range(count):
                    def offset(step):
                        angle = turn*step/count
                        return (center[0]+radius*(n0[0]*math.cos(angle)-n0[1]*math.sin(angle)),
                                center[1]+radius*(n0[0]*math.sin(angle)+n0[1]*math.cos(angle)))
                    start, end = offset(part), offset(part+1)
                    chord = (*start, *end)
                    error = max(point_segment_distance(observed_segment[:2], chord),
                                point_segment_distance(observed_segment[2:], chord))
                    if error <= 0.001:
                        matches.append(dict(polygon=polygon_index, ring=ring_index, vertex=index,
                            center=center, before=before, after=after, partial_angle_degrees=math.degrees(abs(turn)),
                            predicted_segments=count, full_chord=chord, containment_error_m=error,
                            full_chord_length_m=math.dist(start, end),
                            analytic_sagitta_m=radius*(1-math.cos(abs(turn)/(2*count))),
                            observed_endpoint_radii_m=[math.dist(center, observed_segment[:2]),
                                                       math.dist(center, observed_segment[2:])],
                            worst_sample_radius_m=math.dist(center, point),
                            neighboring_vertices_skipped=0))
    return matches


def compute(context):
    from qgis.core import Qgis, QgsCoordinateReferenceSystem, QgsProject, QgsWkbTypes

    p = _parameters(context)
    source_path = context.input("municipi-source")
    if _sha256(source_path) != INPUT_SHA256:
        raise ValueError("The declared municipality source changed")
    source = _load(source_path, "municipi_treball", "Municipi de treball")
    source_feature = _one_feature(source)
    _usable_geometry(source_feature)
    if (source.crs().authid() != "EPSG:25831"
            or source.crs().mapUnits() != Qgis.DistanceUnit.Meters
            or QgsWkbTypes.flatType(source.wkbType()) != QgsWkbTypes.MultiPolygon
            or _identity(source_feature) != EXPECTED_IDENTITY):
        raise ValueError("Municipality identity, geometry or metric CRS does not match the reviewed input")

    # Export only this layer: do not copy the historical embedded WMS project.
    context.processing("native:savefeatures", {
        "INPUT": str(source_path) + "|layername=municipi_treball",
        "OUTPUT": context.output("initial-data"),
    })
    context.processing("native:buffer", {
        "INPUT": context.output("initial-data") + "|layername=municipi_treball",
        "DISTANCE": p["distance_m"],
        "SEGMENTS": p["segments_per_quadrant"],
        "END_CAP_STYLE": 0,
        "JOIN_STYLE": 0,
        "MITER_LIMIT": 2.0,
        "DISSOLVE": p["dissolve"],
        "SEPARATE_DISJOINT": False,
        "OUTPUT": context.output("buffer-data"),
    })

    _compute_arc_probes(context)

    # This exact font is present in the pinned engine and in the delivered fixture.
    if _sha256(FONT_FILE) != FONT_SHA256:
        raise ValueError("The pinned engine's declared DejaVu Sans resource differs")
    shutil.copyfile(FONT_FILE, context.output("font-regular"))
    for project_id, container_id, stored_name in (
        ("initial-project", "initial-data", "inicial"),
        ("resolved-project", "buffer-data", "resolt"),
    ):
        project = QgsProject()
        project.setCrs(QgsCoordinateReferenceSystem("EPSG:25831"))
        project.setEllipsoid("NONE")
        project.setFilePathStorage(Qgis.FilePathType.Relative)
        if project_id == "resolved-project":
            project.addMapLayer(_load(context.output("buffer-data"), "municipi_buffer_500m", "Buffer de 500 m"))
        project.addMapLayer(_load(context.output("initial-data"), "municipi_treball", "Municipi de treball"))
        compose(project, project_id, p, {key: str(value) for key, value in context.outputs.items()})
        context.embed_project(container_id, stored_name, project)
        project.clear()
    if _sha256(source_path) != INPUT_SHA256:
        raise ValueError("Source input was modified during calculation")


def verify(context):
    """Reopen persisted outputs; do not invoke Processing or compute another buffer."""
    from qgis.core import Qgis, QgsWkbTypes

    p = _parameters(context)
    if Qgis.geosVersion() != EXPECTED_GEOS:
        raise ValueError("The reviewed GEOS version changed; review the version-bound validation contract")
    source = _load(context.input("municipi-source"), "municipi_treball", "Font")
    initial = _load(context.output("initial-data"), "municipi_treball", "Inicial")
    result = _load(context.output("buffer-data"), "municipi_buffer_500m", "Buffer")
    features = [_one_feature(layer) for layer in (source, initial, result)]
    original, preserved, buffered = [_usable_geometry(feature) for feature in features]
    reference_segments = _segments(original)
    contour_segments = _segments(buffered)
    points = sample_contour(contour_segments, p["contour_sampling_step_m"])
    # Distance to the nearest segment of ANY original ring, using elementary
    # projection/arithmetic rather than buffer(), GEOS distance or a second result.
    distances = [min(point_segment_distance(point, segment) for segment in reference_segments)
                 for point in points]
    minimum_continuous = continuous_minimum(contour_segments, reference_segments)
    upper_certificate = certify_continuous_upper(
        contour_segments, reference_segments, p["distance_m"] + p["numeric_distance_tolerance_m"])
    lost = original.difference(buffered)
    if lost.isNull() and lost.lastError():
        raise ValueError("Coverage difference failed: " + lost.lastError())
    lost_area = 0.0 if lost.isEmpty() else lost.area()
    parts = len(original.asMultiPolygon()) if original.isMultipart() else 1
    # Conservative independent area-growth bound, not the convex Steiner equality.
    growth_bound = p["distance_m"] * original.length() + parts * math.pi * p["distance_m"]**2
    growth = buffered.area() - original.area()
    if not all(math.isfinite(value) for value in (*distances, lost_area, growth, growth_bound)) or growth_bound <= 0:
        raise ValueError("Non-finite or unusable control metric")

    def check(identity, actual, expected, tolerance=0.0, units="count"):
        return dict(id=identity, actual=float(actual), expected=float(expected),
                    tolerance=float(tolerance), units=units)

    checks = []
    for name, layer, feature in zip(("source", "initial", "buffer"), (source, initial, result), features):
        checks.extend([
            check(name + "-count", sum(1 for _ in layer.getFeatures()), 1),
            check(name + "-crs", int(layer.crs().authid() == "EPSG:25831"), 1, units="boolean"),
            check(name + "-identity", int(_identity(feature) == EXPECTED_IDENTITY), 1, units="boolean"),
            check(name + "-valid", int(feature.geometry().isGeosValid()), 1, units="boolean"),
        ])
    checks.extend([
        check("source-multipolygon", int(QgsWkbTypes.flatType(source.wkbType()) == QgsWkbTypes.MultiPolygon), 1, units="boolean"),
        check("initial-geometry-preserved", int(original.isGeosEqual(preserved)), 1, units="boolean"),
        check("coverage-loss", lost_area, 0, p["coverage_tolerance_m2"], "m2"),
        check("area-increases", int(growth > 0), 1, units="boolean"),
        check("area-growth-upper-bound", growth, growth_bound/2, growth_bound/2, "m2"),
        check("contour-min-distance", min(distances), p["distance_m"], p["contour_distance_tolerance_m"], "m"),
        check("contour-max-distance", max(distances), p["distance_m"], p["numeric_distance_tolerance_m"], "m"),
        check("continuous-min-distance", minimum_continuous, p["distance_m"], p["contour_distance_tolerance_m"], "m"),
        check("continuous-upper-certified", int(upper_certificate["upper_bound_m"] <= p["distance_m"] + p["numeric_distance_tolerance_m"]), 1, units="boolean"),
        check("contour-samples", len(points), MAX_SAMPLES/2, MAX_SAMPLES/2, "samples"),
        check("source-bytes-preserved", int(_sha256(context.input("municipi-source")) == INPUT_SHA256), 1, units="boolean"),
        check("font-bytes", int(_sha256(context.output("font-regular")) == FONT_SHA256), 1, units="boolean"),
    ])
    probes = _arc_probe_measurements(context)
    for probe in probes:
        checks.extend([
            check(probe["id"] + "-chord", probe["chord_endpoint_error_m"], 0, 0.001, "m"),
            check(probe["id"] + "-sagitta", probe["measured_sagitta_m"], probe["predicted_sagitta_m"], 0.001, "m"),
        ])
    # Retain measured evidence even when the producer correctly refuses a check.
    # This is observability only: the model, samples and acceptance checks above
    # remain fixed, and no extra product or alternate GIS execution is introduced.
    worst_index = min(range(len(distances)), key=distances.__getitem__)
    worst_point = points[worst_index]
    output_segment = min(contour_segments, key=lambda segment: point_segment_distance(worst_point, segment))
    nearest_segment = min(reference_segments, key=lambda segment: point_segment_distance(worst_point, segment))
    endpoint_distances = [
        min(point_segment_distance(point, segment) for segment in reference_segments)
        for point in ((output_segment[0], output_segment[1]), (output_segment[2], output_segment[3]))
    ]
    print(json.dumps({
        "diagnostic": "persisted-output-controls",
        "geos_version": Qgis.geosVersion(),
        "source_area_m2": original.area(),
        "buffer_area_m2": buffered.area(),
        "area_growth_m2": growth,
        "area_growth_bound_m2": growth_bound,
        "coverage_loss_m2": lost_area,
        "source_segments": len(reference_segments),
        "buffer_segments": len(contour_segments),
        "samples": len(points),
        "min_distance_m": min(distances),
        "max_distance_m": max(distances),
        "continuous_min_distance_m": minimum_continuous,
        "continuous_upper_certificate": upper_certificate,
        "partial_fillet_sagitta_bound_m": partial_fillet_sagitta_bound(p["distance_m"], p["segments_per_quadrant"]),
        "legacy_minimum_check": {
            "expected": 500.0, "tolerance": LEGACY_CONTOUR_TOLERANCE_M,
            "observed": min(distances), "passed": abs(min(distances)-500.0) <= LEGACY_CONTOUR_TOLERANCE_M,
            "historical_evidence_preserved": True,
        },
        "worst_point_epsg25831": worst_point,
        "worst_output_segment": output_segment,
        "worst_segment_length_m": math.hypot(output_segment[2]-output_segment[0], output_segment[3]-output_segment[1]),
        "worst_segment_endpoint_distances_m": endpoint_distances,
        "nearest_original_segment": nearest_segment,
        "original_fillet_matches": _original_fillet_matches(
            original, output_segment, worst_point, p["distance_m"], p["segments_per_quadrant"]),
        "convex_corner_probes": probes,
        "failed_check_ids": [item["id"] for item in checks
                             if abs(item["actual"]-item["expected"]) > item["tolerance"]],
        "checks": checks,
    }, ensure_ascii=False, indent=2, allow_nan=False), flush=True)
    return checks


def compose(project, project_id, parameters, products):
    """Only domain cartography; native save/inspection/capture stays in the provider."""
    from qgis.core import QgsFillSymbol, QgsPalLayerSettings, QgsTextFormat, QgsVectorLayerSimpleLabeling
    from qgis.PyQt.QtGui import QFont

    text = QgsTextFormat()
    text.setFont(QFont("DejaVu Sans"))
    text.setSize(12)
    project.styleSettings().setDefaultTextFormat(text)
    project.setTitle("Vila-seca · " + ("buffer de 500 m" if project_id == "resolved-project" else "límit municipal"))
    municipal = project.mapLayersByName("Municipi de treball")[0]
    municipal.renderer().setSymbol(QgsFillSymbol.createSimple({
        "color": "255,255,255,0", "outline_color": "#b21789", "outline_width": "0.8",
        "outline_width_unit": "MM",
    }))
    labels = QgsPalLayerSettings()
    labels.fieldName = "nom_muni"
    labels.setFormat(text)
    municipal.setLabeling(QgsVectorLayerSimpleLabeling(labels))
    municipal.setLabelsEnabled(True)
    if project_id == "resolved-project":
        buffer_layer = project.mapLayersByName("Buffer de 500 m")[0]
        buffer_layer.renderer().setSymbol(QgsFillSymbol.createSimple({
            "color": "86,180,233,110", "outline_color": "#0072b2", "outline_width": "0.4",
            "outline_width_unit": "MM",
        }))
