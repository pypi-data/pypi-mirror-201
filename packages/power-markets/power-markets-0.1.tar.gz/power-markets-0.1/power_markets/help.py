# -*- coding: utf-8 -*-
# Copyright (c) Hebes Intelligence Private Company

# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

COUNTRY_HELP = """The name of the country to run the command for (in ISO 3166 alpha-2
codes, except for Greece, for which the abbreviation EL is used)."""

DDIR_HELP = """The path to the folder for storing the downloaded data. If the path is not
an absolute path, it will be interpreted as `power_markets.settings.RAW_DATA_DIR/{country}/{path}`."""

DTARGET_HELP = """The dataset to extract from the raw data.\n
- "load" extracts the load dataset from the `dispatch` data\n
- "reserves" extracts the secondary reserves dataset from the `dispatch` data\n
- "committed" extracts the committed capacity dataset from the `dispatch` data\n
- "imports" extracts the power imports dataset from the `dispatch` data\n
- "exports" extracts the power exports dataset from the `dispatch` data\n
- "res" extracts the RES generation dataset from the `dispatch` data\n
- "available" extracts the available capacity dataset from the `availabilities` data\n
- "reservoirs" extracts the water reservoir levels (for hydro plants) dataset from the `reservoirs` data\n
- "ntc_imports" extracts dataset for total NTC (net transfer capacity) for imports from the `ntc` data\n
- "ntc_exports" extracts dataset for total NTC (net transfer capacity) for exports from the `ntc` data
"""

DTYPE_HELP = """The type of data to download.\n
- "dispatch" includes the inputs and results of the day-ahead scheduling\n
- "availabilities" includes data about the available capacity for all dispatchable power
generation units\n
- "reservoirs" includes data about the filling rates of the hydropower plants\n
- "ntc" includes data about the net transfer capability for power imports and exports."""

DATE_HELP = (
    lambda when, what: f"""The {when} date of the {what} data period (in %d-%m-%Y format,
    like 31-12-2020)."""
)

EXTRACT_HELP = "Extract datasets from the raw data."

FETCH_HELP = """Download power system data from the relevant TSO."""

SOURCE_HELP = """The path to the folder where the downloaded data is stored. If the path is not
an absolute path, it will be interpreted as `power_markets.settings.RAW_DATA_DIR/{country}/{path}`."""

SUFFIX_HELP = """The name to add at each stored file (after the date)."""
