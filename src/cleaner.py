import pandas as pd


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    # Drop duplicate transactions, keeping the first occurrence.
    return df.drop_duplicates(keep="first").reset_index(drop=True)
