# Microclimate

Repository scaffold for microclimate forecasting experiments. The project now
includes a dedicated layout for Google Earth Engine (GEE) data acquisition.

- `docs/gee/README.md` captures the folder-by-folder breakdown for the ingestion
  pipeline.
- `src/data_acquisition/gee/` houses the Python package where GEE collection
  builders, composites, exporters, and pipeline entry-points will live.
- `config/gee/`, `data/gee/`, `logs/gee/`, `tmp/gee/`, and `assets/gee/` provide
  dedicated storage for configuration, raw/processed artefacts, task logging,
  temporary scratch space, and asset metadata respectively.
- `config/run.yaml` drives the batch pipeline; specify `ee_project` (your Google
  Cloud project ID) plus the export target (`export.gcs_bucket` for Cloud
  Storage or `export.asset_prefix` for Earth Engine assets).
- `scripts/gcs_sync.py` offers a lightweight alternative to `gsutil` for pulling
  objects down via the `google-cloud-storage` library—handy on Crostini installs
  with limited disk.

Populate each area with the assets required for your deployment (credentials,
run manifests, notebooks, etc.) and keep sensitive material out of version
control.
