# -*- coding: utf-8 -*-
# Copyright (c) Hebes Intelligence Private Company

# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import calendar
import datetime
import glob
import json
import os
from collections import defaultdict
from typing import Literal
from urllib.error import HTTPError
from urllib.request import urlopen

import numpy as np
import pandas as pd
import xlrd
from tqdm import tqdm

from ...exceptions import NoDataFound
from ...settings import DATASET_DIR
from ...utils import create_path, get_last_sunday


datatypes = {  # see https://www.admie.gr/getFiletypeInfoEN for all possible values
    "dispatch": {
        "name": "DispatchSchedulingResults",
        "frequency": "D",
        "filetype": "xls",
    },
    "availabilities": {
        "name": "DayAheadSchedulingUnitAvailabilities",
        "frequency": "D",
        "filetype": "xls",
    },
    "reservoirs": {"name": "ReservoirFillingRate", "frequency": "D", "filetype": "xls"},
    "ntc": {"name": "MonthlyNTC", "frequency": "M", "filetype": "xls"},
}


###########################################################################################
# Data download
###########################################################################################


def fetch_data(
    start_date: str,
    end_date: str,
    datatype: Literal["dispatch", "availabilities", "reservoirs", "ntc"],
    destination: str,
    suffix: str,
    date_format: str = "%d-%m-%Y",
):
    """General data downloader from ADMIE (Greek TSO)

    Args:
        start_date (str): Left bound for generating dates.
        end_date (str): Right bound for generating dates.
        datatype ({"dispatch", "availabilities", "reservoirs", "ntc"}): The type of data to download.
            "dispatch" includes the inputs and results of the day-ahead scheduling, "availabilities"
            includes data about the available capacity for all dispatchable power generation units,
            "reservoirs" includes data about the filling rates of the hydropower plants, and "ntc"
            includes data about the net transfer capability for power imports and exports.
        destination (str): The path to the folder for storing the downloaded data.
        suffix (str): The name to add at each stored file (after the date).
        date_format (str, optional): The strftime to parse the `start_date` and `end_date` dates.
            Defaults to "%d-%m-%Y".

    Returns:
        list: List of dates for which downloading failed.
    """
    missing_days = []

    start_date = pd.to_datetime(start_date, format=date_format)
    end_date = pd.to_datetime(end_date, format=date_format)

    freq = datatypes[datatype]["frequency"]
    if freq == "M":
        end_date = datetime.date(
            end_date.year,
            end_date.month,
            calendar.monthrange(end_date.year, end_date.month)[-1],
        )
    period = pd.date_range(
        start=start_date,
        end=end_date,
        freq=freq,
        inclusive="both",
    )

    pbar = tqdm(total=len(period))
    for day in period:
        file_path = None

        try:
            if freq == "M":
                last_day = day.strftime("%Y-%m-%d")
                day = datetime.date(day.year, day.month, 1)
                response = urlopen(
                    "https://www.admie.gr/getOperationMarketFile?"
                    f"dateStart={day.strftime('%Y-%m-%d')}&dateEnd={last_day}"
                    f"&FileCategory={datatypes[datatype]['name']}"
                )
            else:
                response = urlopen(
                    "https://www.admie.gr/getOperationMarketFile?"
                    f"dateStart={day.strftime('%Y-%m-%d')}&dateEnd={day.strftime('%Y-%m-%d')}"
                    f"&FileCategory={datatypes[datatype]['name']}"
                )
        except HTTPError:
            continue
        else:
            response = json.loads(response.read().decode("utf-8"))
            if len(response) > 0:
                file_path = response[0]["file_path"]

        if file_path is not None:
            try:
                f = urlopen(file_path)
            except HTTPError:
                missing_days.append(day)
                continue
        else:
            missing_days.append(day)
            continue

        with open(
            os.path.join(
                destination,
                day.strftime("%Y%m%d")
                + "_"
                + suffix
                + f".{datatypes[datatype]['filetype']}",
            ),
            "wb",
        ) as stream:
            stream.write(f.read())
        pbar.update(1)

    pbar.close()
    return missing_days


