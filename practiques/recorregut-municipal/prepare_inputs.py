"""Retain the authorised municipal originals; never overwrite inputs or packages.

Local copies are byte-checked. PNOA acquisition is an explicit separate command.
Requests are materialised from the consumer's scientific specification in
compute.py; QGIS execution, verification and sealing remain provider-owned.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import struct
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCES = {
    "lineas_limite_cnig_20260728.zip": (
        "tmp/pr3-guided/browser/LINEAS_LIMITE.ZIP",
        "d752b1b943e6c60f46a23119d6c3d4ad0b198461c502f0a5433197d7a5e34c83"),
    "cartociudad_tarragona_202604.zip": (
        "tmp/pr3-guided/browser/CARTOCIUDAD_CALLEJERO_TARRAGONA.ZIP",
        "7aa8f388d52d4b4c56a4bf25a8601502346c5dccd06405d556895c11d400f919"),
    "transport_tarragona_202607.zip": (
        "tmp/pr3-guided/browser/RT_TARRAGONA_GPKG.ZIP",
        "26e02dee7bef2ab40b46f60d7f97274cab9f47b3b7a418db09b8c43b85303d72"),
    "tarragona.gpkg": (
        "tmp/pr3-guided/inputs-exact/cartociudad/CARTOCIUDAD_CALLEJERO_TARRAGONA/tarragona.gpkg",
        "75b3523872d582ece5dfa2edd488674852557d898bf65f36b511e45be695f90e"),
    "red_viaria.gpkg": (
        "tmp/pr3-guided/inputs-exact/transport/red_viaria.gpkg",
        "77224877c243c32c23853f6859cc6088e653eb21be9698663492ff3f1f28705d"),
    "mdt25_0472.tif": (
        "tmp/unaltracaptura-qgis/cache/prepared/cnig/mdt25/source/pnoa_mdt25_etrs89_hu31_0472_lid.tif",
        "325b8028bc99d4726cfdd9cb777de0ac06ed815a62da2b0e313c0c17daf4bb7c"),
    "mdt25_0473.tif": (
        "tmp/unaltracaptura-qgis/cache/prepared/cnig/mdt25/source/pnoa_mdt25_etrs89_hu31_0473_lid.tif",
        "827b2a41b61a9636178847137647fb46f07d4f227165279d1487e757921f22bf"),
    "mdt200_tarragona.tif": (
        "tmp/unaltracaptura-qgis/cache/prepared/cnig/mdt200/source/pnoa_mdt200_etrs89_hu31_tarragona.tif",
        "1827b96fd3c2d1f7cc6cb41b169fecd98ecade31581debc5264158aa3b65b118"),
    "pr2_sintetic_original.gpkg": (
        "assets/projectes/vila-seca/dades_preparades/pr2-digitalitzacio-vila-seca.gpkg",
        "2ada5ed5b6076ea85ff3533103704caee37e2759ccd99274f8d4f13ba5acddac"),
}
PHASE_FILES = {
    "pr1-project-setup-exemple.gpkg", "pr2-digitalitzacio-exemple.gpkg",
    "pr3-consultes-exemple.gpkg", "pr4-geoprocessament-exemple.gpkg",
    "pr5-raster-exemple.gpkg", "pr6-sintesi-exemple.gpkg",
    "pr6_pendent_roi_graus.tif",
    *{f"pr5_{name}_{size}{suffix}.tif" for size in ("25m", "200m")
      for name, suffix in (("elevacio", ""), ("pendent", "_graus"),
                           ("orientacio", "_graus"), ("elevacio_classes", ""),
                           ("mascara_elevacio_pendent", ""))},
}
PNOA_URL = "https://www.ign.es/wms-inspire/pnoa-ma?"
PNOA_BOUNDS = [338000, 4544500, 351500, 4558000]
PNOA_SIZE = 2048


def sha256(path):
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def checked(path, required=True):
    path = Path(path)
    if not path.is_absolute():
        path = ROOT / path
    if not path.is_relative_to(ROOT) or ".." in path.parts:
        raise ValueError("Input must be inside the selected workspace")
    for part in (path, *path.parents):
        if part.is_symlink():
            raise ValueError(f"Symlink refused: {part}")
        if part == ROOT:
            break
    if path.exists():
        info = path.stat()
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise ValueError(f"Expected a regular unshared file: {path}")
        if path.suffix == ".gpkg" and any(Path(str(path) + s).exists()
                                           for s in ("-wal", "-shm", "-journal")):
            raise ValueError(f"GeoPackage is not quiescent: {path}")
    elif required:
        raise FileNotFoundError(path)
    return path


def retain(source, name, expected, dry_run):
    source = checked(source)
    destination = checked(HERE / "inputs" / name, required=False)
    if sha256(source) != expected:
        raise ValueError(f"Original differs: {source}")
    state = "planned"
    if destination.exists():
        if sha256(destination) != expected:
            raise ValueError(f"Existing input differs; preserved: {destination}")
        state = "reused"
    elif not dry_run:
        destination.parent.mkdir(parents=True, exist_ok=True)
        checked(destination, required=False)
        with source.open("rb") as src, destination.open("xb") as dst:
            for block in iter(lambda: src.read(1024 * 1024), b""):
                dst.write(block)
            dst.flush()
            os.fsync(dst.fileno())
        if sha256(destination) != expected or sha256(source) != expected:
            raise ValueError("Copy differs; all evidence preserved")
        state = "copied"
    return dict(source=str(source.relative_to(ROOT)),
                destination=str(destination.relative_to(ROOT)),
                sha256=expected, bytes=source.stat().st_size, state=state)


def create(path, raw):
    path = checked(path, required=False)
    path.parent.mkdir(parents=True, exist_ok=True)
    checked(path, required=False)
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def fetch(parameters, maximum):
    url = PNOA_URL + urllib.parse.urlencode(parameters)
    request = urllib.request.Request(url, headers={"User-Agent": "TIG-teaching-inputs/1.0"})
    with urllib.request.urlopen(request, timeout=90) as response:
        if urllib.parse.urlsplit(response.url).hostname != "www.ign.es":
            raise ValueError("Unexpected PNOA redirect")
        raw = response.read(maximum + 1)
        headers = dict(response.headers.items())
    if len(raw) > maximum:
        raise ValueError("PNOA response exceeds the declared bound")
    return raw, dict(url=url, parameters=parameters, headers=headers,
                    sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw))


def pnoa(dry_run):
    names = ("pnoa_vilaseca_context.png", "pnoa_capabilities.xml", "pnoa_vilaseca_procedencia.json")
    paths = [checked(HERE / "inputs" / name, required=False) for name in names]
    if any(path.exists() for path in paths):
        if not all(path.exists() for path in paths):
            raise ValueError("Incomplete PNOA acquisition retained; do not overwrite")
        metadata = json.loads(paths[2].read_text())
        if (sha256(paths[0]) != metadata["getmap"]["sha256"]
                or sha256(paths[1]) != metadata["capabilities"]["sha256"]
                or metadata["bounds"] != PNOA_BOUNDS):
            raise ValueError("Retained PNOA inputs changed")
        return dict(state="reused", metadata=metadata)
    if dry_run:
        return dict(state="planned", bounds=PNOA_BOUNDS, crs="EPSG:25831",
                    width=PNOA_SIZE, height=PNOA_SIZE, destinations=names)
    base = dict(SERVICE="WMS", VERSION="1.3.0")
    capabilities, cap_record = fetch(dict(base, REQUEST="GetCapabilities"), 2_000_000)
    tree = ET.fromstring(capabilities)
    if not any(node.text == "OI.OrthoimageCoverage" for node in tree.iter()):
        raise ValueError("Required PNOA layer is missing")
    geometry = dict(CRS="EPSG:25831", BBOX=",".join(map(str, PNOA_BOUNDS)),
                    WIDTH=str(PNOA_SIZE), HEIGHT=str(PNOA_SIZE))
    image, map_record = fetch(dict(base, **geometry, REQUEST="GetMap",
                                  LAYERS="OI.OrthoimageCoverage", STYLES="",
                                  FORMAT="image/png", TRANSPARENT="FALSE"), 30_000_000)
    if image[:8] != b"\x89PNG\r\n\x1a\n" or struct.unpack(">II", image[16:24]) != (PNOA_SIZE, PNOA_SIZE):
        raise ValueError("GetMap did not return the expected PNG")
    samples = []
    for x, y in ((344400, 4551900), (347000, 4549000), (343000, 4553000)):
        i = int((x - PNOA_BOUNDS[0]) * PNOA_SIZE / (PNOA_BOUNDS[2] - PNOA_BOUNDS[0]))
        j = int((PNOA_BOUNDS[3] - y) * PNOA_SIZE / (PNOA_BOUNDS[3] - PNOA_BOUNDS[1]))
        raw, record = fetch(dict(base, **geometry, REQUEST="GetFeatureInfo", STYLES="",
                                 LAYERS="OI.MosaicElement", QUERY_LAYERS="OI.MosaicElement",
                                 I=str(i), J=str(j), INFO_FORMAT="application/json", FEATURE_COUNT="10"), 1_000_000)
        record.update(point=[x, y], response_text=raw.decode("utf-8"), response=json.loads(raw))
        samples.append(record)
    metadata = dict(schema_version=1, source="IGN/PNOA", licence="CC BY 4.0 scne.es",
                    captured_at=datetime.now(timezone.utc).isoformat(), crs="EPSG:25831",
                    bounds=PNOA_BOUNDS, width=PNOA_SIZE, height=PNOA_SIZE,
                    purpose="Extracte local de context; no és una descàrrega analítica a 25 cm.",
                    capabilities=cap_record, getmap=map_record, mosaic_samples=samples)
    for path, raw in zip(paths, (image, capabilities, (json.dumps(metadata, ensure_ascii=False, indent=2) + "\n").encode())):
        create(path, raw)
    return dict(state="acquired", metadata=metadata)


def model_source(dry_run):
    """Author the two-node QGIS model; target-engine execution is a later check."""
    target = checked(HERE / "pr6_roi_municipal.model3", required=False)
    if target.exists():
        return dict(state="reused", path=str(target.relative_to(ROOT)), sha256=sha256(target))
    if dry_run:
        return dict(state="planned", path=str(target.relative_to(ROOT)))
    from qgis.core import (Qgis, QgsProcessing, QgsProcessingModelChildParameterSource as Source,
        QgsProcessingModelOutput, QgsProcessingModelParameter, QgsProcessingParameterFeatureSource,
        QgsProcessingParameterFeatureSink, QgsProcessingParameterNumber, QgsXmlUtils)
    from qgis.PyQt.QtCore import QPointF
    from qgis.PyQt.QtXml import QDomDocument
    # Author the bounded two-node graph with QGIS's native variant serializer.
    # No GUI or GIS execution is needed to write a model source.
    parameters = {
        "MUNICIPI": QgsProcessingParameterFeatureSource("MUNICIPI", "Un municipi vàlid en EPSG:25831", [QgsProcessing.TypeVectorPolygon]),
        "DISTANCIA": QgsProcessingParameterNumber("DISTANCIA", "Marge en metres", type=QgsProcessingParameterNumber.Double, defaultValue=500, minValue=.001),
        "buffer:BUFFER": QgsProcessingParameterFeatureSink("buffer:BUFFER", "Buffer municipal", QgsProcessing.TypeVectorPolygon),
        "caixa:ROI": QgsProcessingParameterFeatureSink("caixa:ROI", "ROI rectangular", QgsProcessing.TypeVectorPolygon),
    }
    components = {}
    for name, x in (("MUNICIPI", 100), ("DISTANCIA", 450)):
        component = QgsProcessingModelParameter(name)
        component.setPosition(QPointF(x, 50))
        components[name] = component.toVariant()
    children = {}
    for identity, algorithm, output_name, y, sources in (
        ("buffer", "native:buffer", "BUFFER", 200, {
            "INPUT": Source.fromModelParameter("MUNICIPI"), "DISTANCE": Source.fromModelParameter("DISTANCIA"),
            **{name: Source.fromStaticValue(value) for name, value in dict(SEGMENTS=8, END_CAP_STYLE=0, JOIN_STYLE=0,
                MITER_LIMIT=2, DISSOLVE=False, SEPARATE_DISJOINT=False).items()},
        }),
        ("caixa", "native:boundingboxes", "ROI", 350, {"INPUT": Source.fromChildOutput("buffer", "OUTPUT")}),
    ):
        output = QgsProcessingModelOutput(output_name, "Buffer municipal" if identity == "buffer" else "ROI rectangular")
        output.setChildId(identity)
        output.setChildOutputName("OUTPUT")
        output.setPosition(QPointF(560, y))
        children[identity] = dict(active=True, alg_id=algorithm, id=identity,
            component_description=output.description(), component_pos_x=280., component_pos_y=float(y),
            component_width=200., component_height=40., parameters_collapsed=True, outputs_collapsed=True,
            dependencies=[], params={name: [value.toVariant()] for name, value in sources.items()},
            outputs={output_name: output.toVariant()})
    definition = dict(children=children, model_group="TIG", model_name="pr6_roi_municipal",
        parameterDefinitions={name: value.toVariantMap() for name, value in parameters.items()},
        parameters=components, parameterOrder=["MUNICIPI", "DISTANCIA"],
        help={"ALG_DESC": "Una entitat municipal EPSG:25831 i una distància positiva. Buffer de 8 segments/quadrant, extrems i unions arrodonits, sense dissolució; després caixa alineada als eixos. Comprovar geometria i CRS abans d’executar.",
              "ALG_CREATOR": "Docència TIG · URV", "ALG_VERSION": "0.2.0"})
    document = QDomDocument("model")
    document.appendChild(QgsXmlUtils.writeVariant(definition, document))
    raw = document.toString(2).encode("utf-8")
    version = Qgis.QGIS_VERSION
    output_names = ["buffer:BUFFER", "caixa:ROI"]
    create(target, raw)
    return dict(state="authored", source_qgis=version, path=str(target.relative_to(ROOT)),
                sha256=sha256(target), outputs=output_names, execution="not run by source authoring")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("originals", "pnoa", "retain", "request", "model"))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--source")
    parser.add_argument("--name")
    parser.add_argument("--sha256")
    parser.add_argument("--stage", choices=("pr1", "pr2", "pr3", "pr4", "reus", "pr5", "pr6", "bonus"))
    parser.add_argument("--write-request", action="store_true")
    args = parser.parse_args()
    if args.action == "originals":
        for name, (source, expected) in SOURCES.items():
            retain(source, name, expected, True)
        result = [retain(source, name, expected, args.dry_run)
                  for name, (source, expected) in SOURCES.items()]
    elif args.action == "pnoa":
        result = pnoa(args.dry_run)
    elif args.action == "model":
        result = model_source(args.dry_run)
    elif args.action == "retain":
        if args.name not in PHASE_FILES or not args.source or not args.sha256:
            raise ValueError("A reserved phase input, source and sender SHA-256 are required")
        result = retain(args.source, args.name, args.sha256, args.dry_run)
    else:
        if not args.stage:
            raise ValueError("Select one stage")
        spec = importlib.util.spec_from_file_location("municipal_activity", HERE / "compute.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        result = module.request(args.stage, HERE)
        raw = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
        target = checked(HERE / (args.stage + ".json"), required=False)
        if args.write_request and not args.dry_run:
            if target.exists():
                if target.read_bytes() != raw:
                    raise ValueError("Request source differs; review and edit its exact source explicitly")
            else:
                create(target, raw)
            result = dict(request=str(target.relative_to(ROOT)), sha256=hashlib.sha256(raw).hexdigest(),
                          inputs=len(result["inputs"]), products=len(result["products"]), stage=args.stage)
    print(json.dumps({"ok": True, "dry_run": args.dry_run, "result": result}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
