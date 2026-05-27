from pathlib import Path

import pandas as pd

from src.metrics import compute_summary, spend_by_category


def _transactions_for_export(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if pd.api.types.is_datetime64_any_dtype(out["date"]):
        out["date"] = out["date"].dt.strftime("%Y-%m-%d")
    return out


def _summary_overview_df(summary: pd.Series) -> pd.DataFrame:
    return summary.reset_index().rename(columns={"index": "metric", 0: "value"})


def _write_summary_sheet(
    writer: pd.ExcelWriter,
    summary: pd.Series,
    by_category: pd.DataFrame,
) -> None:
    overview = _summary_overview_df(summary)
    overview.to_excel(writer, sheet_name="Summary", index=False, startrow=0)
    start = len(overview) + 2
    by_category.to_excel(writer, sheet_name="Summary", index=False, startrow=start)


def write_report(df: pd.DataFrame, output_path: Path) -> list[Path]:
    output_path = Path(output_path).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    suffix = output_path.suffix.lower()

    transactions = _transactions_for_export(df)
    summary = compute_summary(df)
    by_category = spend_by_category(df)
    written = [output_path]

    if suffix == ".csv":
        transactions.to_csv(output_path, index=False)
        summary_path = output_path.with_name(f"{output_path.stem}_summary{output_path.suffix}")
        overview = _summary_overview_df(summary)
        overview.to_csv(summary_path, index=False)
        category_path = output_path.with_name(
            f"{output_path.stem}_by_category{output_path.suffix}"
        )
        by_category.to_csv(category_path, index=False)
        written.extend([summary_path, category_path])
    elif suffix == ".xlsx":
        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            transactions.to_excel(writer, sheet_name="Transactions", index=False)
            _write_summary_sheet(writer, summary, by_category)
    else:
        raise ValueError(f"Unsupported output format: {suffix} (use .csv or .xlsx)")

    return written