###########################################################################################
# Data extraction into datasets
###########################################################################################


def extract_load(
    start_date: str, end_date: str, raw_data_path: str, date_format: str = "%d-%m-%Y"
):
    """Extract the load dataset from the raw data.

    Args:
        start_date (str): Left bound for generating dates.
        end_date (str): Right bound for generating dates.
        raw_data_path (str): The path to the directory that contains the raw data (day-ahead
            scheduling results).
        date_format (str, optional): The strftime to parse the `start_date` and `end_date` dates.
            Defaults to "%d-%m-%Y".
    """

    period = pd.date_range(
        start=pd.to_datetime(start_date, format=date_format),
        end=pd.to_datetime(end_date, format=date_format),
        freq="D",
        inclusive="both",
    )
    pbar = tqdm(total=len(period))

    data = {}
    for day in period:
        winter_time_change = (day.month == 3) and (
            day == get_last_sunday(day.year, day.month)
        )
        sday = day.strftime("%Y%m%d")
        xlfile = glob.glob(os.path.join(raw_data_path, sday) + "*")

        if len(xlfile) == 0:
            continue
        else:
            try:
                book = xlrd.open_workbook(xlfile[0], formatting_info=True)
            except xlrd.XLRDError:
                continue

        sheet = book.sheet_by_name(f"{sday}_DS")
        idx = sheet.col_values(0).index("LOAD FORECAST + LOSSES")

        data[day] = (
            np.array(sheet.row_values(idx)[1:24])
            if winter_time_change
            else np.array(sheet.row_values(idx)[1:25])
        )

        for item in [
            "SFIKIA PUMPING",
            "THESAVROS1 PUMPING",
            "THESAVROS2 PUMPING",
            "THESAVROS3 PUMPING",
        ]:
            idx = sheet.col_values(0).index(item)
            data[day] += (
                np.array(sheet.row_values(idx)[1:24])
                if winter_time_change
                else np.array(sheet.row_values(idx)[1:25])
            )
        pbar.update(1)

    pbar.close()

    if not data:
        raise NoDataFound()
    
    result = pd.DataFrame.from_dict(data, orient="index", columns=range(24))
    result = result.stack()
    result.index = result.index.map(lambda x: x[0].replace(hour=int(x[1])))
    result = result.to_frame("Total load [MW]")

    path = create_path(os.path.join(DATASET_DIR, "load", "EL"), "load.csv")
    result.to_csv(path, index_label="ds")


def extract_secondary_reserves(
    start_date: str, end_date: str, raw_data_path: str, date_format: str = "%d-%m-%Y"
):
    """Extract the secondary reserves dataset from the raw data.

    Args:
        start_date (str): Left bound for generating dates.
        end_date (str): Right bound for generating dates.
        raw_data_path (str): The path to the directory that contains the raw data (day-ahead
            scheduling results).
        date_format (str, optional): The strftime to parse the `start_date` and `end_date` dates.
            Defaults to "%d-%m-%Y".
    """

    period = pd.date_range(
        start=pd.to_datetime(start_date, format=date_format),
        end=pd.to_datetime(end_date, format=date_format),
        freq="D",
        inclusive="both",
    )
    pbar = tqdm(total=len(period))
    data_2u = {}
    data_2d = {}

    for day in period:
        sday = day.strftime("%Y%m%d")
        xlfile = glob.glob(os.path.join(raw_data_path, sday) + "*")

        if len(xlfile) == 0:
            continue
        else:
            try:
                book = xlrd.open_workbook(xlfile[0], formatting_info=True)
            except xlrd.XLRDError:
                continue

        sheet = book.sheet_by_name(f"{sday}_SecondaryReserve")
        names = sheet.col_values(0)
        data_2u[day] = sheet.row_values(names.index("Up - Requirement"))[2:26]
        data_2d[day] = sheet.row_values(names.index("Dn - Requirement"))[2:26]
        pbar.update(1)

    pbar.close()

    if (not data_2u) or (not data_2d):
        raise NoDataFound()
    
    data_2u = (
        pd.DataFrame.from_dict(data_2u, orient="index", columns=range(24))
        .stack()
        .to_frame("2U")
    )
    data_2u.index = data_2u.index.map(lambda x: x[0].replace(hour=int(x[1])))

    data_2d = (
        pd.DataFrame.from_dict(data_2d, orient="index", columns=range(24))
        .stack()
        .to_frame("2D")
    )
    data_2d.index = data_2d.index.map(lambda x: x[0].replace(hour=int(x[1])))

    result = pd.concat([data_2u, data_2d], axis=1)
    path = create_path(os.path.join(DATASET_DIR, "load", "EL"), "reserves.csv")
    result.to_csv(path, index_label="ds")


