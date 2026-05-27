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


def _parse_amount(value) -> float:
    if pd.isna(value):
        raise ValueError("amount is empty")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)

    s = str(value).strip()
    negative = False
    if s.startswith("(") and s.endswith(")"):
        negative = True
        s = s[1:-1].strip()
    elif s.startswith("-"):
        negative = True
        s = s[1:].strip()

    for sym in "€$£ ":
        s = s.replace(sym, "")
    s = s.strip()
    if not s:
        raise ValueError(f"Invalid amount: {value!r}")

    has_comma = "," in s
    has_dot = "." in s

    if has_comma and has_dot:
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    elif has_comma:
        s = s.replace(",", ".")
    elif s.count(".") > 1:
        parts = s.split(".")
        s = "".join(parts[:-1]) + "." + parts[-1]

    result = float(s)
    return -result if negative else result


def normalize_amounts(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["amount"] = df["amount"].apply(_parse_amount)
    return df
