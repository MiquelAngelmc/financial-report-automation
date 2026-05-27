# Financial Report Automation

Cleans raw bank-style transaction files (CSV or `.xlsx`) and writes a normalized report with spending metrics.

The pipeline loads the file, standardizes dates and amounts, removes duplicate rows, then exports clean transactions plus a summary.

## Requirements

- Python 3.10+
- Dependencies in `requirements.txt` (pandas, openpyxl)

## Setup

```bash
python -m pip install -r requirements.txt
```

## Usage

From the project root:

```bash
python main.py -i data/raw/transactions_dirty.csv -o output/report.xlsx
```

| Flag | Meaning |
|------|---------|
| `-i`, `--input` | Input `.csv` or `.xlsx` file |
| `-o`, `--output` | Output path (format from extension: `.csv` or `.xlsx`) |

Default output if `-o` is omitted:

```bash
python main.py -i data/raw/transactions_dirty.csv
```

Writes `output/transactions_dirty_clean.csv` plus summary CSV files (see below).

```bash
python main.py --help
```

## Output

### Excel (`.xlsx`)

One workbook with two sheets:

- **Transactions** — cleaned rows (`date` as `YYYY-MM-DD`, `amount` as number)
- **Summary** — transaction count, total spend, then spend by category

### CSV (`.csv`)

Three files (CSV has no sheets):

- `<name>.csv` — transactions
- `<name>_summary.csv` — transaction count and total spend
- `<name>_by_category.csv` — spend per category

Generated files go under `output/` (gitignored).

## Example

Sample dirty data: `data/raw/transactions_dirty.csv` (mixed date formats, currency symbols, duplicate rows).

```bash
python main.py -i data/raw/transactions_dirty.csv -o output/report.xlsx
```

Typical console output:

```
Wrote 11 transactions to .../output/report.xlsx
```

After cleaning, 19 raw rows become 11 unique transactions; metrics are computed on that cleaned set.

## What gets cleaned

- Comment lines at the top of CSV exports (`# ...`)
- Dates: `DD/MM/YYYY`, `YYYY-MM-DD`, `MM/DD/YYYY`, and similar variants
- Amounts: `€`, commas, thousands separators, values in parentheses as negative
- Exact duplicate rows (same date, description, amount, category after text trim)
