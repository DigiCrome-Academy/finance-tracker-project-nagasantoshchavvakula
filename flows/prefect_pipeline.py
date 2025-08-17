# flows/prefect_pipeline.py
from prefect import flow

# Import the flows we just wrote
from flows.basic_pipeline import daily_transactions_flow
from flows.advanced_pipeline import (
    advanced_data_pipeline,
    weekly_portfolio_analysis,
    monthly_budget_review,
    processed_data_backup,
)

@flow(name="run-all-now")
def run_all_now():
    daily_transactions_flow()
    advanced_data_pipeline()
    weekly_portfolio_analysis()
    monthly_budget_review()
    processed_data_backup()

def deploy_all(work_pool: str = "local-pool"):
    # One-liners to (re)create deployments with schedules
    daily_transactions_flow.deploy(
        name="daily-transactions",
        work_pool_name=work_pool,
        cron="0 8 * * *", timezone="America/New_York",
    )
    advanced_data_pipeline.deploy(
        name="advanced-pipeline",
        work_pool_name=work_pool,
        cron="*/30 * * * *", timezone="America/New_York",
    )
    weekly_portfolio_analysis.deploy(
        name="weekly-portfolio",
        work_pool_name=work_pool,
        cron="30 8 * * MON", timezone="America/New_York",
    )
    monthly_budget_review.deploy(
        name="monthly-budget",
        work_pool_name=work_pool,
        cron="0 9 1 * *", timezone="America/New_York",
    )
    processed_data_backup.deploy(
        name="nightly-backup",
        work_pool_name=work_pool,
        cron="0 2 * * *", timezone="America/New_York",
    )

if __name__ == "__main__":
    # Run everything once:
    run_all_now()

    # Or just create (or update) all deployments + schedules:
    # deploy_all()