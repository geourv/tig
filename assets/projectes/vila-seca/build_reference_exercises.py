#!/usr/bin/env python3
"""Build and validate the Vila-seca reference exercise projects."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import gc
import hashlib
import io
import json
import os
from pathlib import Path
import re
import sqlite3
import tempfile
from urllib.parse import quote
import uuid
import zipfile
import xml.etree.ElementTree as ElementTree

from osgeo import gdal
from qgis.PyQt.QtCore import QDateTime, QMetaType, Qt
from qgis.PyQt.QtGui import QFont
from qgis.core import (
    Qgis,
    QgsApplication,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsCsException,
    QgsFeature,
    QgsFeatureRequest,
    QgsField,
    QgsFillSymbol,
    QgsGeometry,
    QgsLayerMetadata,
    QgsLayoutItemLabel,
    QgsLayoutItemLegend,
    QgsLayoutItemMap,
    QgsLayoutItemScaleBar,
    QgsLayoutPoint,
    QgsLayoutSize,
    QgsLineSymbol,
    QgsMarkerSymbol,
    QgsPointXY,
    QgsPrintLayout,
    QgsProject,
    QgsProjectMetadata,
    QgsRasterLayer,
    QgsRectangle,
    QgsReferencedRectangle,
    QgsSingleSymbolRenderer,
    QgsSnappingConfig,
    QgsTextFormat,
    QgsVariantUtils,
    QgsVectorFileWriter,
    QgsVectorLayer,
)


PROJECT_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = PROJECT_ROOT.parents[2]
DEFAULT_ICGC_SOURCE = (
    REPOSITORY_ROOT
    / "tmp/reference-exercises/sources/"
    "divisions-administratives-v2r2-municipis-5000-20260120.fgb"
)
DEFAULT_CNIG_SOURCE = REPOSITORY_ROOT / "tmp/reference-exercises/sources/lineas_limite_gml.zip"
CNIG_MEMBER = "au_AdministrativeUnit_4thOrder0.gml"

ICGC_URL = (
    "https://datacloud.icgc.cat/datacloud/divisions-administratives/"
    "fgb_unzip_EPSG25831/"
    "divisions-administratives-v2r2-municipis-5000-20260120.fgb"
)
ICGC_PRODUCT_URL = (
    "https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/"
    "Geoinformacio-cartografica/Divisions-administratives"
)
ICGC_LICENCE_URL = (
    "https://www.icgc.cat/ca/LICGC/Informacio-publica/Transparencia/"
    "Reutilitzacio-de-la-informacio"
)
ICGC_SHA256 = "069f755f253f7af969e80403f6e81fa2cadefbd4c40ffd2f825f30e167bf2b2d"
ICGC_VILA_SECA_WKB_SHA256 = (
    "5465f4f9f08264b1c3dda94df031d8ad0f48e2e4b6b82faeb34d4eb50e683169"
)
CNIG_DOWNLOAD_URL = "https://centrodedescargas.cnig.es/CentroDescargas/descargaDir"
CNIG_SHA256 = "5bd73c530af995c05da8d9ff4e3d293f62d0dc91c5e48ee773fe881716c108a6"
CNIG_LICENCE_URL = "https://www.ign.es/resources/licencia/Condiciones_licenciaUso_IGN.pdf"

PROJECT_CRS = "EPSG:25831"
EXPECTED_QGIS_VERSION = "3.44.11-Solothurn"
EXPECTED_GDAL_VERSION = "3.10.3"
FIXED_TIMESTAMP = "2026-09-18T00:00:00Z"
FIXED_GPKG_TIMESTAMP = "2026-09-18T00:00:00.000Z"
FIXED_ZIP_TIME = (2026, 9, 18, 0, 0, 0)
QGIS_DOCTYPE = b"<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>\n"
QGIS_UUID_PATTERN = re.compile(
    r"\{[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\}"
)

WMS_URL = "https://geoserveis.icgc.cat/servei/catalunya/orto-territorial/wms?"
WMS_LAYER = "ortofoto_25cm_color_2025"
WMS_NAME = "ICGC Ortofoto territorial 2025"
WMS_URI = (
    "crs=EPSG:25831&dpiMode=7&format=image/jpeg&"
    f"layers={WMS_LAYER}&styles=&url={WMS_URL}"
)

README = Path("README-reference-exercises.md")
PROVENANCE = Path("reference-exercises.provenance.yml")
REPORT_ROOT = Path("informes")
CHECKSUMS = Path("SHA256SUMS-reference-exercises")


@dataclass(frozen=True)
class ProjectContract:
    key: str
    stem: str
    project_name: str
    title: str
    abstract: str
    groups: tuple[tuple[str, tuple[tuple[str, bool], ...]], ...]
    default_layer: str
    has_wms: bool = False
    snapping_layer: str | None = None

    @property
    def geopackage(self) -> Path:
        return Path("dades_preparades") / f"{self.stem}.gpkg"

    @property
    def external_project(self) -> Path:
        return Path(f"{self.stem}.qgz")

    @property
    def local_layers(self) -> tuple[str, ...]:
        return tuple(
            layer_name
            for _, layers in self.groups
            for layer_name, _ in layers
        )


PROJECTS = (
    ProjectContract(
        key="pr1",
        stem="pr1-fonts-vila-seca",
        project_name="pr1",
        title="PR1 de referència: fonts municipals de Vila-seca",
        abstract=(
            "Comparació docent de les representacions municipals oficials de l'ICGC i "
            "del CNIG sobre l'Ortofoto Territorial 2025."
        ),
        groups=(
            (
                "10_fonts_oficials",
                (("municipality_icgc_5k", True), ("municipality_cnig", True)),
            ),
            ("00_context", ()),
        ),
        default_layer="municipality_icgc_5k",
        has_wms=True,
    ),
    ProjectContract(
        key="pr2",
        stem="pr2-digitalitzacio-vila-seca",
        project_name="pr2",
        title="PR2 de referència: esquema de digitalització",
        abstract=(
            "Esquema docent amb les fonts municipals preservades, un límit de treball "
            "derivat i geometries exclusivament sintètiques per provar punts, línies i polígons."
        ),
        groups=(
            (
                "30_captura_sintetica",
                (("fanals", True), ("carrils_bici", True), ("plaques_solars", True)),
            ),
            ("20_limit_treball", (("municipi_treball", True),)),
            (
                "10_fonts_preservades",
                (("municipality_icgc_5k", False), ("municipality_cnig", False)),
            ),
            ("00_context", ()),
        ),
        default_layer="municipi_treball",
        has_wms=True,
        snapping_layer="carrils_bici",
    ),
    ProjectContract(
        key="ex05",
        stem="ex05-seleccions-jerarquiques-vila-seca",
        project_name="ex05",
        title="Exercici 05: seleccions jeràrquiques i espacials",
        abstract=(
            "Exemple acotat de seleccions per atribut i per relació espacial sobre els "
            "municipis de Catalunya; no substitueix la micropràctica 3."
        ),
        groups=(
            (
                "20_seleccions_espacials",
                (
                    ("veins_vila_seca_espacial", True),
                    ("tarragona_espacial", False),
                    ("ambit_tarragona", True),
                ),
            ),
            (
                "10_seleccions_atributs",
                (
                    ("vila_seca_atribut", True),
                    ("tarragones_atribut", False),
                    ("camp_tarragona_atribut", False),
                    ("tarragona_atribut", False),
                ),
            ),
            ("00_base", (("municipis_catalunya", True),)),
        ),
        default_layer="ambit_tarragona",
    ),
)

EXPECTED_COUNTS: dict[str, dict[str, int | None]] = {
    "pr1": {"municipality_icgc_5k": 1, "municipality_cnig": 1},
    "pr2": {
        "municipality_icgc_5k": 1,
        "municipality_cnig": 1,
        "municipi_treball": 1,
        "fanals": 3,
        "carrils_bici": 3,
        "plaques_solars": 2,
    },
    "ex05": {
        "municipis_catalunya": 947,
        "tarragona_atribut": 184,
        "camp_tarragona_atribut": 118,
        "tarragones_atribut": 22,
        "vila_seca_atribut": 1,
        "ambit_tarragona": 1,
        "tarragona_espacial": 184,
        "veins_vila_seca_espacial": None,
    },
}

PROJECT_OUTPUTS = tuple(
    path
    for project in PROJECTS
    for path in (project.geopackage, project.external_project)
)
REPORTS = {
    contract.key: REPORT_ROOT / f"{contract.stem}.md"
    for contract in PROJECTS
}
OUTPUT_MEMBERS = PROJECT_OUTPUTS + tuple(REPORTS[contract.key] for contract in PROJECTS)
STATIC_MEMBERS = (README, PROVENANCE, Path("build_reference_exercises.py"))
CHECKSUM_MEMBERS = STATIC_MEMBERS + OUTPUT_MEMBERS


class BuildError(RuntimeError):
    """Raised when a source or generated artifact violates the contract."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise BuildError(message)


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_runtime() -> None:
    require(
        Qgis.QGIS_VERSION == EXPECTED_QGIS_VERSION,
        f"Versió QGIS inesperada: {Qgis.QGIS_VERSION}; s'esperava {EXPECTED_QGIS_VERSION}.",
    )
    gdal_version = gdal.VersionInfo("RELEASE_NAME")
    require(
        gdal_version == EXPECTED_GDAL_VERSION,
        f"Versió GDAL inesperada: {gdal_version}; s'esperava {EXPECTED_GDAL_VERSION}.",
    )


