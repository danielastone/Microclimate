"""Offline dependency and draft configuration checks; no API calls or credentials."""
import datetime
import importlib
from pathlib import Path
import unittest

from data_acquisition.gee.utils.config import read_yaml
from data_acquisition.gee.utils.dates import daterange


class SmokeTests(unittest.TestCase):
    def test_pipeline_dependencies_import_without_credentials(self):
        for module in (
            "ee", "google.cloud.storage",
            "data_acquisition.gee.pipelines.ndvi_batch",
        ):
            importlib.import_module(module)

    def test_draft_config_and_window_coverage(self):
        config = read_yaml(Path(__file__).resolve().parents[1] / "config/run.yaml")
        start = datetime.date.fromisoformat(config["dates"]["start"])
        end = datetime.date.fromisoformat(config["dates"]["end"])
        self.assertLess(start, end)
        step = int(config["composite_days"])
        self.assertGreater(step, 0)
        windows = list(daterange(start, end, step))
        self.assertEqual(windows[0][0], start)
        self.assertEqual(windows[-1][1], end)
        for left, right in zip(windows, windows[1:]):
            self.assertEqual(left[1], right[0])
        self.assertIn(config["export"]["to"], ("ASSET", "CLOUD_STORAGE"))
