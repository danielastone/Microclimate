"""Batch NDVI export pipeline using Google Earth Engine."""

from __future__ import annotations

import datetime as _dt
import os
from typing import List, Optional

import ee  # type: ignore

from ..composites.sentinel2 import build_ndvi_composite
from ..exports.sentinel2 import export_ndvi_to_asset, export_ndvi_to_cloud_storage
from ..utils.config import load_aoi_geometry, read_yaml
from ..utils.dates import daterange


def _format_for_filename(date_value: _dt.date) -> str:
    return date_value.strftime("%Y%m%d")


def _ensure_initialized(project: Optional[str] = None) -> None:
    try:
        ee.Image("COPERNICUS/S2_SR_HARMONIZED")
    except Exception:
        if project:
            ee.Initialize(project=project)
        else:
            ee.Initialize()


def run(config_path: str = "config/run.yaml") -> List[ee.batch.Task]:
    """Run the Sentinel-2 NDVI export pipeline using ``config_path``."""
    cfg = read_yaml(config_path)
    project = cfg.get("ee_project") or os.environ.get("EE_PROJECT")
    _ensure_initialized(project=project)

    aoi = load_aoi_geometry(cfg["aoi_path"])
    start = _dt.date.fromisoformat(cfg["dates"]["start"])
    end = _dt.date.fromisoformat(cfg["dates"]["end"])
    step_days = int(cfg.get("composite_days", 14))
    cloud_thresh = int(cfg.get("s2_cloud_prob_thresh", 40))
    run_id = cfg["run_id"]

    export_cfg = cfg.get("export", {})
    destination = export_cfg.get("to", "ASSET").upper()
    scale = int(export_cfg.get("scale", cfg.get("res_m", 10)))
    crs = export_cfg.get("crs", "EPSG:4326")
    cog = bool(export_cfg.get("cog", True))

    tasks: List[ee.batch.Task] = []

    for start_date, end_date in daterange(start, end, step_days):
        ndvi = build_ndvi_composite(
            aoi=aoi,
            start=start_date.isoformat(),
            end=end_date.isoformat(),
            cloud_probability_threshold=cloud_thresh,
        )

        start_token = _format_for_filename(start_date)
        end_token = _format_for_filename(end_date)

        if destination == "CLOUD_STORAGE":
            bucket = export_cfg.get("gcs_bucket")
            if not bucket:
                raise ValueError("'export.gcs_bucket' must be set for Cloud Storage exports.")
            task = export_ndvi_to_cloud_storage(
                ndvi,
                aoi,
                run_id=run_id,
                start_iso=start_token,
                end_iso=end_token,
                bucket=bucket,
                scale=scale,
                crs=crs,
                cog=cog,
            )
        elif destination == "ASSET":
            asset_prefix = export_cfg.get("asset_prefix")
            if not asset_prefix:
                raise ValueError("'export.asset_prefix' must be set for Asset exports.")
            task = export_ndvi_to_asset(
                ndvi,
                aoi,
                run_id=run_id,
                start_iso=start_token,
                end_iso=end_token,
                asset_prefix=asset_prefix,
                scale=scale,
                crs=crs,
            )
        else:
            raise NotImplementedError(f"Export destination '{destination}' is not supported yet.")

        tasks.append(task)
        print(f"Started export task: {task.id}")

    return tasks


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    run()
