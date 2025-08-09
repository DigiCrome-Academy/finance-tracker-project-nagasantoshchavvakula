#!/usr/bin/env python3
import argparse
import os
import json
import pandas as pd
import matplotlib.pyplot as plt

def main():
    """
    Main function to generate reports and plots from analysis results.
    This script reads the spending report, portfolio metrics, and budget adherence,
    generates visualizations, and writes a summary report.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--spend_report", required=True)
    parser.add_argument("--portfolio_metrics", required=True)
    parser.add_argument("--budget_metrics", required=True)
    parser.add_argument("--out_report", required=True)
    parser.add_argument("--out_plots_dir", required=True)
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.out_report), exist_ok=True)
    os.makedirs(args.out_plots_dir, exist_ok=True)

    spend = pd.read_csv(args.spend_report)
    # simple aggregate for plot
    agg = spend.groupby("category")["total_spend"].sum().sort_values(ascending=False)
    plt.figure()
    agg.plot(kind="bar")
    plt.title("Spend by Category")
    spend_plot = os.path.join(args.out_plots_dir, "spend_by_category.png")
    plt.tight_layout()
    plt.savefig(spend_plot)
    plt.close()

    with open(args.portfolio_metrics) as fh:
        portfolio = json.load(fh)["portfolio"]
    # plot simple total returns
    syms = list(portfolio.keys())
    rets = [portfolio[s]["total_return"] for s in syms]
    plt.figure()
    pd.Series(rets, index=syms).plot(kind="bar")
    plt.title("Portfolio total returns (period)")
    port_plot = os.path.join(args.out_plots_dir, "portfolio_returns.png")
    plt.tight_layout()
    plt.savefig(port_plot)
    plt.close()

    # Write summary markdown
    with open(args.budget_metrics) as fh:
        budgets = json.load(fh)
    with open(args.out_report, "w") as r:
        r.write("# Summary Report\n\n")
        r.write("## Top categories (aggregate spend)\n\n")
        top = agg.head(10)
        r.write(top.to_markdown() + "\n\n")
        r.write("## Budget adherence (sample)\n\n")
        # convert budgets to table
        bdf = pd.DataFrame.from_dict(budgets, orient="index")
        r.write(bdf.to_markdown() + "\n\n")
        r.write("## Plots\n\n")
        r.write(f"- Spend by category: {spend_plot}\n")
        r.write(f"- Portfolio returns: {port_plot}\n")
    print("Report and plots created:", args.out_report, spend_plot, port_plot)

if __name__ == "__main__":
    main()
