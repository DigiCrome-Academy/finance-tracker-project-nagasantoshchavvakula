# flows/basic_pipeline.py

from datetime import datetime, timezone
import logging
import pandas as pd
import json
from pathlib import Path

from prefect import flow, task
# from prefect.filesystems import LocalFileSystem

# ----------------------------
# Logger setup
# ----------------------------
logger = logging.getLogger("finance-tracker")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

# ----------------------------
# Tasks
# ----------------------------
@task
def load_transactions(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    logger.info(f"Loaded {len(df)} transactions from {file_path}")
    return df

@task
def validate_transactions(df: pd.DataFrame) -> pd.DataFrame:
    # Example: drop rows with missing amounts
    df = df.dropna(subset=["amount"])
    return df

@task
def categorize_transactions(df: pd.DataFrame) -> pd.DataFrame:
    # Example: simple categorization
    df["category"] = df["category"].apply(
        lambda x: "transport" if "bus" in x.lower() else "other"
    )
    return df

@task
def calculate_balances(df: pd.DataFrame) -> pd.DataFrame:
    df["balance"] = df["amount"].cumsum()
    return df

@task
def load_budget(file_path: str) -> dict:
    with open(file_path, "r") as f:
        budget = json.load(f)
    return budget

@task
def generate_budget_alerts(df: pd.DataFrame, budget_json: dict):
    budgets = budget_json["monthly_budgets"]  # extract the numeric limits
    for category, limit in budgets.items():
        spent = df[df["category"] == category]["amount"].sum()
        if spent > limit:
            logger.warning(
                f"⚠️ Budget overrun in {category}: spent {spent} vs limit {limit} {budget_json.get('currency', '')}"
            )


@task
def persist_processed(df: pd.DataFrame, output_path: str):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path)
    return output_path

# ----------------------------
# Flow
# ----------------------------
@flow(name="daily-transactions-flow")
def daily_transactions_flow():
    logger.info(f"Starting daily flow at {datetime.now(timezone.utc).isoformat()}")
    
    transactions = load_transactions("data/raw/transactions.csv")
    transactions = validate_transactions(transactions)
    transactions = categorize_transactions(transactions)
    transactions = calculate_balances(transactions)
    
    budget = load_budget("data/raw/budget_data.json")
    generate_budget_alerts(transactions, budget)
    
    output_file = persist_processed(transactions, "data/processed/transactions_enriched.parquet")
    logger.info(f"Flow complete. Output: {output_file}")

# ----------------------------
# Main: local run + deploy
# ----------------------------



if __name__ == "__main__":
    # Run flow locally (ad-hoc)
    daily_transactions_flow()

    # Deploy the flow with local infrastructure
    # daily_transactions_flow.deploy(
    #     name="daily-transactions",
    #     work_pool_name="local-pool",
    #     cron="0 8 * * *",  # daily at 08:00 UTC
        
    # )