def extract_committed_capacity(
    start_date: str, end_date: str, raw_data_path: str, date_format: str = "%d-%m-%Y"
):
    """Extract the committed capacity dataset from the raw data.

    Args:
        start_date (str): Left bound for generating dates.
        end_date (str): Right bound for generating dates.
        raw_data_path (str): The path to the directory that contains the raw data (day-ahead
            scheduling results).
        date_format (str, optional): The strftime to parse the `start_date` and `end_date` dates.
            Defaults to "%d-%m-%Y".
    """
    plants = pd.read_csv(os.path.join(DATASET_DIR, "plants", "EL", "plants.csv"))
    unit_names = plants["Unit"].to_list()

    if "THESAVROS" in unit_names:
        unit_names.remove("THESAVROS")
        unit_names.extend(["THESAVROS1", "THESAVROS2", "THESAVROS3"])

    period = pd.date_range(
        start=pd.to_datetime(start_date, format=date_format),
        end=pd.to_datetime(end_date, format=date_format),
        freq="D",
        inclusive="both",
    )
    pbar = tqdm(total=len(period))
    data = defaultdict(dict)

    for day in period:
        winter_time_change = (day.month == 3) and (
            day == get_last_sunday(day.year, day.month)
        )
        sday = day.strftime("%Y%m%d")
        xlfile = glob.glob(os.path.join(raw_data_path, sday) + "*")

        if len(xlfile) == 0:
            continue
        else:
            try:
                book = xlrd.open_workbook(xlfile[0], formatting_info=True)
            except xlrd.XLRDError:
                continue

        sheet = book.sheet_by_name(f"{sday}_DS")
        all_names = sheet.col_values(0)

        alternative_names = {
            "LAVRIO4_G": "LAVRIO4",
            "LAVRIO4_O": "LAVRIO4",
            "KOMOTINI_G": "KOMOTINI",
            "KOMOTINI_O": "KOMOTINI",
            "ELPEDISON_THES_G": "ELPEDISON_THESS",
            "ELPEDISON_THES_O": "ELPEDISON_THESS",
            "ELPEDISON_THIS_G": "ELPEDISON_THISVI",
            "ELPEDISON_THIS_O": "ELPEDISON_THISVI",
        }

        unit_names.extend(list(alternative_names.keys()))

        for name in set(unit_names).intersection(all_names):
            idx = all_names.index(name)
            data[name][day] = (
                np.pad(np.array(sheet.row_values(idx)[1:24]), (0, 1), mode="edge")
                if winter_time_change
                else np.array(sheet.row_values(idx)[1:25])
            )
        pbar.update(1)

    pbar.close()

    if not data:
        raise NoDataFound()
    
    result = pd.concat({k: pd.DataFrame(v).T for k, v in data.items()}, axis=0)
    result.index = result.index.set_names(["unit_name", "ds"])

    for alt, orig in alternative_names.items():
        result.rename(level=0, index={alt: orig}, inplace=True)

    result = result.groupby(level=[0, 1]).sum()
    path = create_path(os.path.join(DATASET_DIR, "generation", "EL"), "committed.csv")
    result.to_csv(path)


