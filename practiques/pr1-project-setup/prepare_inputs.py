"""Retain the three reviewed PR1 inputs without downloads or replacement."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import stat


ROOT = Path(__file__).resolve().parents[2]
INPUTS = (
    (
        "tmp/reference-exercises/sources/divisions-administratives-v2r2-municipis-5000-20260120.fgb",
        "practiques/pr1-project-setup/inputs/municipis-icgc-20260120.fgb",
        "069f755f253f7af969e80403f6e81fa2cadefbd4c40ffd2f825f30e167bf2b2d",
    ),
    (
        "assets/projectes/vila-seca/dades_preparades/projecte_tig.gpkg",
        "practiques/pr1-project-setup/inputs/municipi-cnig-font.gpkg",
        "46aa316b88ec9f6eac559ca4f2037f1e142a997d3c0722febb8912a9a03654dd",
    ),
    (
        "tmp/unaltracaptura-qgis/cache/prepared/terrain/vila-seca/ortofoto_territorial_2025_vila_seca.tif",
        "practiques/pr1-project-setup/inputs/ortofoto-vilaseca-2025.tif",
        "8cfdb39b6fce124844644087bc39a365da9bcef6401286644590b60c4fd07ad0",
    ),
)


def checked_path(relative, required=True):
    path = ROOT / relative
    for part in (path, *path.parents):
        if part.is_symlink():
            raise ValueError(f"Symlink is not an accepted PR1 input path: {part}")
        if part == ROOT:
            break
    if path.exists():
        info = path.stat()
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise ValueError(f"Expected one regular, unshared file: {relative}")
    elif required:
        raise FileNotFoundError(relative)
    return path


def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    planned = []
    for source, destination, expected in INPUTS:
        original = checked_path(source)
        retained = checked_path(destination, required=False)
        if digest(original) != expected:
            raise ValueError(f"Reviewed source differs: {source}")
        if retained.exists() and digest(retained) != expected:
            raise ValueError(f"Existing destination differs; preserved for diagnosis: {destination}")
        planned.append((original, retained, source, destination, expected))

    report = []
    for original, retained, source, destination, expected in planned:
        state = "reused" if retained.exists() else "planned"
        if state == "planned" and not args.dry_run:
            retained.parent.mkdir(parents=True, exist_ok=True)
            checked_path(destination, required=False)
            with original.open("rb") as src, retained.open("xb") as dst:
                for block in iter(lambda: src.read(1024 * 1024), b""):
                    dst.write(block)
                dst.flush()
                os.fsync(dst.fileno())
            if digest(retained) != expected or digest(original) != expected:
                raise ValueError(f"Copy verification failed; files retained: {destination}")
            state = "copied"
        report.append({"source": source, "destination": destination,
                       "sha256": expected, "bytes": original.stat().st_size, "state": state})
    print(json.dumps({"ok": True, "dry_run": args.dry_run, "inputs": report},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
