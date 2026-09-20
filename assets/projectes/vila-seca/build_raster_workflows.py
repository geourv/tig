#!/usr/bin/env python3
"""Build and validate the ignored raster inputs used by the QGIS captures."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sqlite3
import tempfile

import numpy as np
from osgeo import gdal, ogr, osr


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
CACHE_ROOT = REPOSITORY_ROOT / "tmp/unaltracaptura-qgis/cache"
SOURCE_ROOT = CACHE_ROOT / "prepared"
OUTPUT_ROOT = SOURCE_ROOT / "terrain/vila-seca"
CUTLINE = (
    REPOSITORY_ROOT
    / "assets/projectes/vila-seca/dades_originals/vila-seca-cnig.geojson"
)

MDT25_0472 = (
    SOURCE_ROOT / "cnig/mdt25/source/pnoa_mdt25_etrs89_hu31_0472_lid.tif"
)
MDT25_0473 = (
    SOURCE_ROOT / "cnig/mdt25/source/pnoa_mdt25_etrs89_hu31_0473_lid.tif"
)
MDT200_TARRAGONA = (
    SOURCE_ROOT / "cnig/mdt200/source/pnoa_mdt200_etrs89_hu31_tarragona.tif"
)
ORTHOPHOTO_SOURCE = (
    SOURCE_ROOT
    / "icgc/orthophoto/source/ortofoto_territorial_2025_vila_seca.jpg"
)
ORTHOPHOTO_FACULTY_SOURCE = (
    SOURCE_ROOT
    / "icgc/orthophoto/source/ortofoto_territorial_2025_facultat.jpg"
)
TARRAGONA_BOUNDARY_RAW = (
    SOURCE_ROOT / "cnig/administrative-units/tarragona-cnig.raw.json"
)
TARRAGONA_BOUNDARY = (
    SOURCE_ROOT / "cnig/administrative-units/tarragona-cnig.geojson"
)
TARRAGONA_BOUNDARY_SHA256 = "eda078ca366dc266a9f502adf1cefeb5b91f91f22b463d34f0d2bc7556c912b2"

SOURCE_HASHES = {
    MDT25_0472: "325b8028bc99d4726cfdd9cb777de0ac06ed815a62da2b0e313c0c17daf4bb7c",
    MDT25_0473: "827b2a41b61a9636178847137647fb46f07d4f227165279d1487e757921f22bf",
    MDT200_TARRAGONA: "1827b96fd3c2d1f7cc6cb41b169fecd98ecade31581debc5264158aa3b65b118",
    ORTHOPHOTO_SOURCE: "fa264bc73ea837dd5c44c08f3e9836330961a9670fa4ee265034900810f290d8",
    ORTHOPHOTO_FACULTY_SOURCE: "61a8235709f0770228018b5bcaae308c0abf52c91505b02a77cb689525fb00b7",
    TARRAGONA_BOUNDARY: TARRAGONA_BOUNDARY_SHA256,
    CUTLINE: "abf389424da192263a1f44a569a8f5c9ffb6eeaec5245b22932fb0859831f321",
}

LOW_ELEVATION_DISTANCE = "distancia_zones_baixes_25m_vila_seca.tif"
OUTPUT_NAMES = (
    "mdt25_0472_0473_mosaic.tif",
    "mdt25_vila_seca.tif",
    "mdt200_vila_seca.tif",
    "ortofoto_territorial_2025_vila_seca.tif",
    "ortofoto_territorial_2025_facultat.tif",
    "pendent_25m_graus_vila_seca.tif",
    "pendent_25m_percent_vila_seca.tif",
    "orientacio_25m_graus_vila_seca.tif",
    "orientacio_sectors_25m_vila_seca.tif",
    "elevacio_classes_25m_vila_seca.tif",
    LOW_ELEVATION_DISTANCE,
    "orientacio_sud_25m_vila_seca.tif",
)
OUTPUT_HASHES = {
    "mdt25_0472_0473_mosaic.tif": "7e00f20a23611ba192cc7723cddafc72191af2b6888a76a7d00abe6f3306cb6d",
    "mdt25_vila_seca.tif": "f3f4da904ae1c1fa0c23eb47a5f2c2a2b7f478883efbe930c70ec947098b47b9",
    "mdt200_vila_seca.tif": "bcc83b4f63ec81cc4144ff005732c25db309c6cf46e9770dbbc841277399fee2",
    "ortofoto_territorial_2025_vila_seca.tif": "8cfdb39b6fce124844644087bc39a365da9bcef6401286644590b60c4fd07ad0",
    "ortofoto_territorial_2025_facultat.tif": "d890c966db18f4a3ee4b260981b4446d2c6fb470fa78a7025cb75647120cf7d7",
    "pendent_25m_graus_vila_seca.tif": "39b479da22f1c27048d38bed340d9ebcbd0f2afd695cf2aa632462d839aebd06",
    "pendent_25m_percent_vila_seca.tif": "9da6a4daf8b38f2b10c254d0cd075d34112e4c156405bd4a166ffc1ece287c46",
    "orientacio_25m_graus_vila_seca.tif": "a37d92ee064e90539111c0aa38b7a92e492b5eecb18541579f9a113d64d9aa5c",
    "orientacio_sectors_25m_vila_seca.tif": "e6944c2e17ac1d69ecd5a2ca4d5b32907bf1dc127ef1e5390c3cd335345062d1",
    "elevacio_classes_25m_vila_seca.tif": "8b3f58ef4c9f76d32f1aefd191376c045fd1b647f1310f6b0221ffe023c78b6d",
    LOW_ELEVATION_DISTANCE: "c2f4fb70dce25bb358c704bf73034898fba3086738eec7673ebee5feb26f28db",
    "orientacio_sud_25m_vila_seca.tif": "4370d6fd4e0fc00356177f75742ea5fa552cacbe970b9ae8fe30ac1b425c6e0e",
}
LOW_ELEVATION_VECTOR = "zones_baixes_2m_vila_seca.gpkg"
LOW_ELEVATION_LAYER = "zones_baixes_2m"
LOW_ELEVATION_SHA256 = "b1a7cf497806b1528fa6ef7290dbe3a48f4ec05af5a209f5e452b446bc1ac4dc"
GPKG_LAST_CHANGE = "1970-01-01T00:00:00.000Z"

FLOAT_NODATA = -32767.0
CLASS_NODATA = 255
ORTHOPHOTO_BOUNDS = (339500.0, 4547500.0, 349900.0, 4555300.0)
ORTHOPHOTO_FACULTY_BOUNDS = (344250.0, 4551600.0, 344700.0, 4552050.0)
GTIFF_OPTIONS = [
    "TILED=YES",
    "COMPRESS=DEFLATE",
    "PREDICTOR=3",
    "BIGTIFF=IF_SAFER",
]


class BuildError(RuntimeError):
    """Raised when a source or generated raster violates the contract."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise BuildError(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonicalize_tarragona_boundary() -> None:
    require(TARRAGONA_BOUNDARY_RAW.is_file(), f"Missing source: {TARRAGONA_BOUNDARY_RAW}")
    try:
        payload = json.loads(TARRAGONA_BOUNDARY_RAW.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise BuildError(f"Cannot read Tarragona boundary JSON: {error}") from error

    require(isinstance(payload, dict), "The Tarragona boundary is not a JSON object")
    properties = payload.get("properties")
    geometry = payload.get("geometry")
    require(payload.get("type") == "Feature", "The Tarragona boundary is not a GeoJSON Feature")
    require(str(payload.get("id")) == "1174500", "Unexpected Tarragona boundary identifier")
    require(isinstance(properties, dict), "The Tarragona boundary has no properties object")
    require(properties.get("nameunit") == "Tarragona", "Unexpected administrative unit name")
    require(properties.get("nationallevelname") == "Provincia", "Unexpected administrative level")
    require(properties.get("nationalcode") == "34094300000", "Unexpected Tarragona national code")
    require(properties.get("country") == "ES", "Unexpected Tarragona country code")
    require(properties.get("codnut1") == "ES5", "Unexpected Tarragona NUTS 1 code")
    require(properties.get("codnut2") == "ES51", "Unexpected Tarragona NUTS 2 code")
    require(isinstance(geometry, dict), "The Tarragona boundary has no geometry")
    require(geometry.get("type") == "MultiPolygon", "The Tarragona boundary is not a MultiPolygon")
    require(bool(geometry.get("coordinates")), "The Tarragona boundary has no coordinates")

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
    actual_hash = hashlib.sha256(canonical).hexdigest()
    require(
        actual_hash == TARRAGONA_BOUNDARY_SHA256,
        "Canonical Tarragona boundary content changed: "
        f"expected {TARRAGONA_BOUNDARY_SHA256}, got {actual_hash}",
    )
    TARRAGONA_BOUNDARY.parent.mkdir(parents=True, exist_ok=True)
    TARRAGONA_BOUNDARY.write_bytes(canonical)


def verify_sources() -> None:
    for path, expected in SOURCE_HASHES.items():
        require(path.is_file(), f"Missing source: {path}")
        actual = sha256_file(path)
        require(actual == expected, f"SHA-256 mismatch for {path}: {actual}")


def open_raster(path: Path) -> gdal.Dataset:
    dataset = gdal.Open(str(path), gdal.GA_ReadOnly)
    require(dataset is not None, f"Cannot open raster: {path}")
    return dataset


def raster_bounds(dataset: gdal.Dataset) -> tuple[float, float, float, float]:
    transform = dataset.GetGeoTransform()
    min_x = transform[0]
    max_y = transform[3]
    max_x = min_x + dataset.RasterXSize * transform[1]
    min_y = max_y + dataset.RasterYSize * transform[5]
    return min_x, min_y, max_x, max_y


def municipality_bounds() -> tuple[float, float, float, float]:
    datasource = ogr.Open(str(CUTLINE))
    require(datasource is not None, f"Cannot open cutline: {CUTLINE}")
    layer = datasource.GetLayer(0)
    require(layer is not None, "The municipal cutline has no layer")
    source_srs = layer.GetSpatialRef()
    if source_srs is None:
        source_srs = osr.SpatialReference()
        source_srs.ImportFromEPSG(4326)
    target_srs = osr.SpatialReference()
    target_srs.ImportFromEPSG(25831)
    transform = osr.CoordinateTransformation(source_srs, target_srs)
    feature = layer.GetNextFeature()
    require(feature is not None, "The municipal cutline has no feature")
    geometry = feature.GetGeometryRef().Clone()
    geometry.Transform(transform)
    min_x, max_x, min_y, max_y = geometry.GetEnvelope()
    return min_x, min_y, max_x, max_y


def snap_bounds(
    dataset: gdal.Dataset,
    bounds: tuple[float, float, float, float],
) -> tuple[float, float, float, float]:
    transform = dataset.GetGeoTransform()
    require(transform[2] == 0 and transform[4] == 0, "Rotated grids are unsupported")
    pixel_x = transform[1]
    pixel_y = abs(transform[5])
    origin_x = transform[0]
    origin_y = transform[3]
    min_x, min_y, max_x, max_y = bounds
    snapped_min_x = origin_x + math.floor((min_x - origin_x) / pixel_x) * pixel_x
    snapped_max_x = origin_x + math.ceil((max_x - origin_x) / pixel_x) * pixel_x
    snapped_max_y = origin_y - math.floor((origin_y - max_y) / pixel_y) * pixel_y
    snapped_min_y = origin_y - math.ceil((origin_y - min_y) / pixel_y) * pixel_y
    return snapped_min_x, snapped_min_y, snapped_max_x, snapped_max_y


def build_mosaic(destination: Path, temporary_root: Path) -> None:
    vrt_path = temporary_root / "mdt25_mosaic.vrt"
    options = gdal.BuildVRTOptions(
        resolution="highest",
        srcNodata=FLOAT_NODATA,
        VRTNodata=FLOAT_NODATA,
        addAlpha=False,
    )
    vrt = gdal.BuildVRT(str(vrt_path), [str(MDT25_0472), str(MDT25_0473)], options=options)
    require(vrt is not None, "GDAL could not build the MDT25 mosaic VRT")
    vrt.FlushCache()
    vrt = None
    translated = gdal.Translate(
        str(destination),
        str(vrt_path),
        options=gdal.TranslateOptions(
            format="GTiff",
            outputType=gdal.GDT_Float32,
            noData=FLOAT_NODATA,
            creationOptions=GTIFF_OPTIONS,
            overviewLevel="NONE",
        ),
    )
    require(translated is not None, "GDAL could not materialize the MDT25 mosaic")
    translated.FlushCache()


def clip_to_municipality(
    source: Path,
    destination: Path,
    source_nodata: float,
) -> None:
    dataset = open_raster(source)
    bounds = snap_bounds(dataset, municipality_bounds())
    transform = dataset.GetGeoTransform()
    output = gdal.Warp(
        str(destination),
        dataset,
        options=gdal.WarpOptions(
            format="GTiff",
            outputBounds=bounds,
            xRes=transform[1],
            yRes=abs(transform[5]),
            dstSRS=dataset.GetProjection(),
            resampleAlg="near",
            srcNodata=source_nodata,
            dstNodata=FLOAT_NODATA,
            cutlineDSName=str(CUTLINE),
            cropToCutline=False,
            multithread=False,
            overviewLevel="NONE",
            outputType=gdal.GDT_Float32,
            creationOptions=GTIFF_OPTIONS,
        ),
    )
    require(output is not None, f"GDAL could not clip {source.name}")
    output.FlushCache()


def georeference_orthophoto(source: Path, destination: Path, bounds: tuple[float, ...]) -> None:
    min_x, min_y, max_x, max_y = bounds
    output = gdal.Translate(
        str(destination),
        str(source),
        options=gdal.TranslateOptions(
            format="GTiff",
            outputSRS="EPSG:25831",
            outputBounds=(min_x, max_y, max_x, min_y),
            creationOptions=["TILED=YES", "COMPRESS=DEFLATE", "BIGTIFF=IF_SAFER"],
        ),
    )
    require(output is not None, f"GDAL could not georeference {source.name}")
    output.FlushCache()


def terrain_derivative(
    source: Path,
    destination: Path,
    mode: str,
    slope_format: str | None = None,
) -> None:
    options = gdal.DEMProcessingOptions(
        format="GTiff",
        computeEdges=False,
        alg="Horn",
        band=1,
        scale=1.0,
        slopeFormat=slope_format,
        trigonometric=False,
        zeroForFlat=False,
        creationOptions=GTIFF_OPTIONS,
    )
    output = gdal.DEMProcessing(str(destination), str(source), mode, options=options)
    require(output is not None, f"GDAL could not calculate {mode}")
    output.FlushCache()


def write_classified(
    destination: Path,
    template_path: Path,
    values: np.ndarray,
    colours: dict[int, tuple[int, int, int, int]],
    labels: list[str],
) -> None:
    template = open_raster(template_path)
    driver = gdal.GetDriverByName("GTiff")
    output = driver.Create(
        str(destination),
        template.RasterXSize,
        template.RasterYSize,
        1,
        gdal.GDT_Byte,
        options=[
            "TILED=YES",
            "COMPRESS=DEFLATE",
            "PHOTOMETRIC=PALETTE",
            "BIGTIFF=IF_SAFER",
        ],
    )
    require(output is not None, f"Cannot create classified raster: {destination}")
    output.SetGeoTransform(template.GetGeoTransform())
    output.SetProjection(template.GetProjection())
    band = output.GetRasterBand(1)
    band.SetNoDataValue(CLASS_NODATA)
    colour_table = gdal.ColorTable()
    for value, colour in colours.items():
        colour_table.SetColorEntry(value, colour)
    colour_table.SetColorEntry(CLASS_NODATA, (0, 0, 0, 0))
    band.SetRasterColorInterpretation(gdal.GCI_PaletteIndex)
    band.SetRasterColorTable(colour_table)
    band.SetCategoryNames(labels)
    band.WriteArray(values)
    band.FlushCache()
    output.FlushCache()


def classify_outputs(root: Path) -> dict[str, float | int]:
    elevation_path = root / "mdt25_vila_seca.tif"
    slope_path = root / "pendent_25m_graus_vila_seca.tif"
    aspect_path = root / "orientacio_25m_graus_vila_seca.tif"

    elevation_dataset = open_raster(elevation_path)
    slope_dataset = open_raster(slope_path)
    aspect_dataset = open_raster(aspect_path)
    elevation_band = elevation_dataset.GetRasterBand(1)
    slope_band = slope_dataset.GetRasterBand(1)
    aspect_band = aspect_dataset.GetRasterBand(1)
    elevation = elevation_band.ReadAsArray()
    slope = slope_band.ReadAsArray()
    aspect = aspect_band.ReadAsArray()
    valid = (
        (elevation != FLOAT_NODATA)
        & (slope != FLOAT_NODATA)
        & (aspect != FLOAT_NODATA)
        & np.isfinite(elevation)
        & np.isfinite(slope)
        & np.isfinite(aspect)
    )

    elevation_classes = np.full(elevation.shape, CLASS_NODATA, dtype=np.uint8)
    elevation_classes[valid & (elevation < 2.0)] = 1
    elevation_classes[valid & (elevation >= 2.0)] = 2
    write_classified(
        root / "elevacio_classes_25m_vila_seca.tif",
        elevation_path,
        elevation_classes,
        {1: (44, 123, 182, 255), 2: (222, 184, 135, 255)},
        ["Sense classificar", "Per sota de 2 m", "2 m o més"],
    )

    sectors = np.full(elevation.shape, CLASS_NODATA, dtype=np.uint8)
    directional = valid & (slope >= 2.0)
    sectors[valid & ~directional] = 0
    sectors[directional & ((aspect >= 315.0) | (aspect < 45.0))] = 1
    sectors[directional & (aspect >= 45.0) & (aspect < 135.0)] = 2
    sectors[directional & (aspect >= 135.0) & (aspect < 225.0)] = 3
    sectors[directional & (aspect >= 225.0) & (aspect < 315.0)] = 4
    write_classified(
        root / "orientacio_sectors_25m_vila_seca.tif",
        elevation_path,
        sectors,
        {
            0: (210, 210, 210, 255),
            1: (69, 117, 180, 255),
            2: (250, 196, 79, 255),
            3: (196, 67, 62, 255),
            4: (136, 99, 163, 255),
        },
        ["Pla (< 2 graus)", "Nord", "Est", "Sud", "Oest"],
    )

    south = np.full(elevation.shape, CLASS_NODATA, dtype=np.uint8)
    south[valid] = 0
    south[directional & (aspect >= 135.0) & (aspect < 225.0)] = 1
    write_classified(
        root / "orientacio_sud_25m_vila_seca.tif",
        elevation_path,
        south,
        {0: (215, 215, 215, 150), 1: (230, 85, 13, 255)},
        ["Altres cel·les", "Orientació sud"],
    )

    valid_count = int(valid.sum())
    low_count = int((valid & (elevation < 2.0)).sum())
    south_count = int((south == 1).sum())
    return {
        "valid_cells": valid_count,
        "below_2m_cells": low_count,
        "below_2m_percent": 100.0 * low_count / valid_count,
        "south_facing_cells": south_count,
        "south_facing_percent": 100.0 * south_count / valid_count,
    }


def build_low_elevation_distance(root: Path) -> None:
    source = open_raster(root / "elevacio_classes_25m_vila_seca.tif")
    source_band = source.GetRasterBand(1)
    destination = root / LOW_ELEVATION_DISTANCE
    driver = gdal.GetDriverByName("GTiff")
    output = driver.Create(
        str(destination),
        source.RasterXSize,
        source.RasterYSize,
        1,
        gdal.GDT_Float32,
        options=GTIFF_OPTIONS,
    )
    require(output is not None, f"Cannot create distance raster: {destination}")
    output.SetGeoTransform(source.GetGeoTransform())
    output.SetProjection(source.GetProjection())
    output_band = output.GetRasterBand(1)
    output_band.SetNoDataValue(FLOAT_NODATA)
    output_band.Fill(FLOAT_NODATA)
    require(
        gdal.ComputeProximity(
            source_band,
            output_band,
            options=[
                "VALUES=1",
                "DISTUNITS=GEO",
                "USE_INPUT_NODATA=YES",
                f"NODATA={int(FLOAT_NODATA)}",
            ],
        )
        == 0,
        "GDAL could not calculate proximity to low-elevation cells",
    )
    output_band.FlushCache()
    output.FlushCache()
    output = None
    source = None


def polygonize_low_elevation(root: Path) -> None:
    source = open_raster(root / "elevacio_classes_25m_vila_seca.tif")
    source_band = source.GetRasterBand(1)
    classes = source_band.ReadAsArray()

    memory_driver = gdal.GetDriverByName("MEM")
    mask = memory_driver.Create(
        "",
        source.RasterXSize,
        source.RasterYSize,
        1,
        gdal.GDT_Byte,
    )
    require(mask is not None, "Cannot create the low-elevation mask")
    mask.SetGeoTransform(source.GetGeoTransform())
    mask.SetProjection(source.GetProjection())
    mask_band = mask.GetRasterBand(1)
    mask_band.SetNoDataValue(0)
    mask_band.WriteArray((classes == 1).astype(np.uint8))
    mask_band.FlushCache()

    destination = root / LOW_ELEVATION_VECTOR
    vector_driver = ogr.GetDriverByName("GPKG")
    require(vector_driver is not None, "The GPKG driver is unavailable")
    if destination.exists():
        vector_driver.DeleteDataSource(str(destination))
    datasource = vector_driver.CreateDataSource(str(destination))
    require(datasource is not None, f"Cannot create vector output: {destination}")
    spatial_reference = osr.SpatialReference()
    require(
        spatial_reference.ImportFromWkt(source.GetProjection()) == 0,
        "Cannot read the raster spatial reference",
    )
    layer = datasource.CreateLayer(
        LOW_ELEVATION_LAYER,
        srs=spatial_reference,
        geom_type=ogr.wkbPolygon,
        options=["GEOMETRY_NAME=geom", "SPATIAL_INDEX=YES", "FID=fid"],
    )
    require(layer is not None, "Cannot create the low-elevation vector layer")
    for field in (
        ogr.FieldDefn("classe", ogr.OFTInteger),
        ogr.FieldDefn("llindar_m", ogr.OFTReal),
        ogr.FieldDefn("area_m2", ogr.OFTReal),
        ogr.FieldDefn("criteri", ogr.OFTString),
    ):
        require(layer.CreateField(field) == 0, f"Cannot create field {field.GetName()}")
    require(
        gdal.Polygonize(mask_band, mask_band, layer, 0) == 0,
        "GDAL could not vectorize the low-elevation cells",
    )
    layer.ResetReading()
    for feature in layer:
        geometry = feature.GetGeometryRef()
        require(geometry is not None and not geometry.IsEmpty(), "Empty polygonized geometry")
        feature.SetField("llindar_m", 2.0)
        feature.SetField("area_m2", geometry.GetArea())
        feature.SetField("criteri", "elevacio_m < 2")
        require(layer.SetFeature(feature) == 0, "Cannot complete polygon attributes")
    datasource.FlushCache()
    datasource = None
    with sqlite3.connect(destination) as connection:
        connection.execute(
            "UPDATE gpkg_contents SET last_change = ?",
            (GPKG_LAST_CHANGE,),
        )
        connection.commit()
        connection.execute("VACUUM")
    mask = None
    source = None


def build() -> dict[str, object]:
    canonicalize_tarragona_boundary()
    verify_sources()
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="raster-workflows-", dir=OUTPUT_ROOT.parent) as temporary:
        temporary_root = Path(temporary)
        mosaic = temporary_root / "mdt25_0472_0473_mosaic.tif"
        build_mosaic(mosaic, temporary_root)
        clip_to_municipality(mosaic, temporary_root / "mdt25_vila_seca.tif", FLOAT_NODATA)
        clip_to_municipality(
            MDT200_TARRAGONA,
            temporary_root / "mdt200_vila_seca.tif",
            FLOAT_NODATA,
        )
        georeference_orthophoto(
            ORTHOPHOTO_SOURCE,
            temporary_root / "ortofoto_territorial_2025_vila_seca.tif",
            ORTHOPHOTO_BOUNDS,
        )
        georeference_orthophoto(
            ORTHOPHOTO_FACULTY_SOURCE,
            temporary_root / "ortofoto_territorial_2025_facultat.tif",
            ORTHOPHOTO_FACULTY_BOUNDS,
        )

        slope_degrees_full = temporary_root / "pendent_25m_graus_full.tif"
        slope_percent_full = temporary_root / "pendent_25m_percent_full.tif"
        aspect_full = temporary_root / "orientacio_25m_graus_full.tif"
        terrain_derivative(mosaic, slope_degrees_full, "slope", "degree")
        terrain_derivative(mosaic, slope_percent_full, "slope", "percent")
        terrain_derivative(mosaic, aspect_full, "aspect")
        clip_to_municipality(
            slope_degrees_full,
            temporary_root / "pendent_25m_graus_vila_seca.tif",
            -9999.0,
        )
        clip_to_municipality(
            slope_percent_full,
            temporary_root / "pendent_25m_percent_vila_seca.tif",
            -9999.0,
        )
        clip_to_municipality(
            aspect_full,
            temporary_root / "orientacio_25m_graus_vila_seca.tif",
            -9999.0,
        )
        metrics = classify_outputs(temporary_root)
        build_low_elevation_distance(temporary_root)
        polygonize_low_elevation(temporary_root)

        validate_outputs(temporary_root)

        for name in OUTPUT_NAMES:
            source = temporary_root / name
            require(source.is_file(), f"Expected output was not created: {name}")
            source.replace(OUTPUT_ROOT / name)
        vector_source = temporary_root / LOW_ELEVATION_VECTOR
        require(vector_source.is_file(), f"Expected output was not created: {LOW_ELEVATION_VECTOR}")
        vector_source.replace(OUTPUT_ROOT / LOW_ELEVATION_VECTOR)

    report = validate_outputs()
    report["metrics"] = metrics
    return report


