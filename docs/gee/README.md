# Google Earth Engine Data Acquisition

This document describes the directory layout used for Earth Engine (GEE) ingestion workflows.

```
Microclimate/
├── config/
│   └── gee/
│       ├── auth/        # Local-only credentials (never commit secrets)
│       ├── runs/        # YAML definitions of AOIs and acquisition windows
│       └── lookups/     # Static lookup tables and band metadata
├── data/
│   └── gee/
│       ├── aoi/         # GeoJSONs defining areas of interest for runs
│       ├── raw/         # Direct downloads (Cloud Storage sync, asset exports)
│       ├── intermediate/# Temporary staging during processing
│       └── processed/   # Final rasters/tables promoted for modeling
├── logs/
│   └── gee/             # Task status logs, audit trails, task manifests
├── notebooks/
│   └── gee/             # Exploratory notebooks for AOI validation & QC
├── src/
│   └── data_acquisition/
│       └── gee/
│           ├── collections/  # ImageCollection filters & join logic
│           ├── composites/   # Temporal composites & per-band transforms
│           ├── exports/      # Export helpers wrapping ee.batch tasks
│           ├── pipelines/    # Orchestration entry-points (CLIs, jobs)
│           ├── tasks/        # Monitoring & retry utilities
│           └── utils/        # Shared helpers (config, geometry, auth)
├── tmp/
│   └── gee/             # Ephemeral scratch space (cleared regularly)
└── assets/
    └── gee/             # Local metadata about GEE asset hierarchy
```

Populate each folder with the artefacts relevant to your workflow. Add additional subfolders as your pipeline evolves—for example, per-region or per-product splits under `data/gee/raw` and `data/gee/processed`.