def icgc_fields() -> list[QgsField]:
    return [
        QgsField("CODIMUNI", QMetaType.Type.QString, "text", 6),
        QgsField("NOMMUNI", QMetaType.Type.QString, "text", 60),
        QgsField("NOMMUNIIND", QMetaType.Type.QString, "text", 60),
        QgsField("CAPMUNI", QMetaType.Type.QString, "text", 30),
        QgsField("CAPMUNIIND", QMetaType.Type.QString, "text", 30),
        QgsField("AREAM5000", QMetaType.Type.Double, "real", 19, 3),
        QgsField("CODICOMAR", QMetaType.Type.QString, "text", 2),
        QgsField("NOMCOMAR", QMetaType.Type.QString, "text", 20),
        QgsField("CAPCOMAR", QMetaType.Type.QString, "text", 35),
        QgsField("CAPCOMIND", QMetaType.Type.QString, "text", 35),
        QgsField("CODIVEGUE", QMetaType.Type.QString, "text", 2),
        QgsField("NOMVEGUE", QMetaType.Type.QString, "text", 60),
        QgsField("CAPVEGUE", QMetaType.Type.QString, "text", 50),
        QgsField("CODIPROV", QMetaType.Type.QString, "text", 2),
        QgsField("NOMPROV", QMetaType.Type.QString, "text", 20),
        QgsField("CAPPROV", QMetaType.Type.QString, "text", 15),
    ]


def cnig_fields() -> list[QgsField]:
    return [
        QgsField("gml_id", QMetaType.Type.QString, "text", 80),
        QgsField("nationalCode", QMetaType.Type.QString, "text", 20),
        QgsField("localId", QMetaType.Type.QString, "text", 20),
        QgsField("nom", QMetaType.Type.QString, "text", 100),
        QgsField("nivell", QMetaType.Type.QString, "text", 40),
        QgsField("edicio", QMetaType.Type.QString, "text", 10),
    ]


def icgc_attributes(properties: dict[str, object]) -> list[object]:
    return [properties[field.name()] for field in icgc_fields()]


def copy_multipolygon(geometry: QgsGeometry) -> QgsGeometry:
    copied = QgsGeometry(geometry)
    require(not copied.isEmpty(), "S'ha trobat una geometria buida.")
    if not copied.isMultipart():
        require(copied.convertToMultiType(), "No s'ha pogut convertir la geometria a multipart.")
    require(copied.isGeosValid(), "S'ha trobat una geometria no vàlida.")
    return copied


def load_icgc_source(path: Path) -> list[tuple[dict[str, object], QgsGeometry]]:
    require(path.is_file(), f"Falta la font ICGC: {path}")
    require(sha256_file(path) == ICGC_SHA256, "El SHA-256 de la font ICGC no coincideix.")
    layer = QgsVectorLayer(str(path), "municipis_icgc_font", "ogr")
    require(layer.isValid(), "QGIS no pot obrir el FlatGeobuf de l'ICGC.")
    require(layer.featureCount() == 947, "La font ICGC no conté 947 municipis.")
    require(layer.crs().authid() == PROJECT_CRS, f"La font ICGC no usa {PROJECT_CRS}.")

    expected_fields = tuple(field.name() for field in icgc_fields())
    require(
        tuple(layer.fields().names()) == expected_fields,
        f"L'esquema ICGC ha canviat: {layer.fields().names()}",
    )
    records: list[tuple[dict[str, object], QgsGeometry]] = []
    for feature in layer.getFeatures():
        properties = {name: feature[name] for name in expected_fields}
        records.append((properties, copy_multipolygon(feature.geometry())))
    records.sort(key=lambda record: str(record[0]["CODIMUNI"]))

    require(len({str(record[0]["CODIMUNI"]) for record in records}) == 947, "CODIMUNI no és únic.")
    require(sum(record[0]["CODIPROV"] == "43" for record in records) == 184, "Recompte provincial inesperat.")
    require(sum(record[0]["CODIVEGUE"] == "04" for record in records) == 118, "Recompte de vegueria inesperat.")
    require(sum(record[0]["CODICOMAR"] == "36" for record in records) == 22, "Recompte comarcal inesperat.")
    vila_seca = [record for record in records if record[0]["CODIMUNI"] == "431711"]
    require(len(vila_seca) == 1, "No s'ha trobat exactament Vila-seca a la font ICGC.")
    require(vila_seca[0][0]["NOMMUNI"] == "Vila-seca", "El codi 431711 no correspon a Vila-seca.")
    require(
        sha256_bytes(bytes(vila_seca[0][1].asWkb())) == ICGC_VILA_SECA_WKB_SHA256,
        "La geometria ICGC de Vila-seca no coincideix amb l'edició fixada.",
    )
    del layer
    gc.collect()
    return records


def load_cnig_source(path: Path) -> tuple[list[object], QgsGeometry]:
    require(path.is_file(), f"Falta la font CNIG: {path}")
    require(sha256_file(path) == CNIG_SHA256, "El SHA-256 de la font CNIG no coincideix.")
    source_uri = f"/vsizip/{path.resolve().as_posix()}/{CNIG_MEMBER}"
    layer = QgsVectorLayer(source_uri, "municipis_cnig_font", "ogr")
    require(layer.isValid(), "QGIS no pot obrir l'AdministrativeUnit municipal del CNIG.")
    require(layer.featureCount() == 8220, "La capa municipal del CNIG no conté 8.220 unitats.")
    require(layer.crs().authid() == "EPSG:4258", "La font CNIG no usa EPSG:4258.")
    request = QgsFeatureRequest().setFilterExpression('"nationalCode" = 34094343171')
    features = list(layer.getFeatures(request))
    require(len(features) == 1, "No s'ha trobat exactament Vila-seca a la font CNIG.")
    source = features[0]
    require(source["text"] == "Vila-seca", "La unitat CNIG no es diu Vila-seca.")

    geometry = QgsGeometry(source.geometry())
    transform = QgsCoordinateTransform(
        layer.crs(),
        QgsCoordinateReferenceSystem(PROJECT_CRS),
        QgsProject.instance().transformContext(),
    )
    try:
        result = geometry.transform(transform)
    except QgsCsException as error:
        raise BuildError(f"No s'ha pogut transformar la geometria CNIG: {error}") from error
    require(result == Qgis.GeometryOperationResult.Success, "La transformació CNIG ha fallat.")
    geometry = copy_multipolygon(geometry)
    attributes: list[object] = [
        source["gml_id"],
        str(source["nationalCode"]),
        str(source["localId"]),
        source["text"],
        "Municipio",
        "2026-08-10",
    ]
    del source
    del features
    del layer
    gc.collect()
    return attributes, geometry


def add_features(layer: QgsVectorLayer, features: list[QgsFeature]) -> None:
    result = layer.dataProvider().addFeatures(features)
    success = result[0] if isinstance(result, tuple) else bool(result)
    require(success, f"No s'han pogut afegir entitats a {layer.name()}.")
    layer.updateExtents()


