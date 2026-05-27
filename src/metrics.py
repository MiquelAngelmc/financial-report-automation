import pandas as pd


def compute_summary(df: pd.DataFrame) -> pd.Series:
    return pd.Series(
        {
            "transaction_count": len(df),
            "total_spend": df["amount"].sum(),
        }
    )


def spend_by_category(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("category", as_index=False)["amount"]
        .sum()
        .rename(columns={"amount": "total_spend"})
        .sort_values("total_spend", ascending=False)
        .reset_index(drop=True)
    )