def extract_imports(
    start_date: str, end_date: str, raw_data_path: str, date_format: str = "%d-%m-%Y"
):
    """Extract the power imports dataset from the raw data.

    Args:
        start_date (str): Left bound for generating dates.
        end_date (str): Right bound for generating dates.
        raw_data_path (str): The path to the directory that contains the raw data (day-ahead
            scheduling results).
        date_format (str, optional): The strftime to parse the `start_date` and `end_date` dates.
            Defaults to "%d-%m-%Y".
    """

    period = pd.date_range(
        start=pd.to_datetime(start_date, format=date_format),
        end=pd.to_datetime(end_date, format=date_format),
        freq="D",
        inclusive="both",
    )
    pbar = tqdm(total=len(period))

    data = {}
    for day in period:
        winter_time_change = (day.month == 3) and (
            day == get_last_sunday(day.year, day.month)
        )
        sday = day.strftime("%Y%m%d")
        xlfile = glob.glob(os.path.join(raw_data_path, sday) + "*")

        if len(xlfile) == 0:
            continue
        else:
            try:
                book = xlrd.open_workbook(xlfile[0], formatting_info=True)
            except xlrd.XLRDError:
                continue

        sheet = book.sheet_by_name(f"{sday}_DS")
        names = sheet.col_values(0)
        start = names.index("BORDER IMPORTS") + 1
        end = names.index("BORDER EXPORTS")

        result = 0
        for i in range(start, end):
            result += (
                np.array(sheet.row_values(i)[1:24])
                if winter_time_change
                else np.array(sheet.row_values(i)[1:25])
            )

        data[day] = result
        pbar.update(1)

    pbar.close()

    if not data:
        raise NoDataFound()
    
    result = pd.DataFrame.from_dict(data, orient="index", columns=range(24))
    result = result.stack()
    result.index = result.index.map(
        lambda x: datetime.datetime.combine(x[0], datetime.time(int(x[1])))
    )
    result = result.to_frame("Imports [MW]")
    path = create_path(os.path.join(DATASET_DIR, "flows", "EL"), "imports.csv")
    result.to_csv(path, index_label="ds")


def extract_exports(
    start_date: str, end_date: str, raw_data_path: str, date_format: str = "%d-%m-%Y"
):
    """Extract the power exports dataset from the raw data.

    Args:
        start_date (str): Left bound for generating dates.
        end_date (str): Right bound for generating dates.
        raw_data_path (str): The path to the directory that contains the raw data (day-ahead
            scheduling results).
        date_format (str, optional): The strftime to parse the `start_date` and `end_date` dates.
            Defaults to "%d-%m-%Y".
    """

    period = pd.date_range(
        start=pd.to_datetime(start_date, format=date_format),
        end=pd.to_datetime(end_date, format=date_format),
        freq="D",
        inclusive="both",
    )
    pbar = tqdm(total=len(period))

    data = {}
    for day in period:
        winter_time_change = (day.month == 3) and (
            day == get_last_sunday(day.year, day.month)
        )
        sday = day.strftime("%Y%m%d")
        xlfile = glob.glob(os.path.join(raw_data_path, sday) + "*")

        if len(xlfile) == 0:
            continue
        else:
            try:
                book = xlrd.open_workbook(xlfile[0], formatting_info=True)
            except xlrd.XLRDError:
                continue

        sheet = book.sheet_by_name(f"{sday}_DS")
        names = sheet.col_values(0)
        start = names.index("BORDER EXPORTS") + 1
        end = names.index("CORRIDOR LIMIT")

        result = 0
        for i in range(start, end):
            result += (
                np.array(sheet.row_values(i)[1:24])
                if winter_time_change
                else np.array(sheet.row_values(i)[1:25])
            )
        data[day] = result
        pbar.update(1)

    pbar.close()

    if not data:
        raise NoDataFound()
    
    result = pd.DataFrame.from_dict(data, orient="index", columns=range(24))
    result = result.stack()
    result.index = result.index.map(
        lambda x: datetime.datetime.combine(x[0], datetime.time(int(x[1])))
    )
    result = result.to_frame("Exports [MW]")
    path = create_path(os.path.join(DATASET_DIR, "flows", "EL"), "exports.csv")
    result.to_csv(path, index_label="ds")