def write_layer(
    geopackage: Path,
    layer_name: str,
    geometry_type: str,
    fields: list[QgsField],
    records: list[tuple[list[object], QgsGeometry]],
    create_file: bool,
) -> None:
    memory = QgsVectorLayer(f"{geometry_type}?crs={PROJECT_CRS}", layer_name, "memory")
    require(memory.isValid(), f"No s'ha pogut crear la capa temporal {layer_name}.")
    require(memory.dataProvider().addAttributes(fields), f"No s'han pogut crear els camps de {layer_name}.")
    memory.updateFields()
    features: list[QgsFeature] = []
    for attributes, geometry in records:
        feature = QgsFeature(memory.fields())
        feature.setAttributes(attributes)
        feature.setGeometry(QgsGeometry(geometry))
        features.append(feature)
    add_features(memory, features)

    geopackage.parent.mkdir(parents=True, exist_ok=True)
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "GPKG"
    options.layerName = layer_name
    options.fileEncoding = "UTF-8"
    options.actionOnExistingFile = (
        QgsVectorFileWriter.ActionOnExistingFile.CreateOrOverwriteFile
        if create_file
        else QgsVectorFileWriter.ActionOnExistingFile.CreateOrOverwriteLayer
    )
    options.layerOptions = ["FID=fid", "GEOMETRY_NAME=geom", "SPATIAL_INDEX=YES"]
    error, _, _, error_message = QgsVectorFileWriter.writeAsVectorFormatV3(
        memory,
        str(geopackage),
        QgsProject.instance().transformContext(),
        options,
    )
    require(
        error == QgsVectorFileWriter.WriterError.NoError,
        f"No s'ha pogut escriure {layer_name}: {error_message or error}",
    )
    del features
    del memory
    gc.collect()


def apply_database_contract(
    geopackage: Path,
    descriptions: dict[str, str],
    unique_fields: dict[str, str],
) -> None:
    with sqlite3.connect(geopackage) as connection:
        for layer_name, description in descriptions.items():
            connection.execute(
                "UPDATE gpkg_contents SET identifier = ?, description = ?, last_change = ? "
                "WHERE table_name = ?",
                (layer_name, description, FIXED_GPKG_TIMESTAMP, layer_name),
            )
        for layer_name, field_name in unique_fields.items():
            connection.execute(
                f'CREATE UNIQUE INDEX "ux_{layer_name}_{field_name}" '
                f'ON "{layer_name}"("{field_name}")'
            )
        connection.commit()


def build_pr1(
    geopackage: Path,
    icgc_records: list[tuple[dict[str, object], QgsGeometry]],
    cnig_record: tuple[list[object], QgsGeometry],
) -> None:
    vila_seca = next(record for record in icgc_records if record[0]["CODIMUNI"] == "431711")
    write_layer(
        geopackage,
        "municipality_icgc_5k",
        "MultiPolygon",
        icgc_fields(),
        [(icgc_attributes(vila_seca[0]), vila_seca[1])],
        True,
    )
    write_layer(
        geopackage,
        "municipality_cnig",
        "MultiPolygon",
        cnig_fields(),
        [cnig_record],
        False,
    )
    apply_database_contract(
        geopackage,
        {
            "municipality_icgc_5k": "Vila-seca, divisions administratives ICGC 1:5.000, edició 20260120.",
            "municipality_cnig": "Vila-seca, AdministrativeUnit municipal del CNIG, edició 2026-08-10.",
        },
        {"municipality_icgc_5k": "CODIMUNI", "municipality_cnig": "nationalCode"},
    )


def synthetic_capture_records(
    municipality: QgsGeometry,
) -> dict[str, list[tuple[list[object], QgsGeometry]]]:
    fixture_source = (
        "Fixture didàctica sintètica situada a l'àrea de demostració; "
        "no és una observació territorial"
    )
    review_state = "no_apte_per_analisi"

    fanals: list[tuple[list[object], QgsGeometry]] = []
    for index, point in enumerate(
        (
            QgsPointXY(344379.0, 4551932.5),
            QgsPointXY(344379.0, 4551887.5),
            QgsPointXY(344379.0, 4551842.5),
        ),
        start=1,
    ):
        fanals.append(
            (
                [
                    f"FAN-DEMO-{index:03d}",
                    "fixture",
                    None,
                    None,
                    fixture_source,
                    "Punt de demostració al carrer de Joanot Martorell; cal observar-lo i validar-lo.",
                    review_state,
                ],
                QgsGeometry.fromPointXY(point),
            )
        )

    bike_nodes = (
        QgsPointXY(344260.0, 4551997.5),
        QgsPointXY(344332.5, 4551977.5),
        QgsPointXY(344405.0, 4551975.0),
        QgsPointXY(344487.5, 4551995.0),
    )
    line_coordinates = (
        (bike_nodes[0], bike_nodes[1]),
        (bike_nodes[1], bike_nodes[2]),
        (bike_nodes[2], bike_nodes[3]),
    )
    carrils: list[tuple[list[object], QgsGeometry]] = []
    for index, coordinates in enumerate(line_coordinates, start=1):
        carrils.append(
            (
                [
                    f"CAR-DEMO-{index:03d}",
                    "fixture",
                    1,
                    fixture_source,
                    None,
                    "Tram de demostració a la Via Màxima; els trams consecutius comparteixen l'extrem.",
                    review_state,
                ],
                QgsGeometry.fromPolylineXY(list(coordinates)),
            )
        )

    def rectangle(cx: float, cy: float, width: float, height: float) -> QgsGeometry:
        ring = [
            QgsPointXY(cx - width / 2, cy - height / 2),
            QgsPointXY(cx + width / 2, cy - height / 2),
            QgsPointXY(cx + width / 2, cy + height / 2),
            QgsPointXY(cx - width / 2, cy + height / 2),
            QgsPointXY(cx - width / 2, cy - height / 2),
        ]
        return QgsGeometry.fromPolygonXY([ring])

    plaques = [
        (
            [
                "PLA-DEMO-001",
                "fixture",
                None,
                None,
                fixture_source,
                "Polígon inventat per provar l'esquema.",
                review_state,
            ],
            rectangle(344437.5, 4551799.0, 8.0, 73.0),
        ),
        (
            [
                "PLA-DEMO-002",
                "fixture",
                None,
                None,
                fixture_source,
                "Polígon inventat per provar l'esquema.",
                review_state,
            ],
            rectangle(344474.0, 4551836.5, 27.0, 9.0),
        ),
    ]
    all_geometries = [record[1] for records in (fanals, carrils, plaques) for record in records]
    require(
        all(geometry.within(municipality) for geometry in all_geometries),
        "Una geometria sintètica ha quedat fora del municipi de treball.",
    )
    return {"fanals": fanals, "carrils_bici": carrils, "plaques_solars": plaques}


def build_pr2(
    geopackage: Path,
    icgc_records: list[tuple[dict[str, object], QgsGeometry]],
    cnig_record: tuple[list[object], QgsGeometry],
) -> None:
    vila_seca = next(record for record in icgc_records if record[0]["CODIMUNI"] == "431711")
    write_layer(
        geopackage,
        "municipality_icgc_5k",
        "MultiPolygon",
        icgc_fields(),
        [(icgc_attributes(vila_seca[0]), vila_seca[1])],
        True,
    )
    write_layer(
        geopackage,
        "municipality_cnig",
        "MultiPolygon",
        cnig_fields(),
        [cnig_record],
        False,
    )
    working_fields = [
        QgsField("id_origen", QMetaType.Type.QString, "text", 30),
        QgsField("codi_muni", QMetaType.Type.QString, "text", 6),
        QgsField("nom_muni", QMetaType.Type.QString, "text", 60),
        QgsField("font_capa", QMetaType.Type.QString, "text", 120),
    ]
    write_layer(
        geopackage,
        "municipi_treball",
        "MultiPolygon",
        working_fields,
        [
            (
                ["ICGC-431711-20260120", "431711", "Vila-seca", "municipality_icgc_5k"],
                vila_seca[1],
            )
        ],
        False,
    )

    capture = synthetic_capture_records(vila_seca[1])
    common_tail = [
        QgsField("font", QMetaType.Type.QString, "text", 160),
        QgsField("observacio", QMetaType.Type.QString, "text", 180),
        QgsField("estat_rev", QMetaType.Type.QString, "text", 30),
    ]
    fanal_fields = [
        QgsField("id_fanal", QMetaType.Type.QString, "text", 30),
        QgsField("tipus", QMetaType.Type.QString, "text", 30),
        QgsField("estat", QMetaType.Type.QString, "text", 30),
        QgsField("data_obs", QMetaType.Type.QDate, "date"),
        *common_tail,
    ]
    carril_fields = [
        QgsField("id_tram", QMetaType.Type.QString, "text", 30),
        QgsField("tipus", QMetaType.Type.QString, "text", 30),
        QgsField("continu", QMetaType.Type.Int, "integer"),
        QgsField("font", QMetaType.Type.QString, "text", 160),
        QgsField("data_font", QMetaType.Type.QDate, "date"),
        QgsField("observacio", QMetaType.Type.QString, "text", 180),
        QgsField("estat_rev", QMetaType.Type.QString, "text", 30),
    ]
    placa_fields = [
        QgsField("id_placa", QMetaType.Type.QString, "text", 30),
        QgsField("tipus", QMetaType.Type.QString, "text", 30),
        QgsField("estat", QMetaType.Type.QString, "text", 30),
        QgsField("data_obs", QMetaType.Type.QDate, "date"),
        *common_tail,
    ]
    write_layer(geopackage, "fanals", "Point", fanal_fields, capture["fanals"], False)
    write_layer(geopackage, "carrils_bici", "LineString", carril_fields, capture["carrils_bici"], False)
    write_layer(geopackage, "plaques_solars", "Polygon", placa_fields, capture["plaques_solars"], False)
    apply_database_contract(
        geopackage,
        {
            "municipality_icgc_5k": "Font ICGC preservada sense modificar.",
            "municipality_cnig": "Font CNIG preservada sense modificar.",
            "municipi_treball": "Límit de treball derivat explícitament de municipality_icgc_5k.",
            "fanals": "Fixture didàctica sintètica de punts; no conté observacions territorials.",
            "carrils_bici": "Fixture didàctica sintètica de línies connectades; no representa infraestructura real.",
            "plaques_solars": "Fixture didàctica sintètica de polígons; no representa instal·lacions reals.",
        },
        {
            "municipality_icgc_5k": "CODIMUNI",
            "municipality_cnig": "nationalCode",
            "municipi_treball": "codi_muni",
            "fanals": "id_fanal",
            "carrils_bici": "id_tram",
            "plaques_solars": "id_placa",
        },
    )


