"""Quick manual check from repo root: python scripts/smoke_pipeline.py"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from main import build_clean_dataframe

DATA = ROOT / "data" / "raw" / "transactions_dirty.csv"


def main() -> None:
    df = build_clean_dataframe(DATA)
    print(f"rows: {len(df)}")
    print("amounts:", df["amount"].tolist())


if __name__ == "__main__":
    main()
