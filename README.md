# Fairfax County Lawn-Dryness Assessment

This repository is an early-stage geospatial research project for assessing lawn and vegetation dryness in Fairfax County, Virginia, using satellite and environmental data.

## Research question

Can openly available remote-sensing and weather data identify meaningful spatial and temporal variation in lawn dryness at neighborhood-relevant scales?

The current code does **not** yet produce a validated lawn-dryness measure. It provides the beginning of a Google Earth Engine acquisition pipeline and should be treated as research infrastructure, not an operational drought, fire-risk, irrigation, or property-level decision tool.

## Current implementation

The repository currently includes:

- Google Earth Engine initialization and configuration loading.
- Sentinel-2 surface-reflectance and cloud-probability collection joins.
- Cloud and shadow masking.
- Fourteen-day median NDVI composites.
- Export to Google Cloud Storage or Earth Engine assets.
- A helper for downloading exported objects from Cloud Storage.
- A draft McLean-area configuration at 10-meter resolution.

The run configuration also identifies planned covariates that are not fully implemented yet:

- Vegetation indices: NDVI, NDRE, NDMI, NDWI, EVI, and NIRv.
- Sentinel-1 radar features.
- Land-surface temperature.
- Recent rainfall, evapotranspiration, and vapor-pressure deficit.
- Terrain and canopy characteristics.

## Repository layout

- `config/run.yaml` — draft run configuration.
- `docs/gee/README.md` — Earth Engine data-layout documentation.
- `src/data_acquisition/gee/` — collection, composite, export, and pipeline code.
- `scripts/gcs_sync.py` — Cloud Storage download helper.
- `data/gee/` — ignored local or exported data locations.
- `logs/gee/`, `tmp/gee/`, and `assets/gee/` — ignored runtime locations.

## Running the existing NDVI export

1. Create and activate a Python environment.
2. Install the dependencies required by the imports in this repository, including the Earth Engine Python API, PyYAML, and Google Cloud Storage client.
3. Authenticate Earth Engine and set the Google Cloud project in `config/run.yaml` or `EE_PROJECT`.
4. Add an area-of-interest GeoJSON at the configured `aoi_path`. AOI files are intentionally excluded from version control.
5. Review the date range, cloud threshold, resolution, coordinate system, and export destination.
6. Run:

   ```bash
   python -m src.data_acquisition.gee.pipelines.ndvi_batch
   ```

The sample configuration refers to cloud resources that may not exist or may require separate authorization.

## Validation required before interpretation

NDVI alone is not a direct measurement of lawn dryness. A defensible product would require, at minimum:

1. A clearly defined target variable, such as soil moisture, turf stress, or observed browning.
2. Fairfax County or pilot-area boundaries with documented provenance.
3. Ground observations or another independent validation source.
4. Separation of lawns from trees, crops, impervious surfaces, and other land cover.
5. Controls for seasonality, mowing, irrigation, shade, clouds, and sensor availability.
6. Out-of-sample spatial and temporal validation.
7. Uncertainty reporting at the same geographic scale as any published result.

Until those steps are completed, outputs should be described as vegetation-index composites rather than lawn-dryness estimates.

## Data and credential policy

Large rasters, downloaded exports, local AOIs, runtime logs, virtual environments, and credentials are excluded from Git. Store reproducible source code, small configuration files, schemas, manifests, and derived summary tables in the repository. Store large or sensitive artifacts in an appropriate external data store and record their provenance.

Never commit Earth Engine credentials, service-account keys, Cloud Storage credentials, or local Python environments.