def build_ex05(
    geopackage: Path,
    icgc_records: list[tuple[dict[str, object], QgsGeometry]],
) -> int:
    province = [record for record in icgc_records if record[0]["CODIPROV"] == "43"]
    vegueria = [record for record in icgc_records if record[0]["CODIVEGUE"] == "04"]
    comarca = [record for record in icgc_records if record[0]["CODICOMAR"] == "36"]
    vila_seca = [record for record in icgc_records if record[0]["CODIMUNI"] == "431711"]
    province_geometry = QgsGeometry.unaryUnion([record[1] for record in province])
    require(not province_geometry.isEmpty() and province_geometry.isGeosValid(), "La dissolució de Tarragona no és vàlida.")
    if not province_geometry.isMultipart():
        require(province_geometry.convertToMultiType(), "No s'ha pogut convertir l'àmbit provincial.")

    spatial_province = [
        record
        for record in icgc_records
        if record[1].pointOnSurface().within(province_geometry)
    ]
    require(
        len(spatial_province) == 184,
        f"La selecció espacial provincial retorna {len(spatial_province)} municipis, no 184.",
    )
    vila_geometry = vila_seca[0][1]
    neighbours = [
        record
        for record in icgc_records
        if record[0]["CODIMUNI"] != "431711"
        and record[1].boundingBox().intersects(vila_geometry.boundingBox())
        and record[1].touches(vila_geometry)
    ]
    require(neighbours, "La selecció espacial de veïns de Vila-seca és buida.")

    selections = (
        ("municipis_catalunya", icgc_records),
        ("tarragona_atribut", province),
        ("camp_tarragona_atribut", vegueria),
        ("tarragones_atribut", comarca),
        ("vila_seca_atribut", vila_seca),
    )
    for index, (layer_name, records) in enumerate(selections):
        write_layer(
            geopackage,
            layer_name,
            "MultiPolygon",
            icgc_fields(),
            [(icgc_attributes(properties), geometry) for properties, geometry in records],
            index == 0,
        )
    write_layer(
        geopackage,
        "ambit_tarragona",
        "MultiPolygon",
        [
            QgsField("criteri", QMetaType.Type.QString, "text", 80),
            QgsField("recompte", QMetaType.Type.Int, "integer"),
        ],
        [(["CODIPROV = '43'; dissolució de 184 municipis", 184], province_geometry)],
        False,
    )
    write_layer(
        geopackage,
        "tarragona_espacial",
        "MultiPolygon",
        icgc_fields(),
        [(icgc_attributes(properties), geometry) for properties, geometry in spatial_province],
        False,
    )
    write_layer(
        geopackage,
        "veins_vila_seca_espacial",
        "MultiPolygon",
        icgc_fields(),
        [(icgc_attributes(properties), geometry) for properties, geometry in neighbours],
        False,
    )
    descriptions = {
        "municipis_catalunya": "Base completa de 947 municipis ICGC, edició 20260120.",
        "tarragona_atribut": "Selecció per atribut CODIPROV = '43'.",
        "camp_tarragona_atribut": "Selecció per atribut CODIVEGUE = '04'.",
        "tarragones_atribut": "Selecció per atribut CODICOMAR = '36'.",
        "vila_seca_atribut": "Selecció per atribut CODIMUNI = '431711'.",
        "ambit_tarragona": "Dissolució dels 184 municipis seleccionats per CODIPROV = '43'.",
        "tarragona_espacial": "Municipis amb el punt interior dins de l'àmbit dissolt de Tarragona.",
        "veins_vila_seca_espacial": "Municipis seleccionats perquè toquen geomètricament Vila-seca.",
    }
    unique_fields = {
        layer_name: "CODIMUNI"
        for layer_name, _ in selections
    }
    unique_fields.update(
        {"tarragona_espacial": "CODIMUNI", "veins_vila_seca_espacial": "CODIMUNI"}
    )
    apply_database_contract(geopackage, descriptions, unique_fields)
    return len(neighbours)


def set_layer_metadata(layer: QgsVectorLayer, project_key: str) -> None:
    metadata = QgsLayerMetadata()
    metadata.setIdentifier(f"tig-{project_key}-{layer.name()}")
    metadata.setTitle(layer.name())
    metadata.setLanguage("ca")
    if layer.name() in {"fanals", "carrils_bici", "plaques_solars"}:
        metadata.setAbstract(
            "Fixture didàctica sintètica. Les geometries no provenen de camp, inventari ni imatge "
            "i no es poden utilitzar per descriure el territori."
        )
        metadata.setLicenses(["Material docent; dades sintètiques"])
        layer.setCustomProperty("tig/data_character", "synthetic_teaching_fixture")
        layer.setCustomProperty("tig/analysis_status", "not_suitable")
    elif layer.name() == "municipality_cnig":
        metadata.setAbstract("Extracció municipal de l'AdministrativeUnit oficial del CNIG.")
        metadata.setLicenses(["CC BY 4.0 ign.es"])
        layer.setCustomProperty("tig/source_sha256", CNIG_SHA256)
        layer.setCustomProperty("tig/source_licence_url", CNIG_LICENCE_URL)
    else:
        metadata.setAbstract("Capa oficial o derivada traçable de les divisions administratives de l'ICGC.")
        metadata.setLicenses(["CC BY 4.0"])
        layer.setCustomProperty("tig/source_sha256", ICGC_SHA256)
        layer.setCustomProperty("tig/source_url", ICGC_URL)
        layer.setCustomProperty("tig/source_product_url", ICGC_PRODUCT_URL)
        layer.setCustomProperty("tig/source_licence_url", ICGC_LICENCE_URL)
    layer.setMetadata(metadata)


def set_layer_style(layer: QgsVectorLayer) -> None:
    name = layer.name()
    if name == "fanals":
        symbol = QgsMarkerSymbol.createSimple(
            {"name": "circle", "color": "225,94,28,255", "outline_color": "110,40,10,255", "size": "3.2"}
        )
    elif name == "carrils_bici":
        symbol = QgsLineSymbol.createSimple({"color": "0,121,107,255", "width": "1.2"})
    elif name == "plaques_solars":
        symbol = QgsFillSymbol.createSimple(
            {"color": "244,180,0,180", "outline_color": "120,85,0,255", "outline_width": "0.5"}
        )
    elif name in {"vila_seca_atribut"}:
        symbol = QgsFillSymbol.createSimple(
            {"color": "190,30,45,170", "outline_color": "120,0,0,255", "outline_width": "0.8"}
        )
    elif name in {"veins_vila_seca_espacial"}:
        symbol = QgsFillSymbol.createSimple(
            {"color": "244,146,66,120", "outline_color": "180,90,20,255", "outline_width": "0.5"}
        )
    elif name in {"ambit_tarragona", "tarragona_espacial"}:
        symbol = QgsFillSymbol.createSimple(
            {"color": "28,113,216,35", "outline_color": "28,90,180,255", "outline_width": "0.8"}
        )
    elif name == "municipis_catalunya":
        symbol = QgsFillSymbol.createSimple(
            {"color": "225,225,225,80", "outline_color": "150,150,150,150", "outline_width": "0.15"}
        )
    elif name == "municipality_cnig":
        symbol = QgsFillSymbol.createSimple(
            {"color": "255,255,255,15", "outline_color": "0,102,153,255", "outline_width": "0.9"}
        )
    elif name in {"municipality_icgc_5k", "municipi_treball"}:
        symbol = QgsFillSymbol.createSimple(
            {"color": "255,255,255,20", "outline_color": "153,0,0,255", "outline_width": "0.9"}
        )
    else:
        symbol = QgsFillSymbol.createSimple(
            {"color": "100,149,237,70", "outline_color": "45,80,140,220", "outline_width": "0.35"}
        )
    require(symbol is not None, f"No s'ha pogut crear la simbologia de {name}.")
    layer.setRenderer(QgsSingleSymbolRenderer(symbol))


