# GEE Configuration Layout

This folder stores configuration files that are specific to Google Earth Engine acquisitions.

- `auth/` (optional): service account keys or token metadata. Add the folder locally and do **not** commit secrets.
- `runs/`: per-run YAML files describing AOIs, time windows, and outputs.
- `lookups/`: static lookup tables (e.g., band dictionaries, asset paths).

The repository only tracks structural placeholders—populate the subdirectories with the appropriate files for your environment.
