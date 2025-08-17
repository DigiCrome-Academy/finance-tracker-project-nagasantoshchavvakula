# data_pipeline.py
from functools import reduce
from typing import List, Dict, Any, Callable
from utils import (
    log_execution, handle_exceptions, clean_amount, validate_transaction,
    filter_negative_transactions, filter_positive_transactions
)

#------------------------------------------
# Custom exceptions
#------------------------------------------
class DataValidationError(Exception):
    """Custom exception for data validation errors."""
    pass

#------------------------------------------
# Function composition helper
#------------------------------------------
def compose(*functions: Callable) -> Callable:
    """Compose multiple functions into a single callable."""
    def composed(data: Any) -> Any:
        for func in reversed(functions):
            data = func(data)
        return data
    return composed

#------------------------------------------
# Data transformation functions
#------------------------------------------
@log_execution
def transform_amount(transaction: Dict[str, Any]) -> Dict[str, Any]:
    transaction['amount'] = clean_amount(transaction['amount'])
    return transaction

@log_execution
def upper_case_category(transaction: Dict[str, Any]) -> Dict[str, Any]:
    if 'category' in transaction and isinstance(transaction['category'], str):
        transaction['category'] = transaction['category'].upper()
    return transaction

#------------------------------------------
# Validation pipeline
#------------------------------------------
@handle_exceptions
def validate_pipeline(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    valid_transactions = [tx for tx in transactions if validate_transaction(tx)]
    if len(valid_transactions) != len(transactions):
        raise DataValidationError("Some transactions failed validation.")
    return valid_transactions

#------------------------------------------
# Processing pipeline
#------------------------------------------
def process_transactions(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    pipeline = compose(
        lambda txs: [transform_amount(tx) for tx in txs],
        lambda txs: [upper_case_category(tx) for tx in txs],
        validate_pipeline
    )

    processed = pipeline(transactions)

    income = filter_positive_transactions(processed)
    expenses = filter_negative_transactions(processed)

    return {
        'income': income,
        'expenses': expenses,
        'processed_transactions': processed,
        'total_income': sum(tx['amount'] for tx in income),
        'total_expenses': sum(tx['amount'] for tx in expenses)
    }

if __name__ == "__main__":
    transactions = [
        {'id': 1, 'amount': 100.0, 'currency': 'USD', 'timestamp': '2022-01-01', 'category': 'salary'},
        {'id': 2, 'amount': -50.0, 'currency': 'USD', 'timestamp': '2022-01-02', 'category': 'groceries'},
        {'id': 3, 'amount': 'invalid', 'currency': 'USD', 'timestamp': '2022-01-03', 'category': 'entertainment'},
        {'id': 4, 'amount': 200.0, 'currency': 'USD', 'timestamp': '2022-01-04', 'category': 'freelance'},
    ]

    try:
        result = process_transactions(transactions)
        print("Processed Result:", result)
    except Exception as e:
        print("Error:", e)