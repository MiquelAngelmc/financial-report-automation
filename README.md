# Financial Report Automation

Python-based tool that cleans raw financial transaction data (bank statements, operation logs) and generates structured reports.

## Features (planned)

- Load CSV and Excel files with pandas
- Remove duplicate transactions
- Standardize date and currency formats
- Calculate key metrics (e.g. total spend by category)
- Export clean reports to Excel

## Project structure

```
financial-report-automation/
├── data/
│   └── raw/          # Input files (dirty transaction logs)
├── output/           # Generated reports (gitignored)
├── src/              # Core processing modules
├── main.py           # CLI entry point (coming soon)
└── requirements.txt
```

## Setup

```bash
pip install -r requirements.txt
```
