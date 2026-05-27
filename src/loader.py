from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = ("date", "description", "amount", "category")

def load_transactions(path: str | Path) -> pd.DataFrame:
    # Load a transaction file (CSV or Excel) into a DataFrame.
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)

    suffix = path.suffix.lower()
    if suffix == ".csv":
        df = pd.read_csv(path, comment="#")
    elif suffix in (".xlsx", ".xls"):
        df = pd.read_excel(path)
    else:
        raise ValueError(f"Unsupported file type: {suffix}")

    df.columns = df.columns.str.strip().str.lower()
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {', '.join(missing)}")

    return df