def valid_array(path: Path) -> np.ndarray:
    dataset = open_raster(path)
    band = dataset.GetRasterBand(1)
    values = band.ReadAsArray()
    nodata = band.GetNoDataValue()
    return values[np.isfinite(values) & (values != nodata)]


def validate_outputs(root: Path = OUTPUT_ROOT) -> dict[str, object]:
    verify_sources()
    outputs: dict[str, object] = {}
    for name in OUTPUT_NAMES:
        path = root / name
        require(path.is_file(), f"Missing generated output: {path}")
        dataset = open_raster(path)
        require(dataset.GetRasterBand(1).GetOverviewCount() == 0, f"Unexpected overview: {name}")
        output_sha256 = sha256_file(path)
        require(
            output_sha256 == OUTPUT_HASHES[name],
            f"SHA-256 mismatch for {path}: {output_sha256}",
        )
        outputs[name] = {
            "sha256": output_sha256,
            "size": path.stat().st_size,
            "width": dataset.RasterXSize,
            "height": dataset.RasterYSize,
            "bands": dataset.RasterCount,
            "bounds": [round(value, 3) for value in raster_bounds(dataset)],
            "pixel_size": [
                dataset.GetGeoTransform()[1],
                abs(dataset.GetGeoTransform()[5]),
            ],
        }

    classes_dataset = open_raster(root / "elevacio_classes_25m_vila_seca.tif")
    distance_dataset = open_raster(root / LOW_ELEVATION_DISTANCE)
    require(
        (distance_dataset.RasterXSize, distance_dataset.RasterYSize) == (382, 294),
        "Unexpected distance-raster dimensions",
    )
    require(
        distance_dataset.GetGeoTransform()
        == (339912.5, 25.0, 0.0, 4554987.5, 0.0, -25.0),
        "Unexpected distance-raster geotransform",
    )
    require(
        distance_dataset.GetProjection() == classes_dataset.GetProjection(),
        "Distance raster does not preserve the classified-raster CRS",
    )
    distance_srs = osr.SpatialReference(wkt=distance_dataset.GetProjection())
    require(
        distance_srs.GetAuthorityCode(None) == "25831",
        "Distance raster does not use EPSG:25831",
    )
    classes_band = classes_dataset.GetRasterBand(1)
    distance_band = distance_dataset.GetRasterBand(1)
    require(distance_band.DataType == gdal.GDT_Float32, "Distance raster is not Float32")
    require(
        distance_band.GetNoDataValue() == FLOAT_NODATA,
        "Unexpected distance-raster NoData value",
    )
    classes = classes_band.ReadAsArray()
    distances = distance_band.ReadAsArray()
    valid_mask = distances != FLOAT_NODATA
    require(
        np.array_equal(~valid_mask, classes == CLASS_NODATA),
        "Distance and classification NoData masks differ",
    )
    require(
        np.array_equal(distances == 0, classes == 1),
        "Zero-distance cells do not match class 1",
    )
    valid_distances = distances[valid_mask]
    distance_metrics = {
        "valid_cells": int(valid_mask.sum()),
        "zero_distance_cells": int((distances == 0).sum()),
        "positive_distance_cells": int((distances > 0).sum()),
        "minimum_m": float(valid_distances.min()),
        "maximum_m": float(valid_distances.max()),
        "mean_m": float(valid_distances.mean(dtype=np.float64)),
    }
    require(distance_metrics["valid_cells"] == 34734, "Unexpected valid distance-cell count")
    require(distance_metrics["zero_distance_cells"] == 2150, "Unexpected source-cell count")
    require(distance_metrics["positive_distance_cells"] == 32584, "Unexpected positive-distance count")
    require(distance_metrics["minimum_m"] == 0.0, "Unexpected minimum distance")
    require(
        math.isclose(distance_metrics["maximum_m"], 7100.4404296875, abs_tol=1e-6),
        f"Unexpected maximum distance: {distance_metrics['maximum_m']}",
    )
    require(
        math.isclose(distance_metrics["mean_m"], 3175.079243175146, abs_tol=1e-6),
        f"Unexpected mean distance: {distance_metrics['mean_m']}",
    )
    outputs[LOW_ELEVATION_DISTANCE]["metrics"] = distance_metrics
    classes_dataset = None
    distance_dataset = None

    vector_path = root / LOW_ELEVATION_VECTOR
    require(vector_path.is_file(), f"Missing generated output: {vector_path}")
    vector_datasource = ogr.Open(str(vector_path))
    require(vector_datasource is not None, f"Cannot open generated output: {vector_path}")
    vector_layer = vector_datasource.GetLayerByName(LOW_ELEVATION_LAYER)
    require(vector_layer is not None, f"Missing vector layer: {LOW_ELEVATION_LAYER}")
    require(vector_layer.GetFeatureCount() > 0, "The low-elevation vector layer is empty")
    vector_srs = vector_layer.GetSpatialRef()
    require(
        vector_srs is not None and vector_srs.GetAuthorityCode(None) == "25831",
        "The low-elevation vector layer does not use EPSG:25831",
    )
    vector_area = 0.0
    for feature in vector_layer:
        geometry = feature.GetGeometryRef()
        require(geometry is not None and not geometry.IsEmpty(), "Empty low-elevation polygon")
        require(geometry.IsValid(), "Invalid low-elevation polygon")
        require(feature.GetField("classe") == 1, "Unexpected low-elevation class")
        vector_area += geometry.GetArea()
    expected_area = 2150 * 25 * 25
    require(
        abs(vector_area - expected_area) < 0.01,
        f"Unexpected low-elevation polygon area: {vector_area}",
    )
    vector_sha256 = sha256_file(vector_path)
    require(
        vector_sha256 == LOW_ELEVATION_SHA256,
        f"SHA-256 mismatch for {vector_path}: {vector_sha256}",
    )
    outputs[LOW_ELEVATION_VECTOR] = {
        "sha256": vector_sha256,
        "size": vector_path.stat().st_size,
        "layer": LOW_ELEVATION_LAYER,
        "feature_count": vector_layer.GetFeatureCount(),
        "area_m2": vector_area,
        "crs": "EPSG:25831",
    }
    vector_datasource = None

    degrees = valid_array(root / "pendent_25m_graus_vila_seca.tif")
    percent = valid_array(root / "pendent_25m_percent_vila_seca.tif")
    require(degrees.shape == percent.shape, "Slope outputs have different valid-cell counts")
    relation_error = float(np.max(np.abs(percent - 100.0 * np.tan(np.radians(degrees)))))
    require(relation_error < 0.001, f"Slope unit relation failed: {relation_error}")
    return {
        "ok": True,
        "gdal_version": gdal.VersionInfo("RELEASE_NAME"),
        "slope_relation_max_error": relation_error,
        "outputs": outputs,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate existing outputs without rebuilding them",
    )
    arguments = parser.parse_args()
    gdal.UseExceptions()
    report = validate_outputs() if arguments.check else build()
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
