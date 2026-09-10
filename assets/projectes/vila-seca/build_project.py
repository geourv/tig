#!/usr/bin/env python3
"""Build and validate the reproducible Vila-seca starter project."""

from __future__ import annotations

import argparse
import gc
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import sqlite3
import tempfile
from urllib.parse import quote
import uuid
import zipfile
import xml.etree.ElementTree as ElementTree

from qgis.PyQt.QtCore import QDateTime, QMetaType, Qt
from qgis.core import (
    Qgis,
    QgsApplication,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsCsException,
    QgsFeature,
    QgsField,
    QgsFillSymbol,
    QgsGeometry,
    QgsLayerMetadata,
    QgsProject,
    QgsProjectMetadata,
    QgsRasterLayer,
    QgsReferencedRectangle,
    QgsSingleSymbolRenderer,
    QgsVectorFileWriter,
    QgsVectorLayer,
)


PROJECT_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = PROJECT_ROOT.parents[2]
DEFAULT_DOWNLOADED_SOURCE = (
    REPOSITORY_ROOT
    / "tmp/unaltracaptura-qgis/cache/prepared/cnig/administrative-units/vila-seca-cnig.raw.json"
)
PUBLISHED_SOURCE = Path("dades_originals/vila-seca-cnig.geojson")
GEOPACKAGE = Path("dades_preparades/projecte_tig.gpkg")
EXTERNAL_PROJECT = Path("projecte_tig.qgz")
CHECKSUMS = Path("SHA256SUMS")
ARCHIVE = Path("projecte-tig-vila-seca.zip")
ARCHIVE_ROOT = "projecte-tig-vila-seca"

SOURCE_ITEM_URL = "https://api-features.ign.es/collections/administrativeunit/items/1172246?f=json"
SOURCE_COLLECTION_URL = "https://api-features.ign.es/collections/administrativeunit"
SOURCE_LICENCE_URL = "https://www.ign.es/resources/licencia/Condiciones_licenciaUso_IGN.pdf"
SOURCE_ID = "1172246"
SOURCE_NATIONAL_CODE = "34094343171"
MUNICIPAL_CODE = "43171"
CANONICAL_SOURCE_SHA256 = "abf389424da192263a1f44a569a8f5c9ffb6eeaec5245b22932fb0859831f321"

WMS_URL = "https://www.ign.es/wms-inspire/pnoa-ma?"
WMS_LAYER = "OI.OrthoimageCoverage"
WMS_NAME = "IGN/CNIG PNOA maxima actualitat"
WMS_URI = (
    "crs=EPSG:25831&dpiMode=7&format=image/png&"
    f"layers={WMS_LAYER}&styles=&url={WMS_URL}"
)
LOCAL_LAYER = "municipi_treball"
LOCAL_LAYER_ID = "municipi_treball_1172246"
WMS_LAYER_ID = "ign_cnig_pnoa_oi_orthoimagecoverage"
PROJECT_NAME = "projecte_tig"
PROJECT_CRS = "EPSG:25831"
GROUP_NAMES = (
    "40_resultats",
    "30_intermedies",
    "20_preparades",
    "10_originals_inspeccio",
    "00_context",
)
FIELD_NAMES = (
    "fid",
    "id_origen",
    "codi_oficial",
    "codi_muni",
    "nom_muni",
    "nivell",
    "pais",
    "codi_nut1",
    "codi_nut2",
    "codi_nut3",
    "uri_nivell",
)
FIXED_TIMESTAMP = "2026-09-08T00:00:00Z"
FIXED_GPKG_TIMESTAMP = "2026-09-08T00:00:00.000Z"
FIXED_ZIP_TIME = (2026, 9, 8, 0, 0, 0)
QGIS_PROJECT_MEMBER = "projecte_tig.qgs"
QGIS_STYLE_MEMBER = "projecte_tig_styles.db"
QGIS_DOCTYPE = b"<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>\n"
QGIS_UUID_PATTERN = re.compile(
    r"\{[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\}"
)
CHECKSUM_MEMBERS = (
    Path("README.md"),
    Path("build_project.py"),
    Path("procedencia.yml"),
    PUBLISHED_SOURCE,
    GEOPACKAGE,
    EXTERNAL_PROJECT,
)


class BuildError(RuntimeError):
    """Raised when a source or generated artifact violates the package contract."""


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


