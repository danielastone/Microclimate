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

Populate each area with the assets required for your deployment (credentials,
run manifests, notebooks, etc.) and keep sensitive material out of version
control.
