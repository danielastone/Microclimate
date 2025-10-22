\"\"\"Configuration helpers for GEE acquisition pipelines.\"\"\"

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

import ee  # type: ignore


def read_yaml(path: str | Path) -> dict[str, Any]:
    \"\"\"Load a YAML configuration file.\"\"\"
    with Path(path).expanduser().open() as handle:
        return yaml.safe_load(handle)


def load_aoi_geometry(aoi_path: str | Path) -> ee.Geometry:
    \"\"\"Read a GeoJSON/JSON AOI file into an Earth Engine geometry.\"\"\"
    with Path(aoi_path).expanduser().open() as handle:
        geojson = json.load(handle)
    collection = ee.FeatureCollection(geojson)
    return collection.geometry()
