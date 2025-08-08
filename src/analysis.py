#!/usr/bin/env python3
import argparse, os, json
import pandas as pd
import yaml
import numpy as np

def load_params(path="params.yaml"):
    """
    Load parameters from a YAML file.
    Args:
        path (str): Path to the YAML file.
        Returns:
        dict: Parameters loaded from the file.
    """
    with open(path) as f:
        return yaml.safe_load(f)

def compute_portfolio_metrics(market_df):
    # compute simple total return per symbol over the period
    """Compute portfolio metrics based on market data.
    Args:
    market_df (pd.DataFrame): Market data.
    Returns:
    dict: Portfolio metrics including start price, end price, and total return for each symbol.
    """
    out = {}
    for sym, g in market_df.groupby("symbol"):
        g_sorted = g.sort_values("date")
        start = g_sorted.close.iloc[0]
        end = g_sorted.close.iloc[-1]
        ret = (end / start) - 1.0
        out[sym] = {"start_price": float(start), "end_price": float(end), "total_return": float(ret)}
    return out

def main():
    """
    Main function to analyze transaction data.
    This script performs analysis on transaction data, including spending summaries,
    income summaries, and portfolio metrics.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--transactions", required=True)
    parser.add_argument("--market", required=True)
    parser.add_argument("--budget", required=True)
    parser.add_argument("--spend_report", required=True)
    parser.add_argument("--out_portfolio", required=True)
    parser.add_argument("--out_budget", required=True)
    parser.add_argument("--params", default="params.yaml")
    args = parser.parse_args()

    params = load_params(args.params).get("analysis", {})
    top_n = params.get("top_n_categories", 5)

    df = pd.read_csv(args.transactions, parse_dates=["date"])
    market = pd.read_csv(args.market, parse_dates=["date"])
    with open(args.budget) as f:
        budget = json.load(f)

    # spending summary (monthly)
    spend = df.groupby(["month","category"])["amount"].sum().reset_index().rename(columns={"amount":"total_spend"})
    os.makedirs(os.path.dirname(args.spend_report), exist_ok=True)
    spend.to_csv(args.spend_report, index=False)

    # top categories overall
    top = df.groupby("category")["amount"].sum().abs().sort_values(ascending=False).head(top_n).to_dict()

    # budget adherence: compare monthly spend to monthly budget
    monthly_actual = df.groupby("category")["amount"].sum().abs()
    budgets = budget.get("monthly_budgets", {})
    adherence = {}
    for cat, bval in budgets.items():
        actual = float(monthly_actual.get(cat, 0.0))
        score = None
        if bval > 0:
            score = max(0.0, 1.0 - abs(actual - bval) / bval)  # 1.0 best, decreasing as diverges
        adherence[cat] = {"budget": float(bval), "actual": actual, "adherence_score": score}

    # portfolio metrics
    portfolio_metrics = compute_portfolio_metrics(market)

    os.makedirs(os.path.dirname(args.out_portfolio), exist_ok=True)
    with open(args.out_portfolio, "w") as fh:
        json.dump({"top_categories": top, "portfolio": portfolio_metrics}, fh, indent=2)

    os.makedirs(os.path.dirname(args.out_budget), exist_ok=True)
    with open(args.out_budget, "w") as fh:
        json.dump(adherence, fh, indent=2)

    print("Analysis done. spend_report:", args.spend_report)

if __name__ == "__main__":
    main()
     