def canonical_source_bytes(source: Path) -> tuple[dict[str, object], bytes]:
    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise BuildError(f"No s'ha pogut llegir el JSON de font: {source}: {error}") from error

    require(isinstance(payload, dict), "La resposta de font no es un objecte JSON.")
    properties = payload.get("properties")
    geometry = payload.get("geometry")
    require(payload.get("type") == "Feature", "La resposta no es un objecte GeoJSON Feature.")
    require(str(payload.get("id")) == SOURCE_ID, f"L'identificador de font no es {SOURCE_ID}.")
    require(isinstance(properties, dict), "La font no conte un objecte properties.")
    require(properties.get("nameunit") == "Vila-seca", "La unitat de font no es Vila-seca.")
    require(
        properties.get("nationallevelname") == "Municipio",
        "La unitat de font no te el nivell Municipio.",
    )
    require(
        properties.get("nationalcode") == SOURCE_NATIONAL_CODE,
        f"El codi oficial de font no es {SOURCE_NATIONAL_CODE}.",
    )
    require(properties.get("country") == "ES", "La unitat de font no pertany al codi de pais ES.")
    require(properties.get("codnut3") == "ES514", "La unitat de font no pertany a ES514.")
    require(isinstance(geometry, dict), "La font no conte una geometria.")
    require(geometry.get("type") == "MultiPolygon", "La geometria de font no es MultiPolygon.")
    require(bool(geometry.get("coordinates")), "La geometria de font no te coordenades.")

    canonical = (
        json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")
    actual_hash = sha256_bytes(canonical)
    require(
        actual_hash == CANONICAL_SOURCE_SHA256,
        "El contingut JSON canonic ha canviat: "
        f"s'esperava {CANONICAL_SOURCE_SHA256} i s'ha obtingut {actual_hash}.",
    )
    return payload, canonical


def write_canonical_source(source: Path, destination: Path) -> None:
    _, canonical = canonical_source_bytes(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(canonical)


def build_prepared_layer(source: Path, geopackage: Path) -> None:
    source_layer = QgsVectorLayer(str(source), "vila_seca_cnig_original", "ogr")
    require(source_layer.isValid(), "QGIS no pot obrir el GeoJSON canonic.")
    require(source_layer.featureCount() == 1, "El GeoJSON canonic ha de contenir una entitat.")
    require(source_layer.crs().authid() == "EPSG:4326", "El CRS GeoJSON esperat es EPSG:4326.")
    source_features = list(source_layer.getFeatures())
    require(len(source_features) == 1, "No s'ha pogut llegir exactament una entitat de font.")
    source_feature = source_features[0]
    require(not source_feature.geometry().isEmpty(), "La geometria de font es buida.")
    require(source_feature.geometry().isGeosValid(), "La geometria de font no es valida.")

    target_crs = QgsCoordinateReferenceSystem(PROJECT_CRS)
    require(target_crs.isValid(), f"QGIS no reconeix el CRS {PROJECT_CRS}.")
    memory = QgsVectorLayer(f"MultiPolygon?crs={PROJECT_CRS}", LOCAL_LAYER, "memory")
    require(memory.isValid(), "No s'ha pogut crear la capa preparada temporal.")
    fields = [
        QgsField("id_origen", QMetaType.Type.QString, "text", 20),
        QgsField("codi_oficial", QMetaType.Type.QString, "text", 20),
        QgsField("codi_muni", QMetaType.Type.QString, "text", 5),
        QgsField("nom_muni", QMetaType.Type.QString, "text", 100),
        QgsField("nivell", QMetaType.Type.QString, "text", 40),
        QgsField("pais", QMetaType.Type.QString, "text", 2),
        QgsField("codi_nut1", QMetaType.Type.QString, "text", 3),
        QgsField("codi_nut2", QMetaType.Type.QString, "text", 4),
        QgsField("codi_nut3", QMetaType.Type.QString, "text", 5),
        QgsField("uri_nivell", QMetaType.Type.QString, "text", 255),
    ]
    require(memory.dataProvider().addAttributes(fields), "No s'han pogut crear els camps preparats.")
    memory.updateFields()

    geometry = QgsGeometry(source_feature.geometry())
    transform = QgsCoordinateTransform(
        source_layer.crs(),
        target_crs,
        QgsProject.instance().transformContext(),
    )
    try:
        transform_result = geometry.transform(transform)
    except QgsCsException as error:
        raise BuildError(f"No s'ha pogut transformar la geometria a {PROJECT_CRS}: {error}") from error
    require(
        transform_result == Qgis.GeometryOperationResult.Success,
        f"La transformacio a {PROJECT_CRS} ha retornat {transform_result}.",
    )
    require(not geometry.isEmpty(), "La geometria transformada es buida.")
    require(geometry.isGeosValid(), "La geometria transformada no es valida.")

    properties = {field.name(): source_feature[field.name()] for field in source_layer.fields()}
    prepared = QgsFeature(memory.fields())
    prepared.setGeometry(geometry)
    prepared.setAttributes(
        [
            SOURCE_ID,
            properties["nationalcode"],
            str(properties["nationalcode"])[-5:],
            properties["nameunit"],
            properties["nationallevelname"],
            properties["country"],
            properties["codnut1"],
            properties["codnut2"],
            properties["codnut3"],
            properties["nationallevel"],
        ]
    )
    require(prepared["codi_muni"] == MUNICIPAL_CODE, f"El codi municipal derivat no es {MUNICIPAL_CODE}.")
    require(memory.dataProvider().addFeature(prepared), "No s'ha pogut afegir l'entitat preparada.")
    memory.updateExtents()

    geopackage.parent.mkdir(parents=True, exist_ok=True)
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "GPKG"
    options.layerName = LOCAL_LAYER
    options.fileEncoding = "UTF-8"
    options.actionOnExistingFile = QgsVectorFileWriter.ActionOnExistingFile.CreateOrOverwriteFile
    options.layerOptions = ["FID=fid", "GEOMETRY_NAME=geom", "SPATIAL_INDEX=YES"]
    error, _, _, error_message = QgsVectorFileWriter.writeAsVectorFormatV3(
        memory,
        str(geopackage),
        QgsProject.instance().transformContext(),
        options,
    )
    require(
        error == QgsVectorFileWriter.WriterError.NoError,
        f"No s'ha pogut escriure el GeoPackage: {error_message or error}",
    )

    del prepared
    del memory
    del source_feature
    del source_features
    del source_layer
    gc.collect()

    with sqlite3.connect(geopackage) as connection:
        connection.execute(
            "CREATE UNIQUE INDEX idx_municipi_treball_id_origen ON municipi_treball(id_origen)"
        )
        connection.execute(
            "CREATE UNIQUE INDEX idx_municipi_treball_codi_muni ON municipi_treball(codi_muni)"
        )
        connection.execute(
            "UPDATE gpkg_contents SET identifier = ?, description = ?, last_change = ? WHERE table_name = ?",
            (
                "Limit municipal de Vila-seca",
                "Obra derivada de la unitat administrativa 1172246 de l'IGN/CNIG.",
                FIXED_GPKG_TIMESTAMP,
                LOCAL_LAYER,
            ),
        )
        connection.commit()


def set_layer_metadata(layer: QgsVectorLayer) -> None:
    metadata = QgsLayerMetadata()
    metadata.setIdentifier("IGN-CNIG-AU-1172246")
    metadata.setTitle("Limit municipal de Vila-seca")
    metadata.setAbstract(
        "Copia de treball de la unitat administrativa 1172246 de l'API OGC Features de l'IGN/CNIG."
    )
    metadata.setLanguage("ca")
    metadata.setLicenses(["CC BY 4.0 ign.es"])
    metadata.setRights(["Obra derivada de dades de l'IGN/CNIG."])
    layer.setMetadata(metadata)
    layer.setCustomProperty("tig/source_item_url", SOURCE_ITEM_URL)
    layer.setCustomProperty("tig/source_collection_url", SOURCE_COLLECTION_URL)
    layer.setCustomProperty("tig/source_licence_url", SOURCE_LICENCE_URL)
    layer.setCustomProperty("tig/source_access_date", "2026-09-08")
    layer.setCustomProperty("tig/source_canonical_sha256", CANONICAL_SOURCE_SHA256)
    layer.setCustomProperty("tig/codi_muni_rule", "right(nationalcode, 5)")


def set_project_metadata(project: QgsProject) -> None:
    metadata = QgsProjectMetadata()
    metadata.setIdentifier("tig-vila-seca-starter")
    metadata.setTitle("Projecte TIG: punt de partida de Vila-seca")
    metadata.setAbstract(
        "Projecte docent inicial amb el WMS PNOA de context i el limit municipal oficial preparat."
    )
    metadata.setAuthor("Dos quarts de docs")
    metadata.setLanguage("ca")
    fixed_datetime = QDateTime.fromString(FIXED_TIMESTAMP, Qt.DateFormat.ISODate)
    metadata.setCreationDateTime(fixed_datetime)
    project.setMetadata(metadata)


def geopackage_project_uri(geopackage: Path) -> str:
    encoded_path = quote(geopackage.resolve().as_posix(), safe="/")
    return f"geopackage:{encoded_path}?projectName={PROJECT_NAME}"


def write_qgis_projects(geopackage: Path, external_project: Path) -> None:
    project = QgsProject()
    project.setTitle("Projecte TIG: Vila-seca")
    project.setCrs(QgsCoordinateReferenceSystem(PROJECT_CRS))
    project.setFilePathStorage(Qgis.FilePathType.Relative)
    project.setPresetHomePath(".")
    set_project_metadata(project)
    project.writeEntry("tig", "source_item_id", SOURCE_ID)
    project.writeEntry("tig", "source_canonical_sha256", CANONICAL_SOURCE_SHA256)
    project.writeEntry("tig", "wms_layer", WMS_LAYER)
    project.writeEntry("tig", "access_date", "2026-09-08")

    local_layer = QgsVectorLayer(f"{geopackage}|layername={LOCAL_LAYER}", LOCAL_LAYER, "ogr")
    require(local_layer.isValid(), "QGIS no pot reobrir municipi_treball des del GeoPackage.")
    require(local_layer.setId(LOCAL_LAYER_ID), "No s'ha pogut fixar l'identificador de municipi_treball.")
    local_layer.setDisplayExpression("nom_muni")
    local_layer.setFieldAlias(local_layer.fields().indexFromName("id_origen"), "Identificador d'origen")
    local_layer.setFieldAlias(local_layer.fields().indexFromName("codi_oficial"), "Codi oficial")
    local_layer.setFieldAlias(local_layer.fields().indexFromName("codi_muni"), "Codi municipal")
    local_layer.setFieldAlias(local_layer.fields().indexFromName("nom_muni"), "Nom del municipi")
    set_layer_metadata(local_layer)
    symbol = QgsFillSymbol.createSimple(
        {
            "color": "255,255,255,35",
            "outline_color": "153,0,0,255",
            "outline_width": "0.8",
            "outline_width_unit": "MM",
        }
    )
    require(symbol is not None, "No s'ha pogut crear la simbologia municipal.")
    local_layer.setRenderer(QgsSingleSymbolRenderer(symbol))

    wms_layer = QgsRasterLayer(WMS_URI, WMS_NAME, "wms")
    require(wms_layer.isValid(), "QGIS no pot validar la capa WMS PNOA declarada.")
    require(wms_layer.setId(WMS_LAYER_ID), "No s'ha pogut fixar l'identificador de la capa WMS.")
    wms_layer.setCustomProperty("tig/source_role", "context")
    wms_layer.setCustomProperty("tig/source_access_date", "2026-09-08")
    wms_layer.setCustomProperty("tig/source_licence", "CC BY 4.0 scne.es")
    wms_layer.setCustomProperty(
        "tig/capabilities_url",
        "https://www.ign.es/wms-inspire/pnoa-ma?SERVICE=WMS&REQUEST=GetCapabilities",
    )

    root = project.layerTreeRoot()
    groups = {name: root.addGroup(name) for name in GROUP_NAMES}
    project.addMapLayer(wms_layer, False)
    groups["00_context"].addLayer(wms_layer)
    project.addMapLayer(local_layer, False)
    groups["20_preparades"].addLayer(local_layer)

    default_extent = QgsReferencedRectangle(local_layer.extent(), local_layer.crs())
    project.viewSettings().setDefaultViewExtent(default_extent)

    external_project.parent.mkdir(parents=True, exist_ok=True)
    require(project.write(str(external_project)), "QGIS no ha pogut escriure projecte_tig.qgz.")
    require(
        project.write(geopackage_project_uri(geopackage)),
        "QGIS no ha pogut escriure la fita projecte_tig al GeoPackage.",
    )

    project.clear()
    del project
    del local_layer
    del wms_layer
    gc.collect()


def normalize_project_xml(content: bytes) -> bytes:
    try:
        root = ElementTree.fromstring(content)
    except ElementTree.ParseError as error:
        raise BuildError("La definicio del projecte QGIS no es XML valid.") from error

    root.set("saveDateTime", FIXED_TIMESTAMP)
    root.set("saveUser", "unaltraweb")
    root.set("saveUserFull", "unaltraweb")

    author = root.find("./projectMetadata/author")
    require(author is not None, "El projecte QGIS no conte metadades d'autor.")
    author.text = "Dos quarts de docs"

    annotation_id = root.find("./main-annotation-layer/id")
    require(annotation_id is not None, "El projecte QGIS no conte la capa d'anotacions principal.")
    annotation_id.text = "Annotations_tig_vila_seca"

    style_settings = root.find("./ProjectStyleSettings")
    require(style_settings is not None, "El projecte QGIS no conte ProjectStyleSettings.")
    style_settings.set("projectStyleId", f"attachment:///{QGIS_STYLE_MEMBER}")
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
                        f"https://dosquartsdedocs.org/tig/vila-seca/qgis-id/{len(generated_ids)}",
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

    return QGIS_DOCTYPE + ElementTree.tostring(root, encoding="utf-8") + b"\n"


def normalize_qgis_archive(content: bytes) -> bytes:
    if not content.startswith(b"PK"):
        return normalize_project_xml(content)
    source = io.BytesIO(content)
    target = io.BytesIO()
    with zipfile.ZipFile(source, "r") as current:
        project_members = [member for member in current.infolist() if member.filename.endswith(".qgs")]
        style_members = [member for member in current.infolist() if member.filename.endswith("_styles.db")]
        require(len(project_members) == 1, "El projecte QGIS no conte una unica definicio .qgs.")
        require(len(style_members) == 1, "El projecte QGIS no conte una unica base d'estils.")
        members = [
            (QGIS_PROJECT_MEMBER, normalize_project_xml(current.read(project_members[0]))),
            (QGIS_STYLE_MEMBER, current.read(style_members[0])),
        ]

    with zipfile.ZipFile(
        target,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as normalized:
        for filename, payload in members:
            info = zipfile.ZipInfo(filename, FIXED_ZIP_TIME)
            info.create_system = 3
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o100644 & 0xFFFF) << 16
            normalized.writestr(info, payload)
    return target.getvalue()


def normalize_external_project(path: Path) -> None:
    path.write_bytes(normalize_qgis_archive(path.read_bytes()))


def normalize_geopackage(path: Path) -> None:
    with sqlite3.connect(path) as connection:
        projects = connection.execute(
            "SELECT name, content FROM qgis_projects ORDER BY name"
        ).fetchall()
        require([row[0] for row in projects] == [PROJECT_NAME], "El GeoPackage no conte una unica fita projecte_tig.")
        stored_content = projects[0][1]
        if isinstance(stored_content, bytes):
            stored_hex = stored_content.decode("ascii")
        else:
            stored_hex = str(stored_content)
        normalized = normalize_qgis_archive(bytes.fromhex(stored_hex))
        metadata = json.dumps(
            {
                "last_modified_time": FIXED_TIMESTAMP,
                "last_modified_user": "unaltraweb",
            },
            ensure_ascii=True,
            sort_keys=True,
            separators=(",", ":"),
        )
        connection.execute(
            "UPDATE qgis_projects SET metadata = ?, content = ? WHERE name = ?",
            (metadata, normalized.hex(), PROJECT_NAME),
        )
        connection.execute("UPDATE gpkg_contents SET last_change = ?", (FIXED_GPKG_TIMESTAMP,))
        connection.commit()
        connection.execute("PRAGMA journal_mode=DELETE")
        connection.execute("VACUUM")
        connection.commit()


def project_xml(content: bytes) -> bytes:
    if not content.startswith(b"PK"):
        return content
    with zipfile.ZipFile(io.BytesIO(content), "r") as archive:
        qgs_members = [name for name in archive.namelist() if name.endswith(".qgs")]
        require(len(qgs_members) == 1, "El projecte QGIS no conte una unica definicio .qgs.")
        return archive.read(qgs_members[0])


def embedded_project_content(geopackage: Path) -> bytes:
    with sqlite3.connect(geopackage) as connection:
        row = connection.execute(
            "SELECT content FROM qgis_projects WHERE name = ?",
            (PROJECT_NAME,),
        ).fetchone()
    require(row is not None, "No s'ha trobat la fita QGIS incrustada projecte_tig.")
    stored = row[0]
    stored_hex = stored.decode("ascii") if isinstance(stored, bytes) else str(stored)
    return bytes.fromhex(stored_hex)


def validate_portable_xml(content: bytes, expected_relative_source: str) -> None:
    require(
        content == normalize_qgis_archive(content),
        "El projecte QGIS no usa la serialitzacio canonica del paquet.",
    )
    xml = project_xml(content).decode("utf-8")
    require(expected_relative_source in xml, f"No s'ha trobat la font relativa {expected_relative_source}.")
    for forbidden in ("/workspace/", "/home/", "/tmp/", ".build-"):
        require(forbidden not in xml, f"El projecte conserva un cami no transportable: {forbidden}")


def validate_geopackage(geopackage: Path) -> dict[str, object]:
    require(geopackage.is_file(), f"Falta el GeoPackage: {geopackage}")
    with sqlite3.connect(geopackage) as connection:
        integrity = connection.execute("PRAGMA integrity_check").fetchone()
        require(integrity == ("ok",), f"La integritat SQLite ha fallat: {integrity}")
        projects = connection.execute("SELECT name FROM qgis_projects ORDER BY name").fetchall()
        require(projects == [(PROJECT_NAME,)], "La taula qgis_projects no conte exactament projecte_tig.")
        source_rows = connection.execute(
            "SELECT id_origen, codi_oficial, codi_muni, nom_muni, nivell, pais, codi_nut3 "
            "FROM municipi_treball"
        ).fetchall()
        require(
            source_rows
            == [(SOURCE_ID, SOURCE_NATIONAL_CODE, MUNICIPAL_CODE, "Vila-seca", "Municipio", "ES", "ES514")],
            f"Els atributs preparats no coincideixen amb el contracte: {source_rows}",
        )
        unique_indices = {
            row[1]
            for row in connection.execute("PRAGMA index_list('municipi_treball')").fetchall()
            if row[2] == 1
        }
        require(
            {
                "idx_municipi_treball_id_origen",
                "idx_municipi_treball_codi_muni",
            }.issubset(unique_indices),
            "Falten els indexs unics dels identificadors municipals.",
        )

    layer = QgsVectorLayer(f"{geopackage}|layername={LOCAL_LAYER}", LOCAL_LAYER, "ogr")
    require(layer.isValid(), "QGIS no pot obrir municipi_treball.")
    require(layer.featureCount() == 1, "municipi_treball no conte exactament una entitat.")
    require(layer.crs().authid() == PROJECT_CRS, f"municipi_treball no usa {PROJECT_CRS}.")
    require(tuple(layer.fields().names()) == FIELD_NAMES, f"Esquema inesperat: {layer.fields().names()}")
    feature = next(layer.getFeatures())
    require(not feature.geometry().isEmpty(), "La geometria preparada es buida.")
    require(feature.geometry().isGeosValid(), "La geometria preparada no es valida.")
    extent = layer.extent()
    summary = {
        "feature_count": layer.featureCount(),
        "crs": layer.crs().authid(),
        "fields": layer.fields().names(),
        "extent": [extent.xMinimum(), extent.yMinimum(), extent.xMaximum(), extent.yMaximum()],
    }
    del feature
    del layer
    gc.collect()
    return summary


def validate_project(path_or_uri: str, geopackage: Path) -> dict[str, object]:
    project = QgsProject()
    require(project.read(path_or_uri), f"QGIS no pot obrir el projecte: {path_or_uri}")
    require(project.crs().authid() == PROJECT_CRS, f"El projecte no usa {PROJECT_CRS}.")
    require(project.filePathStorage() == Qgis.FilePathType.Relative, "El projecte no desa camins relatius.")
    require(project.presetHomePath() == ".", "La carpeta inicial del projecte no es relativa.")
    actual_groups = tuple(child.name() for child in project.layerTreeRoot().children())
    require(actual_groups == GROUP_NAMES, f"Grups de projecte inesperats: {actual_groups}")

    local_layers = project.mapLayersByName(LOCAL_LAYER)
    require(len(local_layers) == 1, "El projecte no conte exactament una capa municipi_treball.")
    local_layer = local_layers[0]
    require(local_layer.id() == LOCAL_LAYER_ID, "L'identificador intern de municipi_treball ha canviat.")
    require(local_layer.isValid(), "La font local de municipi_treball no es resol.")
    require(local_layer.featureCount() == 1, "La capa local del projecte no conte una entitat.")
    require(local_layer.crs().authid() == PROJECT_CRS, "La capa local del projecte te un CRS inesperat.")
    local_path = Path(local_layer.source().split("|", 1)[0]).resolve()
    require(local_path == geopackage.resolve(), f"La capa local apunta fora del paquet: {local_path}")

    wms_layers = project.mapLayersByName(WMS_NAME)
    require(len(wms_layers) == 1, "El projecte no conte exactament una capa WMS PNOA.")
    wms_layer = wms_layers[0]
    require(wms_layer.id() == WMS_LAYER_ID, "L'identificador intern de la capa WMS ha canviat.")
    require(wms_layer.providerType() == "wms", "La capa de context no usa el proveidor WMS.")
    require(wms_layer.isValid(), "La capa WMS PNOA no respon durant la validacio.")
    require(WMS_LAYER in wms_layer.source(), "La font WMS no conserva OI.OrthoimageCoverage.")
    require("www.ign.es/wms-inspire/pnoa-ma" in wms_layer.source(), "La font WMS no apunta a l'IGN.")

    summary = {
        "title": project.title(),
        "crs": project.crs().authid(),
        "groups": list(actual_groups),
        "layers": sorted(layer.name() for layer in project.mapLayers().values()),
    }
    project.clear()
    del project
    del local_layer
    del wms_layer
    gc.collect()
    return summary


def copy_static_inputs(staging: Path) -> None:
    for relative in (Path("README.md"), Path("build_project.py"), Path("procedencia.yml")):
        source = PROJECT_ROOT / relative
        require(source.is_file(), f"Falta l'entrada estatica {source}.")
        destination = staging / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def write_checksums(root: Path) -> None:
    lines = []
    for relative in CHECKSUM_MEMBERS:
        path = root / relative
        require(path.is_file(), f"Falta el membre del paquet {relative}.")
        lines.append(f"{sha256_file(path)}  {relative.as_posix()}")
    (root / CHECKSUMS).write_text("\n".join(lines) + "\n", encoding="ascii")


def validate_checksums(root: Path) -> None:
    checksum_path = root / CHECKSUMS
    require(checksum_path.is_file(), f"Falta {checksum_path}.")
    observed_paths: list[Path] = []
    for line in checksum_path.read_text(encoding="ascii").splitlines():
        digest, separator, relative_text = line.partition("  ")
        require(separator == "  " and len(digest) == 64, f"Linia SHA-256 invalida: {line}")
        relative = Path(relative_text)
        require(not relative.is_absolute() and ".." not in relative.parts, f"Cami SHA-256 insegur: {relative}")
        path = root / relative
        require(path.is_file(), f"Falta el fitxer declarat a SHA256SUMS: {relative}")
        require(sha256_file(path) == digest, f"SHA-256 incorrecte: {relative}")
        observed_paths.append(relative)
    require(tuple(observed_paths) == CHECKSUM_MEMBERS, "L'inventari de SHA256SUMS no es l'esperat.")


def write_archive(root: Path, destination: Path) -> None:
    members = (*CHECKSUM_MEMBERS, CHECKSUMS)
    with zipfile.ZipFile(
        destination,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as archive:
        for relative in members:
            source = root / relative
            info = zipfile.ZipInfo(f"{ARCHIVE_ROOT}/{relative.as_posix()}", FIXED_ZIP_TIME)
            info.create_system = 3
            info.compress_type = zipfile.ZIP_DEFLATED
            mode = 0o100755 if relative == Path("build_project.py") else 0o100644
            info.external_attr = (mode & 0xFFFF) << 16
            archive.writestr(info, source.read_bytes())


def validate_package_files(root: Path) -> dict[str, object]:
    source_path = root / PUBLISHED_SOURCE
    _, canonical = canonical_source_bytes(source_path)
    require(source_path.read_bytes() == canonical, "El GeoJSON publicat no usa la serialitzacio canonica.")
    validate_checksums(root)
    geopackage = root / GEOPACKAGE
    external = root / EXTERNAL_PROJECT
    gpkg_summary = validate_geopackage(geopackage)
    validate_portable_xml(external.read_bytes(), "./dades_preparades/projecte_tig.gpkg")
    validate_portable_xml(embedded_project_content(geopackage), "./projecte_tig.gpkg")
    external_summary = validate_project(str(external), geopackage)
    embedded_summary = validate_project(geopackage_project_uri(geopackage), geopackage)
    require(
        external_summary == embedded_summary,
        "El projecte extern i la fita incrustada no representen el mateix estat.",
    )
    return {
        "source_sha256": sha256_file(source_path),
        "geopackage": gpkg_summary,
        "project": external_summary,
    }


def validate_archive(path: Path) -> dict[str, object]:
    require(path.is_file(), f"Falta l'arxiu de distribucio: {path}")
    expected = {
        f"{ARCHIVE_ROOT}/{relative.as_posix()}"
        for relative in (*CHECKSUM_MEMBERS, CHECKSUMS)
    }
    with zipfile.ZipFile(path, "r") as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), "El ZIP conte membres duplicats.")
        require(set(names) == expected, f"Inventari ZIP inesperat: {names}")
        for info in archive.infolist():
            member = Path(info.filename)
            require(not member.is_absolute() and ".." not in member.parts, f"Membre ZIP insegur: {info.filename}")
            require(info.date_time == FIXED_ZIP_TIME, f"Marca temporal ZIP no normalitzada: {info.filename}")
        with tempfile.TemporaryDirectory(prefix=".transport-", dir=PROJECT_ROOT) as temporary:
            archive.extractall(temporary)
            extracted_root = Path(temporary) / ARCHIVE_ROOT
            return validate_package_files(extracted_root)


def publish(staging: Path, archive_path: Path) -> None:
    outputs = (PUBLISHED_SOURCE, GEOPACKAGE, EXTERNAL_PROJECT, CHECKSUMS)
    for relative in outputs:
        source = staging / relative
        destination = PROJECT_ROOT / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        os.replace(source, destination)
    os.replace(archive_path, PROJECT_ROOT / ARCHIVE)


def build(source: Path) -> dict[str, object]:
    require(source.is_file(), f"No s'ha trobat la font descarregada: {source}")
    with tempfile.TemporaryDirectory(prefix=".build-", dir=PROJECT_ROOT) as temporary:
        staging = Path(temporary)
        copy_static_inputs(staging)
        canonical_path = staging / PUBLISHED_SOURCE
        geopackage = staging / GEOPACKAGE
        external = staging / EXTERNAL_PROJECT
        archive_path = staging / ARCHIVE

        write_canonical_source(source, canonical_path)
        build_prepared_layer(canonical_path, geopackage)
        write_qgis_projects(geopackage, external)
        normalize_external_project(external)
        normalize_geopackage(geopackage)
        write_checksums(staging)
        validate_package_files(staging)
        write_archive(staging, archive_path)
        transport_summary = validate_archive(archive_path)
        archive_hash = sha256_file(archive_path)
        archive_size = archive_path.stat().st_size
        publish(staging, archive_path)

    return {
        "ok": True,
        "mode": "build",
        "source": str(source),
        "archive_sha256": archive_hash,
        "archive_bytes": archive_size,
        **transport_summary,
    }


def check() -> dict[str, object]:
    package_summary = validate_package_files(PROJECT_ROOT)
    archive_summary = validate_archive(PROJECT_ROOT / ARCHIVE)
    require(package_summary == archive_summary, "El ZIP no coincideix amb els fitxers publicats.")
    return {
        "ok": True,
        "mode": "check",
        "archive_sha256": sha256_file(PROJECT_ROOT / ARCHIVE),
        "archive_bytes": (PROJECT_ROOT / ARCHIVE).stat().st_size,
        **package_summary,
    }


def default_source() -> Path:
    if DEFAULT_DOWNLOADED_SOURCE.is_file():
        return DEFAULT_DOWNLOADED_SOURCE
    return PROJECT_ROOT / PUBLISHED_SOURCE


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        type=Path,
        help="Resposta JSON descarregada; per defecte usa la memoria cau o la copia publicada.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Valida el paquet publicat sense regenerar-lo.",
    )
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    QgsApplication.setPrefixPath("/usr", True)
    application = QgsApplication([], False)
    application.initQgis()
    try:
        result = check() if arguments.check else build((arguments.source or default_source()).resolve())
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