def add_layout(
    project: QgsProject,
    contract: ProjectContract,
    extent: QgsReferencedRectangle,
    map_layers: list[object],
) -> None:
    layout = QgsPrintLayout(project)
    layout.initializeDefaults()
    layout.setName("mapa_referencia")

    title = QgsLayoutItemLabel(layout)
    title.setText(contract.title)
    title_format = QgsTextFormat()
    title_format.setFont(QFont("DejaVu Sans"))
    title_format.setSize(16)
    title.setTextFormat(title_format)
    title.adjustSizeToText()
    title.attemptMove(QgsLayoutPoint(10, 8, Qgis.LayoutUnit.Millimeters))
    layout.addLayoutItem(title)

    map_item = QgsLayoutItemMap(layout)
    map_item.setFrameEnabled(True)
    map_item.attemptMove(QgsLayoutPoint(10, 25, Qgis.LayoutUnit.Millimeters))
    map_item.attemptResize(QgsLayoutSize(140, 150, Qgis.LayoutUnit.Millimeters))
    map_item.setExtent(extent.buffered(max(extent.width() * 0.06, 300.0)))
    map_item.setLayers(map_layers)
    map_item.setKeepLayerSet(True)
    layout.addLayoutItem(map_item)

    legend = QgsLayoutItemLegend(layout)
    legend.setTitle("Capes")
    legend.setLinkedMap(map_item)
    legend.setLegendFilterByMapEnabled(True)
    legend.attemptMove(QgsLayoutPoint(154, 30, Qgis.LayoutUnit.Millimeters))
    legend.attemptResize(QgsLayoutSize(130, 120, Qgis.LayoutUnit.Millimeters))
    layout.addLayoutItem(legend)

    scale_bar = QgsLayoutItemScaleBar(layout)
    scale_bar.setStyle("Single Box")
    scale_bar.setLinkedMap(map_item)
    scale_bar.setNumberOfSegments(4)
    scale_bar.setUnits(Qgis.DistanceUnit.Meters)
    if contract.key == "ex05":
        scale_bar.setMapUnitsPerScaleBarUnit(1_000)
        scale_bar.setUnitsPerSegment(20)
        scale_bar.setUnitLabel("km")
    else:
        scale_bar.setUnitsPerSegment(100 if contract.key == "pr2" else 1_000)
        scale_bar.setUnitLabel("m")
    scale_format = QgsTextFormat()
    scale_format.setFont(QFont("DejaVu Sans"))
    scale_format.setSize(8)
    scale_bar.setTextFormat(scale_format)
    scale_bar.applyDefaultSize()
    if contract.key == "ex05":
        scale_bar.setMapUnitsPerScaleBarUnit(1_000)
        scale_bar.setUnitsPerSegment(20_000)
        scale_bar.setUnitLabel("km")
        scale_bar.resizeToMinimumWidth()
    scale_bar.attemptMove(QgsLayoutPoint(154, 163, Qgis.LayoutUnit.Millimeters))
    layout.addLayoutItem(scale_bar)

    note = QgsLayoutItemLabel(layout)
    if contract.key == "pr2":
        note.setText("Geometries de captura: fixtures sintètiques, no observacions territorials.")
    elif contract.key == "ex05":
        note.setText("Exercici acotat; no substitueix la micropràctica 3.")
    else:
        note.setText("Fonts municipals: ICGC i CNIG. Context remot: Ortofoto Territorial 2025.")
    note_format = QgsTextFormat()
    note_format.setFont(QFont("DejaVu Sans"))
    note_format.setSize(7)
    note.setTextFormat(note_format)
    note.setFrameEnabled(True)
    note.setMarginX(1.5)
    note.setMarginY(1.5)
    note.attemptMove(QgsLayoutPoint(10, 184, Qgis.LayoutUnit.Millimeters))
    note.attemptResize(QgsLayoutSize(277, 15, Qgis.LayoutUnit.Millimeters))
    layout.addLayoutItem(note)
    require(project.layoutManager().addLayout(layout), "No s'ha pogut afegir la composició.")


def geopackage_project_uri(geopackage: Path, project_name: str) -> str:
    encoded_path = quote(geopackage.resolve().as_posix(), safe="/")
    return f"geopackage:{encoded_path}?projectName={project_name}"


def stable_layer_id(contract: ProjectContract, layer_name: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9_]", "_", layer_name).strip("_").lower()
    stable = uuid.uuid5(
        uuid.NAMESPACE_URL,
        f"https://dosquartsdedocs.org/tig/reference/{contract.key}/layer/{layer_name}",
    )
    return f"{slug}_{stable.hex}"


def set_project_metadata(project: QgsProject, contract: ProjectContract) -> None:
    metadata = QgsProjectMetadata()
    metadata.setIdentifier(f"tig-reference-{contract.key}")
    metadata.setTitle(contract.title)
    metadata.setAbstract(contract.abstract)
    metadata.setAuthor("Dos quarts de docs")
    metadata.setLanguage("ca")
    metadata.setCreationDateTime(QDateTime.fromString(FIXED_TIMESTAMP, Qt.DateFormat.ISODate))
    project.setMetadata(metadata)


def write_qgis_project(
    geopackage: Path,
    external_project: Path,
    contract: ProjectContract,
) -> None:
    project = QgsProject()
    project.setTitle(contract.title)
    project.setCrs(QgsCoordinateReferenceSystem(PROJECT_CRS))
    project.setFilePathStorage(Qgis.FilePathType.Relative)
    project.setPresetHomePath(".")
    set_project_metadata(project, contract)
    project.writeEntry("tig", "reference_exercise", contract.key)
    project.writeEntry("tig", "icgc_source_sha256", ICGC_SHA256)
    project.writeEntry("tig", "cnig_source_sha256", CNIG_SHA256)
    if contract.key == "pr2":
        project.writeEntry("tig", "fixture_notice", "synthetic_not_observed_not_suitable_for_analysis")
    if contract.key == "ex05":
        project.writeEntry("tig", "scope_notice", "exercise_only_not_micropractice_3")

    root = project.layerTreeRoot()
    groups = {name: root.addGroup(name) for name, _ in contract.groups}
    loaded_layers: dict[str, QgsVectorLayer] = {}
    for group_name, layer_contracts in contract.groups:
        for layer_name, visible in layer_contracts:
            layer = QgsVectorLayer(f"{geopackage}|layername={layer_name}", layer_name, "ogr")
            require(layer.isValid(), f"QGIS no pot obrir {layer_name} des de {geopackage.name}.")
            require(
                layer.setId(stable_layer_id(contract, layer_name)),
                f"No s'ha pogut fixar l'ID de {layer_name}.",
            )
            if "NOMMUNI" in layer.fields().names():
                layer.setDisplayExpression("NOMMUNI")
            elif "nom" in layer.fields().names():
                layer.setDisplayExpression("nom")
            set_layer_metadata(layer, contract.key)
            set_layer_style(layer)
            project.addMapLayer(layer, False)
            node = groups[group_name].addLayer(layer)
            node.setItemVisibilityChecked(visible)
            loaded_layers[layer_name] = layer

    wms_layer: QgsRasterLayer | None = None
    if contract.has_wms:
        wms_layer = QgsRasterLayer(WMS_URI, WMS_NAME, "wms")
        # The remote WMS is visual context; the build validates its declaration, not availability.
        require(
            wms_layer.setId(stable_layer_id(contract, "icgc_ortofoto_2025")),
            "No s'ha pogut fixar l'ID del WMS.",
        )
        wms_layer.setCustomProperty("tig/source_role", "visual_context_only")
        wms_layer.setCustomProperty("tig/source_access_date", "2026-09-18")
        wms_layer.setCustomProperty("tig/source_licence", "CC BY 4.0")
        wms_layer.setCustomProperty("tig/source_licence_url", ICGC_LICENCE_URL)
        project.addMapLayer(wms_layer, False)
        groups["00_context"].addLayer(wms_layer)

    if contract.snapping_layer:
        snapping_layer = loaded_layers[contract.snapping_layer]
        snapping = project.snappingConfig()
        snapping.setEnabled(True)
        snapping.setMode(Qgis.SnappingMode.AdvancedConfiguration)
        snapping.setIndividualLayerSettings(
            snapping_layer,
            QgsSnappingConfig.IndividualLayerSettings(
                True,
                Qgis.SnappingType.Vertex,
                10.0,
                Qgis.MapToolUnit.Pixels,
                0.0,
                0.0,
            ),
        )
        project.setSnappingConfig(snapping)
        project.writeEntry("tig", "snapping_contract", "carrils_bici:vertex:10px")

    default_layer = loaded_layers[contract.default_layer]
    default_extent = QgsReferencedRectangle(default_layer.extent(), default_layer.crs())
    project.viewSettings().setDefaultViewExtent(default_extent)
    layout_extent = default_extent
    if contract.key == "pr2":
        capture_extent = QgsRectangle(loaded_layers["fanals"].extent())
        capture_extent.combineExtentWith(loaded_layers["carrils_bici"].extent())
        capture_extent.combineExtentWith(loaded_layers["plaques_solars"].extent())
        layout_extent = QgsReferencedRectangle(capture_extent, default_layer.crs())
    visible_layer_names = [
        layer_name
        for _, layer_contracts in contract.groups
        for layer_name, visible in layer_contracts
        if visible
    ]
    layout_layers: list[object] = [loaded_layers[layer_name] for layer_name in visible_layer_names]
    if wms_layer is not None:
        layout_layers.append(wms_layer)
    add_layout(project, contract, layout_extent, layout_layers)

    external_project.parent.mkdir(parents=True, exist_ok=True)
    require(project.write(str(external_project)), f"QGIS no ha pogut escriure {external_project.name}.")
    require(
        project.write(geopackage_project_uri(geopackage, contract.project_name)),
        f"QGIS no ha pogut incrustar el projecte {contract.project_name}.",
    )
    project.clear()
    del project
    del default_layer
    del loaded_layers
    del wms_layer
    gc.collect()


