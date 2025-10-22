\"\"\"Helpers for exporting Sentinel-2 composites from Earth Engine.\"\"\"

from __future__ import annotations

import ee  # type: ignore

__all__ = [
    \"export_ndvi_to_cloud_storage\",
    \"export_ndvi_to_asset\",
]


def export_ndvi_to_cloud_storage(
    ndvi_image: ee.Image,
    aoi: ee.Geometry,
    *,
    run_id: str,
    start_iso: str,
    end_iso: str,
    bucket: str,
    scale: int,
    crs: str,
    cog: bool,
) -> ee.batch.Task:
    \"\"\"Kick off a Cloud Optimized GeoTIFF export to Google Cloud Storage.\"\"\"
    name = f\"{run_id}_{start_iso}_{end_iso}\"

    task = ee.batch.Export.image.toCloudStorage(
        image=ndvi_image.clip(aoi),
        description=name,
        bucket=bucket,
        fileNamePrefix=name,
        region=aoi,
        scale=scale,
        crs=crs,
        fileFormat=\"GeoTIFF\",
        formatOptions={\"cloudOptimized\": cog},
        maxPixels=1e13,
    )
    task.start()
    return task


def export_ndvi_to_asset(
    ndvi_image: ee.Image,
    aoi: ee.Geometry,
    *,
    run_id: str,
    start_iso: str,
    end_iso: str,
    asset_prefix: str,
    scale: int,
    crs: str,
) -> ee.batch.Task:
    \"\"\"Kick off an Earth Engine Asset export.\"\"\"
    name = f\"{run_id}_{start_iso}_{end_iso}\"
    asset_id = f\"{asset_prefix.rstrip('/')}/{name}\"

    task = ee.batch.Export.image.toAsset(
        image=ndvi_image.clip(aoi),
        description=name,
        assetId=asset_id,
        region=aoi,
        scale=scale,
        crs=crs,
        maxPixels=1e13,
    )
    task.start()
    return task
