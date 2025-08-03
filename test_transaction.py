from src.transaction import Transaction
from datetime import datetime

txn = Transaction(
    transaction_id='TXN001', 
    date=datetime(2023, 10, 1),
    amount=100.0,
    description="Test transaction",
    category="Food",
    merchant="Supermarket",
    account_type="Bank Account"
)
print(txn)
print(txn.to_dict())
print(Transaction.from_dict(txn.to_dict()))
print(txn.month)
print(txn.year)