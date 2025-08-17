# flows/advanced_pipeline.py
from __future__ import annotations

import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, Tuple

import numpy as np
import pandas as pd
from prefect import flow, task, get_run_logger
from prefect.artifacts import create_table_artifact, create_markdown_artifact

DATA_DIR = Path("data")
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
EXTERNAL_DIR = DATA_DIR / "external"
STATE_DIR = PROCESSED_DIR / ".state"
STATE_DIR.mkdir(parents=True, exist_ok=True)

TX_PATH = RAW_DIR / "transactions.csv"
MKT_PATH = RAW_DIR / "market_data.csv"     # e.g., symbol,date,close
BUDGET_PATH = RAW_DIR / "budget_data.json"
PORTFOLIO_OUT = PROCESSED_DIR / "portfolio_metrics.parquet"
BACKUP_DIR = DATA_DIR / "backups"

def _hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

@task(persist_result=True, retries=2, retry_delay_seconds=5)
def load_csv(path: Path) -> pd.DataFrame:
    if not Path(path).exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path)

@task(persist_result=True, retries=2, retry_delay_seconds=5)
def load_json(path: Path) -> Dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))

@task(persist_result=True)
def data_quality_check(df: pd.DataFrame, min_rows: int = 50) -> Tuple[bool, str]:
    if df is None or len(df) < min_rows:
        return False, f"Too few rows: {0 if df is None else len(df)} < {min_rows}"
    if df.isna().mean().mean() > 0.2:
        return False, "More than 20% NA across the frame"
    return True, "ok"

@task(
    persist_result=True,
    # Cache by inputs' fingerprints so we skip recomputation when sources unchanged
    cache_key_fn=lambda c, p: f"valuation_{p['tx_hash']}_{p['mkt_hash']}",
    cache_expiration=timedelta(hours=12),
)
def compute_portfolio_valuation(
    tx: pd.DataFrame,
    market: pd.DataFrame,
    tx_hash: str,
    mkt_hash: str,
) -> pd.DataFrame:
    """Toy example: join on date/symbol-like info to produce a value series."""
    logger = get_run_logger()
    df = tx.copy()
    df["date"] = pd.to_datetime(df["date"])
    market["date"] = pd.to_datetime(market["date"])

    # Suppose transaction ["symbol","shares"] exist; if not, fake a small demo field
    if "symbol" not in df.columns:
        df["symbol"] = "CASH"
    if "shares" not in df.columns:
        df["shares"] = np.where(df["amount"] > 0, 0, 0)  # placeholder

    # Last close per symbol/date
    last_close = (
        market.sort_values(["symbol", "date"])
              .groupby(["symbol", "date"], as_index=False)["close"].last()
    )

    merged = pd.merge(df, last_close, how="left", on=["symbol", "date"])
    merged["position_value"] = merged["shares"].fillna(0) * merged["close"].fillna(1.0)

    daily_value = (
        merged.groupby("date", as_index=False)["position_value"].sum()
              .rename(columns={"position_value": "portfolio_value"})
              .sort_values("date")
    )
    logger.info(f"Valuation points: {len(daily_value)}")
    return daily_value

@task(persist_result=True, retries=1, retry_delay_seconds=3)
def persist_portfolio(df: pd.DataFrame, out_path: Path = PORTFOLIO_OUT) -> str:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_path, index=False)

    # ensure datetime columns are JSON serializable
    df = df.copy()
    for col in df.select_dtypes(include=["datetime64[ns]", "datetimetz"]):
        df[col] = df[col].astype(str)
    create_table_artifact(
        table=df.tail(10).to_dict(orient="list"),
        key="portfolio-tail",
        description="Last 10 portfolio value points",
    )
    return str(out_path)

@task(persist_result=True)
def fingerprint_inputs(paths: Tuple[Path, ...]) -> str:
    h = hashlib.sha256()
    for p in sorted(paths):
        h.update(_hash_file(p).encode())
    return h.hexdigest()

@task(persist_result=True)
def was_data_changed(fingerprint: str, state_key: str) -> bool:
    state_file = STATE_DIR / f"{state_key}.txt"
    prev = state_file.read_text().strip() if state_file.exists() else ""
    changed = (prev != fingerprint)
    if changed:
        state_file.write_text(fingerprint)
    return changed

@task(persist_result=True)
def backup_processed(source_dir: Path = PROCESSED_DIR, backup_dir: Path = BACKUP_DIR) -> str:
    backup_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    # simple copy: per-file timestamp suffix
    copied = []
    for p in source_dir.rglob("*.*"):
        if p.is_file():
            dest = backup_dir / f"{p.stem}_{stamp}{p.suffix}"
            dest.write_bytes(p.read_bytes())
            copied.append(dest.name)
    create_markdown_artifact(
        markdown=f"Backed up **{len(copied)}** files to `{backup_dir}` at {stamp}",
        key="processed-backups",
    )
    return f"{len(copied)} files"

