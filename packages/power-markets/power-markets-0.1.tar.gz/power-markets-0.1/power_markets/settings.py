# -*- coding: utf-8 -*-

import importlib.resources

import power_markets

with importlib.resources.path(power_markets, "__main__.py") as main_path:
    SOURCE_PATH = main_path.resolve().parent

RAW_DATA_DIR = SOURCE_PATH / "raw_data"
DATASET_DIR = SOURCE_PATH / "datasets"
