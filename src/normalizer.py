import re
from datetime import datetime

import pandas as pd

_YEAR_FIRST = re.compile(r"^(\d{4})[-/](\d{1,2})[-/](\d{1,2})$")
_DMY = re.compile(r"^(\d{1,2})[-/](\d{1,2})[-/](\d{4})$")


def _parse_date_string(value: str) -> datetime:
    value = str(value).strip()

    match = _YEAR_FIRST.match(value)
    if match:
        year, month, day = (int(match.group(i)) for i in range(1, 4))
        return datetime(year, month, day)

    match = _DMY.match(value)
    if not match:
        raise ValueError(f"Unrecognized date format: {value!r}")

    part1, part2, year = (int(match.group(i)) for i in range(1, 4))
    separator = "/" if "/" in value else "-"

    if part1 > 12:
        day, month = part1, part2
    elif part2 > 12:
        month, day = part1, part2
    elif separator == "/":
        day, month = part1, part2
    else:
        month, day = part1, part2

    return datetime(year, month, day)


def normalize_dates(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["date"] = df["date"].apply(_parse_date_string)
    return df