# ---------- Main advanced flow ----------

@flow(name="advanced-data-pipeline", persist_result=True)
def advanced_data_pipeline(
    tx_path: Path = TX_PATH,
    market_path: Path = MKT_PATH,
    budget_path: Path = BUDGET_PATH,
    state_key: str = "tx+mkt",
    require_change: bool = True,
) -> Optional[str]:
    """
    Combine multiple inputs; parallel load; cache heavy valuation; conditional branches; change-triggered runs.
    """
    logger = get_run_logger()

    # Parallel loading
    tx_fut = load_csv.submit(tx_path)
    mkt_fut = load_csv.submit(market_path)
    budget = load_json.submit(budget_path)  # not used directly here, but demonstrates multi-source

    # Quality checks (will wait on futures as needed)
    ok_tx, msg_tx = data_quality_check(tx_fut)
    ok_mk, msg_mk = data_quality_check(mkt_fut)

    if not ok_tx or not ok_mk:
        create_markdown_artifact(
            markdown=f"### ❌ Data quality failed\n- tx: {msg_tx}\n- market: {msg_mk}",
            key="advanced-quality",
        )
        raise ValueError(f"Data quality failed: tx={msg_tx}; market={msg_mk}")

    # Change detection gate
    fingerprint = fingerprint_inputs((Path(tx_path), Path(market_path)))
    if require_change:
        changed = was_data_changed(fingerprint, state_key)
        if not changed:
            logger.info("No data changes detected; skipping heavy compute.")
            return "skipped (no change)"

    # Cache-able heavy compute (keyed by source hashes)
    tx_hash = _hash_file(Path(tx_path))
    mkt_hash = _hash_file(Path(market_path))
    valuation = compute_portfolio_valuation(tx_fut, mkt_fut, tx_hash=tx_hash, mkt_hash=mkt_hash)

    saved = persist_portfolio(valuation)
    backup_processed()  # small safety backup on each successful run

    return f"saved: {saved}"

# ---------- Extra scheduled flows ----------

@flow(name="weekly-portfolio-analysis", persist_result=True)
def weekly_portfolio_analysis() -> str:
    df = pd.read_parquet(PORTFOLIO_OUT) if PORTFOLIO_OUT.exists() else pd.DataFrame()
    if df.empty:
        return "no data"
    week = df.tail(7)
    change = (week["portfolio_value"].iloc[-1] - week["portfolio_value"].iloc[0]) / max(1e-9, week["portfolio_value"].iloc[0])
    pct = round(100 * change, 2)
    create_markdown_artifact(markdown=f"**Weekly change:** {pct}%", key="weekly-portfolio-change")
    # Optional: notify if > ±5%
    # slack = SlackWebhook.load("finance-alerts"); slack.notify(f"Weekly portfolio change: {pct}%")
    return f"{pct}%"

@flow(name="monthly-budget-review", persist_result=True)
def monthly_budget_review(budget_path: Path = BUDGET_PATH) -> str:
    tx_file = PROCESSED_DIR / "transactions_enriched.parquet"
    if not tx_file.exists():
        return "no transactions yet"

    tx = pd.read_parquet(tx_file)

    # Extract only numeric budgets
    budget_json = json.loads(Path(budget_path).read_text())
    budget = budget_json.get("monthly_budgets", {})

    spent = tx[tx["amount"] < 0].groupby("category")["amount"].sum().abs()

    rows = []
    for k in set(budget) | set(spent.index):
        try:
            budget_val = float(budget.get(k, 0))
        except (TypeError, ValueError):
            budget_val = 0.0
        spent_val = float(spent.get(k, 0))
        rows.append({"category": k, "budget": budget_val, "spent": spent_val})

    create_table_artifact(table=rows, key="monthly-budget-review")
    return "ok"


@flow(name="processed-data-backup", persist_result=True)
def processed_data_backup() -> str:
    return backup_processed()
    
# from prefect.deployments import Deployment
# from prefect.server.schemas.schedules import CronSchedule

if __name__ == "__main__":
    # Local ad-hoc run:
    advanced_data_pipeline()

    # You **cannot** deploy programmatically like Prefect 2.
    # Instead, use the CLI or UI to schedule:
    # Example CLI:
    # prefect deployment create flows/advanced_pipeline.py:advanced_data_pipeline \
    #   --name "advanced-pipeline" \
    #   --work-pool local-pool \
    #   --cron "*/30 * * * *"