def extract_res_generation(
    start_date: str, end_date: str, raw_data_path: str, date_format: str = "%d-%m-%Y"
):
    """Extract the RES generation dataset from the raw data.

    Args:
        start_date (str): Left bound for generating dates.
        end_date (str): Right bound for generating dates.
        raw_data_path (str): The path to the directory that contains the raw data (day-ahead
            scheduling results).
        date_format (str, optional): The strftime to parse the `start_date` and `end_date` dates.
            Defaults to "%d-%m-%Y".
    """

    period = pd.date_range(
        start=pd.to_datetime(start_date, format=date_format),
        end=pd.to_datetime(end_date, format=date_format),
        freq="D",
        inclusive="both",
    )
    pbar = tqdm(total=len(period))

    data = {}
    for day in period:
        winter_time_change = (day.month == 3) and (
            day == get_last_sunday(day.year, day.month)
        )
        sday = day.strftime("%Y%m%d")
        xlfile = glob.glob(os.path.join(raw_data_path, sday) + "*")

        if len(xlfile) == 0:
            continue
        else:
            try:
                book = xlrd.open_workbook(xlfile[0], formatting_info=True)
            except xlrd.XLRDError:
                continue

        sheet = book.sheet_by_name(f"{sday}_DS")
        names = sheet.col_values(0)
        if "RENEWABLES" in names:
            idx = sheet.col_values(0).index("RENEWABLES")
        elif "RENEWABLES TOTAL" in names:
            idx = sheet.col_values(0).index("RENEWABLES TOTAL")
        else:
            raise RuntimeError("Could not find relevant field")

        data[day] = (
            np.array(sheet.row_values(idx)[1:24])
            if winter_time_change
            else np.array(sheet.row_values(idx)[1:25])
        )
        pbar.update(1)

    if not data:
        raise NoDataFound()
    
    pbar.close()
    result = pd.DataFrame.from_dict(data, orient="index", columns=range(24))
    result = result.stack()
    result.index = result.index.map(
        lambda x: datetime.datetime.combine(x[0], datetime.time(int(x[1])))
    )
    result = result.to_frame("RES generation [MW]")
    path = create_path(os.path.join(DATASET_DIR, "generation", "EL"), "RES.csv")
    result.to_csv(path, index_label="ds")


def extract_available_capacity(
    start_date: str, end_date: str, raw_data_path: str, date_format: str = "%d-%m-%Y"
):
    """Extract the available capacity dataset from the raw data.

    Args:
        start_date (str): Left bound for generating dates.
        end_date (str): Right bound for generating dates.
        raw_data_path (str): The path to the directory that contains the raw data (plant
            availabilities).
        date_format (str, optional): The strftime to parse the `start_date` and `end_date` dates.
            Defaults to "%d-%m-%Y".
    """
    plants = pd.read_csv(os.path.join(DATASET_DIR, "plants", "EL", "plants.csv"))
    unit_names = plants["Unit"].to_list()

    period = pd.date_range(
        start=pd.to_datetime(start_date, format=date_format),
        end=pd.to_datetime(end_date, format=date_format),
        freq="D",
        inclusive="both",
    )
    pbar = tqdm(total=len(period))
    data = defaultdict(dict)

    for day in period:
        sday = day.strftime("%Y%m%d")
        xlfile = glob.glob(os.path.join(raw_data_path, sday) + "*")

        if len(xlfile) == 0:
            continue
        else:
            try:
                book = xlrd.open_workbook(xlfile[0], formatting_info=True)
            except xlrd.XLRDError:
                continue

        sheet = book.sheet_by_name("Unit_MaxAvail_Publish")
        all_names = sheet.col_values(1)
        for name in set(unit_names).intersection(all_names):
            idx = all_names.index(name)
            data[day][name] = float(sheet.cell(idx, 3).value)
        pbar.update(1)

    pbar.close()

    if not data:
        raise NoDataFound()
    
    result = pd.DataFrame.from_dict(data, orient="index")
    path = create_path(os.path.join(DATASET_DIR, "capacity", "EL"), "available.csv")
    result.to_csv(path, index_label="ds")