def normalize_project_xml(
    content: bytes,
    contract: ProjectContract,
    style_member: str,
    expected_relative_source: str,
) -> bytes:
    try:
        root = ElementTree.fromstring(content)
    except ElementTree.ParseError as error:
        raise BuildError(f"El projecte {contract.key} no conté XML vàlid.") from error
    root.set("saveDateTime", FIXED_TIMESTAMP)
    root.set("saveUser", "unaltraweb")
    root.set("saveUserFull", "unaltraweb")

    author = root.find("./projectMetadata/author")
    require(author is not None, f"El projecte {contract.key} no conté autoria.")
    author.text = "Dos quarts de docs"
    annotation_id = root.find("./main-annotation-layer/id")
    require(annotation_id is not None, f"El projecte {contract.key} no conté la capa d'anotacions.")
    annotation_id.text = f"Annotations_tig_reference_{contract.key}"
    style_settings = root.find("./ProjectStyleSettings")
    require(style_settings is not None, f"El projecte {contract.key} no conté ProjectStyleSettings.")
    style_settings.set("projectStyleId", f"attachment:///{style_member}")
    style_settings.set("RandomizeDefaultSymbolColor", "0")

    profile_colors = {
        "color": "153,0,0,255,rgb:0.6,0,0,1",
        "line_color": "153,0,0,255,rgb:0.6,0,0,1",
        "outline_color": "102,0,0,255,rgb:0.4,0,0,1",
    }
    for profile_tag in ("profileLineSymbol", "profileFillSymbol", "profileMarkerSymbol"):
        for profile in root.iter(profile_tag):
            for option in profile.iter("Option"):
                name = option.get("name")
                if name in profile_colors:
                    option.set("value", profile_colors[name])

    individual_snapping = root.find("./snapping-settings/individual-layer-settings")
    if individual_snapping is not None:
        individual_snapping[:] = sorted(
            individual_snapping,
            key=lambda element: element.get("id", ""),
        )

    source_marker = f"/dades_preparades/{contract.stem}.gpkg"

    def normalize_local_source(value: str) -> str:
        if source_marker not in value:
            return value
        _, suffix = value.split(source_marker, 1)
        return expected_relative_source + suffix

    for element in root.iter():
        for key, value in element.attrib.items():
            element.set(key, normalize_local_source(value))
        if element.text:
            element.text = normalize_local_source(element.text)

    generated_ids: dict[str, str] = {}
    for element in root.iter():
        values = [element.attrib[key] for key in sorted(element.attrib)]
        if element.text:
            values.append(element.text)
        for value in values:
            for match in QGIS_UUID_PATTERN.finditer(value):
                original = match.group(0)
                if original not in generated_ids:
                    stable = uuid.uuid5(
                        uuid.NAMESPACE_URL,
                        f"https://dosquartsdedocs.org/tig/reference/{contract.key}/{len(generated_ids)}",
                    )
                    generated_ids[original] = f"{{{stable}}}"

    def replace_generated_id(match: re.Match[str]) -> str:
        return generated_ids[match.group(0)]

    for element in root.iter():
        for key, value in element.attrib.items():
            element.set(key, QGIS_UUID_PATTERN.sub(replace_generated_id, value))
        if element.text:
            element.text = QGIS_UUID_PATTERN.sub(replace_generated_id, element.text)
        ordered_attributes = sorted(element.attrib.items())
        element.attrib.clear()
        element.attrib.update(ordered_attributes)
    ElementTree.indent(root, space="  ")
    return QGIS_DOCTYPE + ElementTree.tostring(root, encoding="utf-8") + b"\n"


def normalize_qgis_archive(
    content: bytes,
    contract: ProjectContract,
    expected_relative_source: str,
) -> bytes:
    project_member = f"{contract.project_name}.qgs"
    style_member = f"{contract.project_name}_styles.db"
    if not content.startswith(b"PK"):
        return normalize_project_xml(content, contract, style_member, expected_relative_source)
    source = io.BytesIO(content)
    target = io.BytesIO()
    with zipfile.ZipFile(source, "r") as current:
        project_members = [member for member in current.infolist() if member.filename.endswith(".qgs")]
        style_members = [member for member in current.infolist() if member.filename.endswith("_styles.db")]
        require(len(project_members) == 1, f"El projecte {contract.key} no conté un únic .qgs.")
        require(len(style_members) == 1, f"El projecte {contract.key} no conté una única base d'estils.")
        members = [
            (
                project_member,
                normalize_project_xml(
                    current.read(project_members[0]),
                    contract,
                    style_member,
                    expected_relative_source,
                ),
            ),
            (style_member, current.read(style_members[0])),
        ]
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as normalized:
        for filename, payload in members:
            info = zipfile.ZipInfo(filename, FIXED_ZIP_TIME)
            info.create_system = 3
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o100644 & 0xFFFF) << 16
            normalized.writestr(info, payload)
    return target.getvalue()


def normalize_project_files(root: Path, contract: ProjectContract) -> None:
    external = root / contract.external_project
    external_relative_source = f"./dades_preparades/{contract.stem}.gpkg"
    embedded_relative_source = f"./{contract.stem}.gpkg"
    external.write_bytes(
        normalize_qgis_archive(external.read_bytes(), contract, external_relative_source)
    )
    geopackage = root / contract.geopackage
    with sqlite3.connect(geopackage) as connection:
        projects = connection.execute("SELECT name, content FROM qgis_projects ORDER BY name").fetchall()
        require(
            [row[0] for row in projects] == [contract.project_name],
            f"{geopackage.name} no conté únicament el projecte {contract.project_name}.",
        )
        stored = projects[0][1]
        stored_hex = stored.decode("ascii") if isinstance(stored, bytes) else str(stored)
        normalized = normalize_qgis_archive(
            bytes.fromhex(stored_hex),
            contract,
            embedded_relative_source,
        )
        metadata = json.dumps(
            {"last_modified_time": FIXED_TIMESTAMP, "last_modified_user": "unaltraweb"},
            ensure_ascii=True,
            sort_keys=True,
            separators=(",", ":"),
        )
        connection.execute(
            "UPDATE qgis_projects SET metadata = ?, content = ? WHERE name = ?",
            (metadata, normalized.hex(), contract.project_name),
        )
        connection.execute("UPDATE gpkg_contents SET last_change = ?", (FIXED_GPKG_TIMESTAMP,))
        connection.commit()
        connection.execute("PRAGMA journal_mode=DELETE")
        connection.execute("VACUUM")
        connection.commit()


