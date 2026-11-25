# Construction Material Price Intelligence

## Overview
A reproducible data analytics portfolio project that cleans supplier quote data, standardises measurement units, benchmarks construction material prices and compares suppliers. It demonstrates a workflow relevant to construction technology platforms and estimation products.

**Important data note:** All supplier names, dates and prices in `data/supplier_prices_raw.csv` are simulated examples created for this portfolio project. They are not verified supplier quotations, live market prices or a representation of actual BuildEase data. Do not use them for procurement or project costing.

## Business questions
1. What is the average, minimum and maximum quoted price for each material?
2. How much do supplier prices vary for the same material?
3. Which records should be rejected during data quality checks?
4. How can inconsistent units (e.g. tonne vs kg, m³ vs cubic metre) be standardised before comparison?

## Tools
- Python
- Pandas and NumPy
- Matplotlib
- SQL (SQLite-compatible queries)

## Data workflow
1. Load raw supplier quotes from CSV.
2. Parse prices and dates and normalise text fields.
3. Standardise unit labels.
4. Convert steel price quoted per tonne into price per kg.
5. Reject invalid/non-positive prices, unsupported units, unknown suppliers and invalid currencies/dates.
6. Remove duplicate quote records.
7. Calculate material-level benchmarks and supplier comparisons.
8. Export cleaned data, rejected records, benchmark tables and charts.

## Run locally
Install dependencies:
```bash
pip install pandas numpy matplotlib
```
Run:
```bash
python src/analyse_prices.py
```
Generated files are saved in `outputs/`.

## Project structure
```text
Construction_Material_Price_Intelligence/
├── data/
│   └── supplier_prices_raw.csv
├── outputs/
│   ├── supplier_prices_clean.csv
│   ├── rejected_records.csv
│   ├── material_price_benchmarks.csv
│   ├── supplier_comparison.csv
│   ├── average_price_by_material.png
│   └── supplier_price_spread.png
├── sql/
│   └── analysis_queries.sql
├── src/
│   └── analyse_prices.py
└── README.md
```

## Limitations and next steps
- The sample is small and simulated; findings are illustrative only.
- A production version should ingest dated supplier catalogues/quotes, preserve source provenance, validate VAT and delivery-cost treatment, and define exact product specifications.
- Unit conversion must be material-specific. A bag, length, grade or diameter must not be assumed interchangeable merely because labels look similar.
- Next iteration: add regional trend analysis over multiple months, outlier flags, a Power BI/Looker Studio dashboard, and a BOQ-versus-actual quantity audit dataset.