def extract_reservoir_levels(
    start_date: str, end_date: str, raw_data_path: str, date_format: str = "%d-%m-%Y"
):
    """Extract the water reservoir levels (for hydro plants) dataset from the raw data.

    Args:
        start_date (str): Left bound for generating dates.
        end_date (str): Right bound for generating dates.
        raw_data_path (str): The path to the directory that contains the raw data (hydro
            reservoirs).
        date_format (str, optional): The strftime to parse the `start_date` and `end_date` dates.
            Defaults to "%d-%m-%Y".
    """
    period = pd.date_range(
        start=pd.to_datetime(start_date, format=date_format),
        end=pd.to_datetime(end_date, format=date_format),
        freq="D",
        inclusive="both",
    )
    pbar = tqdm(total=len(period))

    data = {}
    for day in period:
        sday = day.strftime("%Y%m%d")
        xlfile = glob.glob(os.path.join(raw_data_path, sday) + "*")

        if len(xlfile) == 0:
            continue
        else:
            try:
                book = xlrd.open_workbook(xlfile[0], formatting_info=True)
            except xlrd.XLRDError:
                continue

        sheet = book.sheet_by_name(f"{sday}ReservoirFillingRate")
        data[day] = [item for item in sheet.row_values(2) if type(item) == float][0]
        pbar.update(1)

    pbar.close()

    if not data:
        raise NoDataFound()
    
    result = pd.DataFrame.from_dict(data, orient="index", columns=["Average"])
    result["Average"] = (
        result["Average"]
        .mask(result["Average"] == 0)
        .fillna(method="ffill")
        .fillna(method="bfill")
    )

    long_term = result["Average"].groupby(lambda x: x.dayofyear).mean().to_dict()
    result["LT_Average"] = np.array(result.index.map(lambda x: long_term[x.dayofyear]))
    path = create_path(os.path.join(DATASET_DIR, "hydro", "EL"), "reservoirs.csv")
    result.to_csv(path, index_label="ds")