def embedded_project_content(geopackage: Path, project_name: str) -> bytes:
    with sqlite3.connect(geopackage) as connection:
        row = connection.execute(
            "SELECT content FROM qgis_projects WHERE name = ?", (project_name,)
        ).fetchone()
    require(row is not None, f"No s'ha trobat el projecte incrustat {project_name}.")
    stored = row[0]
    stored_hex = stored.decode("ascii") if isinstance(stored, bytes) else str(stored)
    return bytes.fromhex(stored_hex)


def project_xml(content: bytes) -> bytes:
    if not content.startswith(b"PK"):
        return content
    with zipfile.ZipFile(io.BytesIO(content), "r") as archive:
        members = [name for name in archive.namelist() if name.endswith(".qgs")]
        require(len(members) == 1, "El paquet QGIS no conté una única definició .qgs.")
        return archive.read(members[0])


def validate_portability(
    content: bytes,
    contract: ProjectContract,
    expected_relative_source: str,
) -> None:
    require(
        content == normalize_qgis_archive(content, contract, expected_relative_source),
        f"El projecte {contract.key} no usa la serialització canònica.",
    )
    xml = project_xml(content).decode("utf-8")
    require(expected_relative_source in xml, f"No s'ha trobat la font relativa {expected_relative_source}.")
    for layer_name in contract.local_layers:
        require(f"layername={layer_name}" in xml, f"El projecte {contract.key} no referencia {layer_name}.")
    for forbidden in ("/workspace/", "/home/", "/tmp/", ".reference-exercises-"):
        require(forbidden not in xml, f"El projecte {contract.key} conserva un camí no transportable: {forbidden}")


def validate_geopackage(root: Path, contract: ProjectContract) -> dict[str, object]:
    geopackage = root / contract.geopackage
    require(geopackage.is_file(), f"Falta {geopackage}.")
    with sqlite3.connect(geopackage) as connection:
        require(connection.execute("PRAGMA integrity_check").fetchone() == ("ok",), f"Integritat fallida: {geopackage}")
        projects = connection.execute("SELECT name FROM qgis_projects ORDER BY name").fetchall()
        require(projects == [(contract.project_name,)], f"Projectes incrustats inesperats a {geopackage.name}: {projects}")
        layers = {
            row[0]
            for row in connection.execute(
                "SELECT table_name FROM gpkg_contents WHERE data_type = 'features'"
            ).fetchall()
        }
        require(layers == set(contract.local_layers), f"Inventari de capes inesperat a {geopackage.name}: {layers}")

    counts: dict[str, int] = {}
    for layer_name in contract.local_layers:
        layer = QgsVectorLayer(f"{geopackage}|layername={layer_name}", layer_name, "ogr")
        require(layer.isValid(), f"QGIS no pot obrir {layer_name} a {geopackage.name}.")
        require(layer.crs().authid() == PROJECT_CRS, f"{layer_name} no usa {PROJECT_CRS}.")
        count = int(layer.featureCount())
        expected = EXPECTED_COUNTS[contract.key][layer_name]
        if expected is not None:
            require(count == expected, f"{layer_name} conté {count} entitats, no {expected}.")
        else:
            require(count > 0, f"{layer_name} és buida.")
        counts[layer_name] = count
        for feature in layer.getFeatures():
            geometry = feature.geometry()
            require(not geometry.isEmpty(), f"{layer_name} conté una geometria buida.")
            require(geometry.isGeosValid(), f"{layer_name} conté una geometria no vàlida.")
            if layer_name in {"fanals", "carrils_bici", "plaques_solars"}:
                require(
                    str(feature["font"]).startswith("Fixture didàctica sintètica"),
                    f"{layer_name} conté una font que no declara la fixture.",
                )
                require(feature["estat_rev"] == "no_apte_per_analisi", f"{layer_name} no bloqueja l'ús analític.")
                date_field = "data_font" if layer_name == "carrils_bici" else "data_obs"
                require(QgsVariantUtils.isNull(feature[date_field]), f"{layer_name} inventa una data d'observació.")
        del layer

    if contract.key == "pr2":
        line_layer = QgsVectorLayer(f"{geopackage}|layername=carrils_bici", "carrils_bici", "ogr")
        endpoints: dict[str, int] = {}
        for feature in line_layer.getFeatures():
            points = feature.geometry().asPolyline()
            require(len(points) >= 2, "Un tram sintètic no té prou vèrtexs.")
            for point in (points[0], points[-1]):
                key = f"{point.x():.6f},{point.y():.6f}"
                endpoints[key] = endpoints.get(key, 0) + 1
        require(
            sorted(endpoints.values()) == [1, 1, 2, 2],
            "Els tres trams no formen una cadena amb dos extrems compartits.",
        )
        del line_layer

    if contract.key == "ex05":
        require(
            counts["tarragona_atribut"] == counts["tarragona_espacial"] == 184,
            "Les seleccions provincial per atribut i espacial no són equivalents.",
        )
    gc.collect()
    return {"layers": counts, "crs": PROJECT_CRS, "embedded_project": contract.project_name}


def validate_project(
    path_or_uri: str,
    geopackage: Path,
    contract: ProjectContract,
) -> dict[str, object]:
    project = QgsProject()
    require(project.read(path_or_uri), f"QGIS no pot obrir el projecte {path_or_uri}.")
    require(project.crs().authid() == PROJECT_CRS, f"El projecte {contract.key} no usa {PROJECT_CRS}.")
    require(project.filePathStorage() == Qgis.FilePathType.Relative, f"{contract.key} no desa camins relatius.")
    require(project.presetHomePath() == ".", f"{contract.key} no té carpeta inicial relativa.")
    actual_groups = tuple(child.name() for child in project.layerTreeRoot().children())
    expected_groups = tuple(group_name for group_name, _ in contract.groups)
    require(actual_groups == expected_groups, f"Grups inesperats a {contract.key}: {actual_groups}")

    expected_names = set(contract.local_layers)
    if contract.has_wms:
        expected_names.add(WMS_NAME)
    actual_names = {layer.name() for layer in project.mapLayers().values()}
    require(actual_names == expected_names, f"Capes inesperades a {contract.key}: {actual_names}")
    for layer_name in contract.local_layers:
        layers = project.mapLayersByName(layer_name)
        require(len(layers) == 1 and layers[0].isValid(), f"{contract.key} no resol {layer_name}.")
        require(
            layers[0].id() == stable_layer_id(contract, layer_name),
            f"QGIS no conserva l'identificador estable de {layer_name}.",
        )
        local_path = Path(layers[0].source().split("|", 1)[0]).resolve()
        require(local_path == geopackage.resolve(), f"{layer_name} apunta fora del GeoPackage: {local_path}")
    if contract.has_wms:
        layers = project.mapLayersByName(WMS_NAME)
        require(len(layers) == 1 and layers[0].providerType() == "wms", f"{contract.key} no conté el WMS ICGC.")
        require(
            layers[0].id() == stable_layer_id(contract, "icgc_ortofoto_2025"),
            f"QGIS no conserva l'identificador estable del WMS de {contract.key}.",
        )
        require(WMS_LAYER in layers[0].source(), f"{contract.key} no conserva la capa WMS 2025.")
    if contract.snapping_layer:
        snapping = project.snappingConfig()
        require(snapping.enabled(), "PR2 no té activat l'ajust.")
        require(snapping.mode() == Qgis.SnappingMode.AdvancedConfiguration, "PR2 no usa ajust avançat.")
        layer = project.mapLayersByName(contract.snapping_layer)[0]
        settings = snapping.individualLayerSettings(layer)
        require(settings.enabled(), "L'ajust no està activat per a carrils_bici.")
        require(settings.typeFlag() == Qgis.SnappingType.Vertex, "L'ajust de carrils_bici no és a vèrtexs.")
        require(settings.tolerance() == 10.0, "La tolerància d'ajust no és 10 píxels.")
        require(settings.units() == Qgis.MapToolUnit.Pixels, "La tolerància d'ajust no usa píxels.")
    layouts = tuple(sorted(layout.name() for layout in project.layoutManager().layouts()))
    require(layouts == ("mapa_referencia",), f"Composicions inesperades a {contract.key}: {layouts}")
    layout = project.layoutManager().layoutByName("mapa_referencia")
    map_items = [item for item in layout.items() if isinstance(item, QgsLayoutItemMap)]
    require(len(map_items) == 1, f"{contract.key} no conté un únic mapa de composició.")
    visible_layer_names = [
        layer_name
        for _, layer_contracts in contract.groups
        for layer_name, visible in layer_contracts
        if visible
    ]
    if contract.has_wms:
        visible_layer_names.append(WMS_NAME)
    require(
        [layer.name() for layer in map_items[0].layers()] == visible_layer_names,
        f"Conjunt de capes inesperat a la composició de {contract.key}.",
    )
    summary = {
        "title": project.title(),
        "groups": list(actual_groups),
        "layers": sorted(actual_names),
        "layouts": list(layouts),
    }
    project.clear()
    del project
    gc.collect()
    return summary


