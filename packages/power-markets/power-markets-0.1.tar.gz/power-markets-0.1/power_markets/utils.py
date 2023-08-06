# -*- coding: utf-8 -*-
# Copyright (c) Hebes Intelligence Private Company

# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import datetime
from pathlib import Path

from dateutil.rrule import SU as Sunday
from dateutil.rrule import WEEKLY, rrule


def create_path(path: str, output_file: str):
    output_dir = Path(path)
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir / output_file


def get_last_sunday(year, month):
    date = datetime.datetime(year=year, month=month, day=1)
    # we can find max 5 sundays in a months
    days = rrule(freq=WEEKLY, dtstart=date, byweekday=Sunday, count=5)
    # Check if last date is same month,
    # If not this couple year/month only have 4 Sundays
    if days[-1].month == month:
        return days[-1]
    else:
        return days[-2]
