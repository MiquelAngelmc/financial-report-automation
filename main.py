import argparse
from pathlib import Path

from src.cleaner import remove_duplicates
from src.loader import load_transactions
from src.normalizer import normalize_amounts, normalize_dates
from src.reporter import write_report


def build_clean_dataframe(input_path: Path):
    df = load_transactions(input_path)
    df = normalize_dates(df)
    df = normalize_amounts(df)
    df = remove_duplicates(df)
    return df


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
    written = write_report(df, output_path)
    print(f"Wrote {len(df)} transactions to {written[0]}")
    for path in written[1:]:
        print(f"  summary: {path}")


if __name__ == "__main__":
    main()
