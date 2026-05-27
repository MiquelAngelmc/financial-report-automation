# Financial Report Automation

Takes messy bank statements or transaction logs (CSV/Excel), cleans them up, and outputs a structured file.

## Setup

Install dependencies once:

```bash
pip install -r requirements.txt
```

If `pip` is not found, use:

```bash
python -m pip install -r requirements.txt
```

## Usage

Run the pipeline (load → normalize dates and amounts → drop duplicates → write file):

```bash
python main.py -i data/raw/transactions_dirty.csv -o output/report.xlsx
```

- **`-i` / `--input`**: path to your CSV or Excel file.
- **`-o` / `--output`**: where to write the result. The format is chosen from the extension (`.csv` or `.xlsx`).

If you omit `-o`, the default is `output/<input_filename_stem>_clean.csv`.

```bash
python main.py -i data/raw/transactions_dirty.csv
```

For options:

```bash
python main.py --help
```
