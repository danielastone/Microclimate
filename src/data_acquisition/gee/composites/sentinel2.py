\"\"\"Sentinel-2 composite builders.\"\"\"

from __future__ import annotations

import ee  # type: ignore


def build_ndvi_composite(
    aoi: ee.Geometry,
    start: str,
    end: str,
    cloud_probability_threshold: int,
) -> ee.Image:
    \"\"\"Generate an NDVI composite for the AOI between ``start`` and ``end``.\"\"\"
    s2_sr = (
        ee.ImageCollection(\"COPERNICUS/S2_SR_HARMONIZED\")
        .filterBounds(aoi)
        .filterDate(start, end)
        .filter(ee.Filter.lt(\"CLOUDY_PIXEL_PERCENTAGE\", 80))
    )

    s2_cp = (
        ee.ImageCollection(\"COPERNICUS/S2_CLOUD_PROBABILITY\")
        .filterBounds(aoi)
        .filterDate(start, end)
    )

    joined = ee.ImageCollection(
        ee.Join.saveFirst(\"clouds\").apply(
            s2_sr,
            s2_cp,
            ee.Filter.equals(leftField=\"system:index\", rightField=\"system:index\"),
        )
    )

    def mask_clouds(image: ee.Image) -> ee.Image:
        cloud_prob = ee.Image(image.get(\"clouds\")).select(\"probability\")
        scl = image.select(\"SCL\")
        cloud = cloud_prob.gt(cloud_probability_threshold)
        shadow = scl.eq(3)
        mask = cloud.Or(shadow).Not()
        return image.updateMask(mask)

    masked = joined.map(mask_clouds)
    median = masked.median()

    ndvi = median.normalizedDifference([\"B8\", \"B4\"]).rename(\"ndvi\")
    return ndvi.set(
        {
            \"system:time_start\": ee.Date(start).millis(),
            \"system:time_end\": ee.Date(end).millis(),
        }
    )
