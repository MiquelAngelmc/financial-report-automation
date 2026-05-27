import argparse
from pathlib import Path

from src.cleaner import remove_duplicates
from src.loader import load_transactions
from src.normalizer import normalize_amounts, normalize_dates


def build_clean_dataframe(input_path: Path):
    df = load_transactions(input_path)
    df = normalize_dates(df)
    df = normalize_amounts(df)
    df = remove_duplicates(df)
    return df


def write_output(df, output_path: Path) -> None:
    output_path = output_path.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    suffix = output_path.suffix.lower()
    if suffix == ".csv":
        df.to_csv(output_path, index=False)
    elif suffix in (".xlsx", ".xls"):
        df.to_excel(output_path, index=False)
    else:
        raise ValueError(f"Unsupported output format: {suffix} (use .csv or .xlsx)")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Clean bank-style transactions (CSV or Excel) and write a normalized file.",
    )
    parser.add_argument(
        "--input",
        "-i",
        type=Path,
        required=True,
        help="Input CSV or Excel path",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="Output path (.csv or .xlsx). Default: output/<input_stem>_clean.csv",
    )
    args = parser.parse_args()

    input_path = args.input.resolve()
    if args.output is not None:
        output_path = args.output
    else:
        output_path = Path("output") / f"{input_path.stem}_clean.csv"

    df = build_clean_dataframe(input_path)
    write_output(df, output_path)
    print(f"Wrote {len(df)} rows to {output_path.resolve()}")


if __name__ == "__main__":
    main()
