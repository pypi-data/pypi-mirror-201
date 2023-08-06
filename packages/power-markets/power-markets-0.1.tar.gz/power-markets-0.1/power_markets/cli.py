# -*- coding: utf-8 -*-
# Copyright (c) Hebes Intelligence Private Company

# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import logging
import os

import click

from .countries.Greece import admie
from .exceptions import NoDataFound
from .help import (
    COUNTRY_HELP,
    DATE_HELP,
    DDIR_HELP,
    DTARGET_HELP,
    DTYPE_HELP,
    EXTRACT_HELP,
    FETCH_HELP,
    SOURCE_HELP,
    SUFFIX_HELP,
)
from .settings import RAW_DATA_DIR

logger = logging.getLogger("power-markets")


@click.group(name="power-markets")
def fetch_cli():
    pass


@fetch_cli.command("fetch", help=FETCH_HELP)
@click.option("--country", "-c", type=str, required=True, help=COUNTRY_HELP)
@click.option(
    "--start-date",
    "-sd",
    type=click.DateTime(formats=["%d-%m-%Y"]),
    required=True,
    help=DATE_HELP("first", "download"),
)
@click.option(
    "--end-date",
    "-ed",
    type=click.DateTime(formats=["%d-%m-%Y"]),
    required=True,
    help=DATE_HELP("last", "download"),
)
@click.option("--data-type", "-dt", type=str, required=True, help=DTYPE_HELP)
@click.option("--dest-dir", "-dd", type=str, required=True, help=DDIR_HELP)
@click.option("--suffix", "-s", type=str, required=True, help=SUFFIX_HELP)
def fetch_data(country, start_date, end_date, data_type, dest_dir, suffix):
    if not os.path.isabs(dest_dir):
        dest_dir = os.path.join(RAW_DATA_DIR, country, dest_dir)

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    if country == "EL":
        missing_days = admie.fetch_data(
            start_date, end_date, data_type, dest_dir, suffix
        )
    else:
        raise NotImplementedError(f"{country} country is not supported yet.")

    if missing_days:
        logger.warning(f"Data for the following dates was not found: {missing_days}")


@fetch_cli.command("extract", help=EXTRACT_HELP)
@click.option("--country", "-c", type=str, required=True, help=COUNTRY_HELP)
@click.option(
    "--start-date",
    "-sd",
    type=click.DateTime(formats=["%d-%m-%Y"]),
    required=True,
    help=DATE_HELP("first", "input"),
)
@click.option(
    "--end-date",
    "-ed",
    type=click.DateTime(formats=["%d-%m-%Y"]),
    required=True,
    help=DATE_HELP("last", "input"),
)
@click.option("--data-target", "-dt", type=str, required=True, help=DTARGET_HELP)
@click.option("--data-dir", "-dd", type=str, required=True, help=SOURCE_HELP)
def extract_data(country, start_date, end_date, data_target, data_dir):
    if not os.path.isabs(data_dir):
        data_dir = os.path.join(RAW_DATA_DIR, country, data_dir)

    func_switch = {}

    if country == "EL":
        func_switch = {
            "load": admie.extract_load,
            "reserves": admie.extract_secondary_reserves,
            "committed": admie.extract_committed_capacity,
            "imports": admie.extract_imports,
            "exports": admie.extract_exports,
            "res": admie.extract_res_generation,
            "available": admie.extract_available_capacity,
            "reservoirs": admie.extract_reservoir_levels,
            "ntc_imports": admie.extract_import_ntc,
            "ntc_exports": admie.extract_export_ntc,
        }
    else:
        raise NotImplementedError(f"{country} country is not supported yet.")

    if data_target in func_switch:
        logger.info(f"Extracting data for target `{data_target}`.")
        try:
            func_switch.get(data_target)(start_date, end_date, data_dir)
        except NoDataFound:
            logger.error("No relevant data found.") 
    else:
        raise ValueError(f"Data target `{data_target}` not applicable.")