def validate_artifacts(root: Path) -> dict[str, object]:
    summaries: dict[str, object] = {}
    for contract in PROJECTS:
        geopackage = root / contract.geopackage
        external = root / contract.external_project
        require(external.is_file(), f"Falta {external}.")
        geopackage_summary = validate_geopackage(root, contract)
        validate_portability(
            external.read_bytes(),
            contract,
            f"./dades_preparades/{contract.stem}.gpkg",
        )
        validate_portability(
            embedded_project_content(geopackage, contract.project_name),
            contract,
            f"./{contract.stem}.gpkg",
        )
        external_summary = validate_project(str(external), geopackage, contract)
        embedded_summary = validate_project(
            geopackage_project_uri(geopackage, contract.project_name),
            geopackage,
            contract,
        )
        require(external_summary == embedded_summary, f"Els projectes extern i incrustat difereixen a {contract.key}.")
        summaries[contract.key] = {
            "geopackage": geopackage_summary,
            "project": external_summary,
        }
    return summaries


def expected_report(root: Path, contract: ProjectContract, summary: dict[str, object]) -> str:
    geopackage = summary["geopackage"]
    project = summary["project"]
    lines = [
        f"# Informe de validació: {contract.stem}",
        "",
        f"- Títol: {project['title']}",
        f"- Generat: `{FIXED_TIMESTAMP}`",
        f"- Runtime: QGIS `{Qgis.QGIS_VERSION}`; GDAL `{gdal.VersionInfo('RELEASE_NAME')}`.",
        f"- CRS: `{geopackage['crs']}`",
        f"- Projecte incrustat: `{geopackage['embedded_project']}`",
        "",
        "## Artefactes",
        "",
        "| Fitxer | Bytes | SHA-256 |",
        "| --- | ---: | --- |",
    ]
    for relative in (contract.geopackage, contract.external_project):
        path = root / relative
        lines.append(f"| `{relative.as_posix()}` | {path.stat().st_size} | `{sha256_file(path)}` |")
    lines.extend(
        [
            "",
            "## Capes locals",
            "",
            "| Capa | Entitats |",
            "| --- | ---: |",
        ]
    )
    for layer_name, feature_count in sorted(geopackage["layers"].items()):
        lines.append(f"| `{layer_name}` | {feature_count} |")
    lines.extend(
        [
            "",
            "## Projecte QGIS",
            "",
            "- Grups: " + ", ".join(f"`{value}`" for value in project["groups"]) + ".",
            "- Capes resoltes: " + ", ".join(f"`{value}`" for value in project["layers"]) + ".",
            "- Composicions: " + ", ".join(f"`{value}`" for value in project["layouts"]) + ".",
        ]
    )
    if contract.has_wms:
        lines.append(
            f"- Context remot declarat: `{WMS_LAYER}` del WMS de l'ICGC; no participa en cap derivació."
        )
    lines.extend(
        [
            "",
            "## Fonts verificades",
            "",
            "| Font | Entitats | SHA-256 |",
            "| --- | ---: | --- |",
            f"| ICGC, municipis 1:5.000 | 947 | `{ICGC_SHA256}` |",
            f"| CNIG, unitats administratives | 8.220 | `{CNIG_SHA256}` |",
            "",
            "Totes les validacions del contracte han passat.",
            "",
        ]
    )
    return "\n".join(lines)


def checksum_member_path(root: Path, relative: Path) -> Path:
    if relative in STATIC_MEMBERS:
        return PROJECT_ROOT / relative
    return root / relative


def write_reports_and_checksums(root: Path, summaries: dict[str, object]) -> None:
    for contract in PROJECTS:
        report_path = root / REPORTS[contract.key]
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            expected_report(root, contract, summaries[contract.key]),
            encoding="utf-8",
        )
    lines = [
        f"{sha256_file(checksum_member_path(root, relative))}  {relative.as_posix()}"
        for relative in CHECKSUM_MEMBERS
    ]
    (root / CHECKSUMS).write_text("\n".join(lines) + "\n", encoding="ascii")


def validate_reports_and_checksums(root: Path, summaries: dict[str, object]) -> None:
    for contract in PROJECTS:
        report_path = root / REPORTS[contract.key]
        require(report_path.is_file(), f"Falta {report_path}.")
        observed_report = report_path.read_text(encoding="utf-8")
        require(
            observed_report == expected_report(root, contract, summaries[contract.key]),
            f"L'informe no coincideix amb els artefactes: {REPORTS[contract.key]}.",
        )
    checksum_path = root / CHECKSUMS
    require(checksum_path.is_file(), f"Falta {checksum_path}.")
    observed_paths: list[Path] = []
    for line in checksum_path.read_text(encoding="ascii").splitlines():
        digest, separator, relative_text = line.partition("  ")
        require(separator == "  " and len(digest) == 64, f"Línia SHA-256 invàlida: {line}")
        relative = Path(relative_text)
        require(not relative.is_absolute() and ".." not in relative.parts, f"Camí SHA-256 insegur: {relative}")
        path = checksum_member_path(root, relative)
        require(path.is_file(), f"Falta el fitxer declarat a checksums: {relative}")
        require(sha256_file(path) == digest, f"SHA-256 incorrecte: {relative}")
        observed_paths.append(relative)
    require(tuple(observed_paths) == CHECKSUM_MEMBERS, "L'inventari de checksums no és l'esperat.")


def validate_static_files() -> None:
    for relative in STATIC_MEMBERS:
        require((PROJECT_ROOT / relative).is_file(), f"Falta el fitxer estàtic {relative}.")


def publish(staging: Path) -> None:
    for relative in (*OUTPUT_MEMBERS, CHECKSUMS):
        source = staging / relative
        destination = PROJECT_ROOT / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        os.replace(source, destination)


def build(icgc_source: Path, cnig_source: Path) -> dict[str, object]:
    verify_runtime()
    validate_static_files()
    icgc_records = load_icgc_source(icgc_source)
    cnig_record = load_cnig_source(cnig_source)
    with tempfile.TemporaryDirectory(prefix=".reference-exercises-", dir=PROJECT_ROOT) as temporary:
        staging = Path(temporary)
        contracts = {contract.key: contract for contract in PROJECTS}
        build_pr1(staging / contracts["pr1"].geopackage, icgc_records, cnig_record)
        build_pr2(staging / contracts["pr2"].geopackage, icgc_records, cnig_record)
        neighbour_count = build_ex05(staging / contracts["ex05"].geopackage, icgc_records)
        require(neighbour_count > 0, "La selecció de veïns no ha produït cap resultat.")
        for contract in PROJECTS:
            write_qgis_project(
                staging / contract.geopackage,
                staging / contract.external_project,
                contract,
            )
            normalize_project_files(staging, contract)
        summaries = validate_artifacts(staging)
        write_reports_and_checksums(staging, summaries)
        validate_reports_and_checksums(staging, summaries)
        publish(staging)
    final_summaries = validate_artifacts(PROJECT_ROOT)
    validate_reports_and_checksums(PROJECT_ROOT, final_summaries)
    return {
        "ok": True,
        "mode": "build",
        "projects": final_summaries,
        "checksums": CHECKSUMS.as_posix(),
    }


def check() -> dict[str, object]:
    verify_runtime()
    validate_static_files()
    summaries = validate_artifacts(PROJECT_ROOT)
    validate_reports_and_checksums(PROJECT_ROOT, summaries)
    return {"ok": True, "mode": "check", "projects": summaries, "checksums": CHECKSUMS.as_posix()}


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--icgc-source", type=Path, default=DEFAULT_ICGC_SOURCE)
    parser.add_argument("--cnig-source", type=Path, default=DEFAULT_CNIG_SOURCE)
    parser.add_argument("--check", action="store_true", help="Valida els artefactes sense regenerar-los.")
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    QgsApplication.setPrefixPath("/usr", True)
    application = QgsApplication([], False)
    application.initQgis()
    try:
        result = check() if arguments.check else build(arguments.icgc_source.resolve(), arguments.cnig_source.resolve())
        result["qgis_version"] = Qgis.QGIS_VERSION
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except BuildError as error:
        print(json.dumps({"ok": False, "error": str(error)}, ensure_ascii=False, indent=2))
        return 1
    finally:
        application.exitQgis()


if __name__ == "__main__":
    raise SystemExit(main())
