#!/usr/bin/env python3
import argparse, os, json
import pandas as pd
import yaml
import numpy as np

def load_params(path="params.yaml"):
    """Load parameters from a YAML file.
    Args:
        path (str): Path to the YAML file.
        Returns:
        dict: Parameters loaded from the file.
    """
    with open(path) as f:
        return yaml.safe_load(f)

def main():
    """Main function to clean transaction data.
    This script performs basic cleaning tasks such as removing duplicates,
    handling missing values, filtering by currency and amount, and detecting outliers.
    It also generates metrics about the cleaning process.

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--metrics", required=True)
    parser.add_argument("--params", default="params.yaml")
    args = parser.parse_args()

    params = load_params(args.params).get("data_cleaning", {})
    min_amount = params.get("min_amount", 0.0)
    allowed_currencies = params.get("allowed_currencies", ["USD"])

    df = pd.read_csv(args.input, parse_dates=["date"])
    original_count = len(df)

    # basic cleaning
    df = df.drop_duplicates(subset=["transaction_id"])
    dup_removed = original_count - len(df)

    # handle missing values
    missing_before = df.isna().sum().to_dict()
    df = df.dropna(subset=["amount", "date", "category"])  # drop essential missing
    missing_after = df.isna().sum().to_dict()

    # filter currency and amounts
    df = df[df.currency.isin(allowed_currencies)]
    df = df[df.amount.abs() >= min_amount]  # keep refunds if >= threshold

    # outlier detection (IQR on amount)
    q1 = df.amount.quantile(0.25)
    q3 = df.amount.quantile(0.75)
    iqr = q3 - q1 if q3>q1 else 0
    lower = q1 - 1.5*iqr
    upper = q3 + 1.5*iqr
    outliers = df[(df.amount < lower) | (df.amount > upper)]
    outlier_count = len(outliers)

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    df.to_csv(args.output, index=False)

    metrics = {
        "original_count": int(original_count),
        "after_clean_count": int(len(df)),
        "duplicates_removed": int(dup_removed),
        "missing_before": {k:int(v) for k,v in missing_before.items()},
        "missing_after": {k:int(v) for k,v in missing_after.items()},
        "outlier_count": int(outlier_count),
        "min_amount_threshold": float(min_amount)
    }
    os.makedirs(os.path.dirname(args.metrics), exist_ok=True)
    with open(args.metrics, "w") as fh:
        json.dump(metrics, fh, indent=2)
    print("Cleaning done. Metrics:", metrics)

if __name__ == "__main__":
    main()
