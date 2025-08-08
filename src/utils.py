# utils.py
import re
import time
import functools
import logging
from typing import Callable, Any, Dict, List, Union

#------------------------------------------
# Logging configuration
#------------------------------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

#------------------------------------------
# Decorators
#------------------------------------------
def log_execution(func: Callable) -> Callable:
    """Decorator to log the execution time of a function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"Executed {func.__name__} in {end_time - start_time:.4f} seconds")
        return result
    return wrapper

def time_execution(func: Callable) -> Callable:
    """Decorator to time the execution of a function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> float:
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        return end_time - start_time
    return wrapper

def handle_exceptions(func: Callable) -> Callable:
    """Decorator to handle exceptions and log them."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            raise
    return wrapper

#------------------------------------------
# Pure functions
#------------------------------------------
@log_execution
def clean_amount(amount: Union[str, float, int]) -> float:
    """Clean and convert an amount to a float."""
    if isinstance(amount, str):
        amount = re.sub(r'[^\d.-]', '', amount)
        return float(amount)
    elif isinstance(amount, (int, float)):
        return float(amount)
    else:
        raise ValueError(f"Invalid amount type: {type(amount)}")

@log_execution
def validate_transaction(transaction: Dict[str, Any]) -> bool:
    """Validate a transaction dictionary."""
    required_keys = {'id', 'amount', 'currency', 'timestamp'}
    if not all(key in transaction for key in required_keys):
        logger.error(f"Transaction missing required keys: {transaction}")
        return False
    if not isinstance(transaction['amount'], (int, float, str)):
        logger.error(f"Invalid amount type in transaction: {transaction['amount']}")
        return False
    return True

#------------------------------------------
# Higher order functions 
#------------------------------------------
def apply_to_transactions(transactions: List[Dict[str, Any]], func: Callable) -> List[Any]:
    """Apply a function to a list of valid transactions."""
    results = []
    for transaction in transactions:
        if validate_transaction(transaction):
            results.append(func(transaction))
        else:
            logger.warning(f"Skipping invalid transaction: {transaction}")
    return results

#------------------------------------------
# Default parameters
#------------------------------------------
def format_currency(amount: float, currency: str = 'USD', *args, **kwargs) -> str:
    """Format an amount as a currency string."""
    symbol = kwargs.get('symbol', '$')
    return f"{symbol}{amount:,.2f} {currency}"

#------------------------------------------
# Lambda functions
#------------------------------------------
filter_positive_transactions = lambda txs: [t for t in txs if t.get('amount', 0) > 0]
filter_negative_transactions = lambda txs: [t for t in txs if t.get('amount', 0) < 0]

#------------------------------------------
# Recursive functions
#------------------------------------------
def sum_transaction_amounts(transactions: List[Dict[str, Any]]) -> float:
    """Recursively sum transaction amounts."""
    if not transactions:
        return 0.0
    return transactions[0].get('amount', 0) + sum_transaction_amounts(transactions[1:])

def sum_nested_amounts(data: Union[List, Dict]) -> float:
    """Recursively sum amounts in nested structures."""
    if isinstance(data, list):
        return sum(sum_nested_amounts(item) for item in data)
    elif isinstance(data, dict):
        return sum_nested_amounts(list(data.values()))
    elif isinstance(data, (int, float)):
        return data
    return 0.0

if __name__ == "__main__":
    from utils import apply_to_transactions, format_currency, sum_transaction_amounts
    from data_pipeline import transform_amount

    transactions = [
        {'id': 1, 'amount': '100.50', 'currency': 'USD', 'timestamp': '2023-10-01', 'category': 'groceries'},
        {'id': 2, 'amount': '-20.00', 'currency': 'USD', 'timestamp': '2023-10-02', 'category': 'entertainment'},
        {'id': 3, 'amount': '300', 'currency': 'USD', 'timestamp': '2023-10-03', 'category': 'utilities'},
    ]

    cleaned = apply_to_transactions(transactions, transform_amount)
    print("Cleaned Transactions:", cleaned)

    total = sum_transaction_amounts(cleaned)
    print("Total Amount:", total)

    print("Formatted:", format_currency(total, symbol='$'))