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
    import yaml
    with open(path) as f:
        return yaml.safe_load(f)

def main():
    """
    Main function to create features from transaction data.
    This script generates additional features such as absolute amount, log-transformed amount,
    month, day of week, weekend indicator, and rolling averages.
    It reads the input CSV, applies transformations, and writes the output to a new CSV file
    """ 
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--params", default="params.yaml")
    args = parser.parse_args()
    params = load_params(args.params).get("feature_engineering", {})
    rolling_window = params.get("rolling_window", 7)

    df = pd.read_csv(args.input, parse_dates=["date"])
    # simple features
    df["abs_amount"] = df.amount.abs()
    df["amount_log1p"] = np.log1p(df["abs_amount"])
    df["month"] = df.date.dt.to_period("M").astype(str)
    df["day_of_week"] = df.date.dt.day_name()
    df["is_weekend"] = df.day_of_week.isin(["Saturday","Sunday"]).astype(int)

    # rolling avg per user
    df = df.sort_values(["user_id","date"])
    df["rolling_amount_mean"] = df.groupby("user_id")["amount"].transform(lambda x: x.rolling(rolling_window, min_periods=1).mean())

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    df.to_csv(args.output, index=False)
    print("Features written:", args.output)

if __name__ == "__main__":
    main()
