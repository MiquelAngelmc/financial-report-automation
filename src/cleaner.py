import pandas as pd

# Two rows are duplicates when all of these columns match exactly.
DEDUP_COLUMNS = ("date", "description", "amount", "category")


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["description"] = df["description"].astype(str).str.strip()
    df["category"] = df["category"].astype(str).str.strip()

    return df.drop_duplicates(subset=DEDUP_COLUMNS, keep="first").reset_index(drop=True)
