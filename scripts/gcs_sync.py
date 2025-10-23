#!/usr/bin/env python3
"""Lightweight helper to mirror a GCS prefix into a local folder.

Intended for environments where installing the Cloud SDK / gsutil
is impractical (e.g., Crostini partitions on ChromeOS).

Example:
    export GOOGLE_APPLICATION_CREDENTIALS="$PWD/config/gee/auth/gee-key.json"
    python scripts/gcs_sync.py \
        --bucket mclean-gee-export \
        --prefix mclean_l0_2025Q3 \
        --dest data/gee/raw
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from google.cloud import storage


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download objects from GCS.")
    parser.add_argument(
        "--bucket",
        required=True,
        help="Name of the Cloud Storage bucket, e.g. mclean-gee-export.",
    )
    parser.add_argument(
        "--prefix",
        default="",
        help="Optional prefix within the bucket to sync (default: entire bucket).",
    )
    parser.add_argument(
        "--dest",
        default="data/gee/raw",
        help="Local destination directory for downloads.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List the files that would be downloaded without writing to disk.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    client = storage.Client()  # Uses GOOGLE_APPLICATION_CREDENTIALS if set.
    bucket = client.bucket(args.bucket)
    dest_root = Path(args.dest).expanduser().resolve()
    dest_root.mkdir(parents=True, exist_ok=True)

    blobs = bucket.list_blobs(prefix=args.prefix)
    found = False

    for blob in blobs:
        found = True
        relative_path = Path(blob.name)
        target_path = dest_root / relative_path
        if args.dry_run:
            print(f"[DRY RUN] Would download: {blob.name} -> {target_path}")
            continue

        target_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"Downloading {blob.name} -> {target_path}")
        blob.download_to_filename(target_path)

    if not found:
        print("No objects matched the specified prefix.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