def extract_import_ntc(
    start_date: str, end_date: str, raw_data_path: str, date_format: str = "%d-%m-%Y"
):
    """Extract data for total NTC (net transfer capacity) for imports.

    Args:
        start_date (str): Left bound for generating dates.
        end_date (str): Right bound for generating dates.
        raw_data_path (str): The path to the directory that contains the raw data (day-ahead
            scheduling results).
        date_format (str, optional): The strftime to parse the `start_date` and `end_date` dates.
            Defaults to "%d-%m-%Y".
    """

    start_date = pd.to_datetime(start_date, format=date_format)
    period = pd.date_range(
        start=datetime.date(start_date.year, start_date.month, 1),
        end=pd.to_datetime(end_date, format=date_format),
        freq="MS",
        inclusive="both",
    )
    pbar = tqdm(total=len(period))

    result = []
    for day in period:
        sday = day.strftime("%Y%m%d")
        xlfile = glob.glob(os.path.join(raw_data_path, sday) + "*")

        if len(xlfile) == 0:
            continue
        else:
            try:
                book = xlrd.open_workbook(xlfile[0], formatting_info=True)
            except xlrd.XLRDError:
                continue

        sheet = book.sheet_by_name("IMPORTS")
        row = sheet.row_values(2)
        nodes = [name for name in row if name and not "INTERCONNECTION" in name]
        imports = {}
        for i, name in enumerate(row):
            if name in nodes:
                start, end = sheet.col_values(i)[3:5]
                index = pd.date_range(
                    pd.to_datetime(start, format="%d.%m.%Y"),
                    pd.to_datetime(end, format="%d.%m.%Y"),
                    freq="D",
                )
                data = pd.DataFrame(
                    data=np.tile(np.array(sheet.col_values(i)[6:30]), (len(index), 1)),
                    index=index,
                    columns=range(24),
                )
                if name in imports:
                    imports[name] = pd.concat((imports[name], data))
                else:
                    imports[name] = data

        total = 0
        for df in imports.values():
            total += df
        result.append(total)
        pbar.update(1)

    pbar.close()

    if not result:
        raise NoDataFound()
    
    result = pd.concat(result)
    result = result.stack()
    result.index = result.index.map(lambda x: x[0].replace(hour=int(x[1])))
    result = result.to_frame("Total import NTC [MW]")
    path = create_path(os.path.join(DATASET_DIR, "ntc", "EL"), "imports.csv")
    result.to_csv(path, index_label="ds")


def extract_export_ntc(
    start_date: str, end_date: str, raw_data_path: str, date_format: str = "%d-%m-%Y"
):
    """Extract data for total NTC (net transfer capacity) for exports.

    Args:
        start_date (str): Left bound for generating dates.
        end_date (str): Right bound for generating dates.
        raw_data_path (str): The path to the directory that contains the raw data (day-ahead
            scheduling results).
        date_format (str, optional): The strftime to parse the `start_date` and `end_date` dates.
            Defaults to "%d-%m-%Y".
    """

    start_date = pd.to_datetime(start_date, format=date_format)
    period = pd.date_range(
        start=datetime.date(start_date.year, start_date.month, 1),
        end=pd.to_datetime(end_date, format=date_format),
        freq="MS",
        inclusive="both",
    )
    pbar = tqdm(total=len(period))

    result = []
    for day in period:
        sday = day.strftime("%Y%m%d")
        xlfile = glob.glob(os.path.join(raw_data_path, sday) + "*")

        if len(xlfile) == 0:
            continue
        else:
            try:
                book = xlrd.open_workbook(xlfile[0], formatting_info=True)
            except xlrd.XLRDError:
                continue

        sheet = book.sheet_by_name("EXPORTS")
        row = sheet.row_values(2)
        nodes = [name for name in row if name and not "INTERCONNECTION" in name]
        exports = {}
        for i, name in enumerate(row):
            if name in nodes:
                start, end = sheet.col_values(i)[3:5]
                index = pd.date_range(
                    pd.to_datetime(start, format="%d.%m.%Y"),
                    pd.to_datetime(end, format="%d.%m.%Y"),
                    freq="D",
                )
                data = pd.DataFrame(
                    data=np.tile(np.array(sheet.col_values(i)[6:30]), (len(index), 1)),
                    index=index,
                    columns=range(24),
                )
                if name in exports:
                    exports[name] = pd.concat((exports[name], data))
                else:
                    exports[name] = data

        total = 0
        for df in exports.values():
            total += df
        result.append(total)
        pbar.update(1)

    pbar.close()

    if not result:
        raise NoDataFound()

    result = pd.concat(result)
    result = result.stack()
    result.index = result.index.map(lambda x: x[0].replace(hour=int(x[1])))
    result = result.to_frame("Total export NTC [MW]")
    path = create_path(os.path.join(DATASET_DIR, "ntc", "EL"), "exports.csv")
    result.to_csv(path, index_label="ds")
