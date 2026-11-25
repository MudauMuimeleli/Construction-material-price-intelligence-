"""
Construction Material Price Intelligence
Run: python src/analyse_prices.py
Dependencies: pandas, numpy, matplotlib
All input prices are simulated portfolio-project data, not live supplier quotes.
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "supplier_prices_raw.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

UNIT_MAP = {
    "bag": "bag", "50 kg bag": "bag",
    "kg": "kg", "ton": "kg",
    "linear metre": "m", "lm": "m", "linear m": "m",
    "m3": "m3", "cubic metre": "m3", "m³": "m3",
    "each": "each", "unit": "each",
    "metre": "m", "meter": "m", "m": "m"
}

def clean_prices(df):
    df = df.copy()
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["quote_date"] = pd.to_datetime(df["quote_date"], errors="coerce")
    df["currency"] = df["currency"].astype(str).str.strip().str.upper()
    df["unit_original"] = df["unit"].astype(str).str.strip().str.lower()
    df["unit_standard"] = df["unit_original"].map(UNIT_MAP)
    df["supplier"] = df["supplier"].astype(str).str.strip()
    df["city"] = df["city"].astype(str).str.strip()

    # Convert bulk steel pricing from R/tonne to R/kg.
    tonne_rows = df["unit_original"].eq("ton")
    df.loc[tonne_rows, "price"] = df.loc[tonne_rows, "price"] / 1000
    df.loc[tonne_rows, "unit_standard"] = "kg"

    # Keep only valid South African rand prices and supported units.
    valid = (
        df["currency"].eq("R") &
        df["price"].gt(0) &
        df["unit_standard"].notna() &
        df["material_id"].notna() &
        df["supplier"].ne("Unknown Supplier") &
        df["quote_date"].notna()
    )
    rejected = df.loc[~valid].copy()
    clean = df.loc[valid].copy()

    # Remove exact duplicate quote records.
    clean = clean.drop_duplicates(
        subset=["material_id", "supplier", "city", "price", "unit_standard", "quote_date"]
    )

    # Comparable price basis: price per standard unit.
    clean["price_per_standard_unit"] = clean["price"]
    clean["standard_unit"] = clean["unit_standard"]

    return clean, rejected

def create_outputs(clean, rejected):
    clean.to_csv(OUT / "supplier_prices_clean.csv", index=False)
    rejected.to_csv(OUT / "rejected_records.csv", index=False)

    summary = (clean.groupby(["material_id", "material_name", "category", "standard_unit"])
               ["price_per_standard_unit"]
               .agg(supplier_count="count", min_price="min", avg_price="mean",
                    median_price="median", max_price="max")
               .reset_index())
    summary["price_spread"] = summary["max_price"] - summary["min_price"]
    summary["spread_pct_of_min"] = (summary["price_spread"] / summary["min_price"] * 100).round(2)
    summary.to_csv(OUT / "material_price_benchmarks.csv", index=False)

    supplier = (clean.groupby(["material_id", "material_name", "supplier", "city", "standard_unit"])
                ["price_per_standard_unit"].mean().reset_index())
    supplier.to_csv(OUT / "supplier_comparison.csv", index=False)

    # Chart 1: mean benchmark price by material (different units remain labelled).
    fig, ax = plt.subplots(figsize=(10, 5))
    labels = summary["material_name"] + " (R/" + summary["standard_unit"] + ")"
    ax.bar(labels, summary["avg_price"])
    ax.set_title("Average Supplier Price by Material")
    ax.set_ylabel("Average price (R per standard unit)")
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    fig.savefig(OUT / "average_price_by_material.png", dpi=160)
    plt.close(fig)

    # Chart 2: price spread percentage by material.
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(summary["material_name"], summary["spread_pct_of_min"])
    ax.set_title("Supplier Price Spread by Material")
    ax.set_ylabel("Price spread (% of minimum price)")
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    fig.savefig(OUT / "supplier_price_spread.png", dpi=160)
    plt.close(fig)

    return summary, supplier

def main():
    raw = pd.read_csv(RAW)
    clean, rejected = clean_prices(raw)
    summary, supplier = create_outputs(clean, rejected)
    print(f"Raw records: {len(raw)}")
    print(f"Clean records: {len(clean)}")
    print(f"Rejected records: {len(rejected)}")
    print("\\nMaterial benchmarks:")
    print(summary.to_string(index=False))
    print(f"\\nOutputs saved to: {OUT}")

if __name__ == "__main__":
    main()
