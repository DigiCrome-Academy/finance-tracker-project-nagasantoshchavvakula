from typing import List, Dict
from datetime import datetime
from transaction import Transaction


class Account:
    """
    Represents a bank account that holds transactions and tracks the balance.
    Args:
        account_name (str): The name of the account.
        account_type (str): The type of the account (e.g., "Bank Account", "Checking Account").
    """
    def __init__(self, account_name: str, account_type: str = "Bank Account"):
        self.account_name = self._validate_required(account_name, "Account Name")
        self.account_type = self._validate_required(account_type, "Account Type")
        self.balance = 0.0
        self.transaction_list: List[Transaction] = []

    def add_transaction(self, transaction: Transaction) -> None:
        """
        Adds a transaction to the account and updates the balance.
        """
        if not isinstance(transaction, Transaction):
            raise TypeError("Only Transaction objects can be added.")
        self.transaction_list.append(transaction)
        self.balance += transaction.amount

    def remove_transaction(self, transaction_id: str) -> None:
        """
        Removes a transaction by ID and updates the balance.
        """
        for i, txn in enumerate(self.transaction_list):
            if txn.transaction_id == transaction_id:
                self.balance -= txn.amount
                del self.transaction_list[i]
                return
        raise ValueError(f"Transaction with ID {transaction_id} not found.")

    def get_balance(self) -> float:
        """
        Returns the current balance.
        """
        return self.balance

    def get_transactions_by_category(self, category: str) -> List[Transaction]:
        """
        Returns a list of transactions in the specified category.
        """
        return [txn for txn in self.transaction_list if txn.category.lower() == category.lower()]

    def get_monthly_summary(self, month: int, year: int) -> Dict[str, float]:
        """
        Returns summary of spending per category for a given month and year.
        """
        summary: Dict[str, float] = {}
        for txn in self.transaction_list:
            if txn.month == month and txn.year == year:
                summary[txn.category] = summary.get(txn.category, 0.0) + txn.amount
        return summary

    def _validate_required(self, value: str, field_name: str) -> str:
        if not value or not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} cannot be empty.")
        return value

    def __str__(self) -> str:
        return f"{self.account_type} - {self.account_name}: Balance ${self.balance:.2f}"

    def __repr__(self) -> str:
        return f"Account(account_name={self.account_name!r}, account_type={self.account_type!r}, balance={self.balance!r})"

class CheckingAccount(Account):
    """
    Represents a checking account with optional overdraft protection.
    
    """
    def __init__(self, account_name: str, overdraft_limit: float = 0.0):
        super().__init__(account_name, account_type="Checking Account")
        self.overdraft_limit = overdraft_limit

    def add_transaction(self, transaction: Transaction) -> None:
        """
        Adds a transaction with overdraft protection.
        """
        if self.balance + transaction.amount < -self.overdraft_limit:
            raise ValueError("Transaction exceeds overdraft limit.")
        super().add_transaction(transaction)

    def __str__(self):
        return f"{self.account_type} - {self.account_name}: Balance ${self.balance:.2f}, Overdraft Limit: ${self.overdraft_limit:.2f}"


class SavingsAccount(Account):
    """
    Represents a savings account with a withdrawal limit.
    """
    def __init__(self, account_name: str, withdrawal_limit: int = 6):
        super().__init__(account_name, account_type="Savings Account")
        self.withdrawal_limit = withdrawal_limit
        self.withdrawals_this_month = 0

    def add_transaction(self, transaction: Transaction) -> None:
        """
        Adds a transaction, ensuring it doesn’t exceed the monthly withdrawal limit.
        """
        if transaction.amount < 0:  # Assuming positive means withdrawal
            if self.withdrawals_this_month >= self.withdrawal_limit:
                raise ValueError("Monthly withdrawal limit exceeded.")
            self.withdrawals_this_month += 1
        super().add_transaction(transaction)

    def reset_withdrawals(self) -> None:
        """
        Resets withdrawal count (to be called monthly).
        """
        self.withdrawals_this_month = 0

    def __str__(self):
        return f"{self.account_type} - {self.account_name}: Balance ${self.balance:.2f}, Withdrawals this month: {self.withdrawals_this_month}/{self.withdrawal_limit}"
    
if __name__ == "__main__":
    from datetime import datetime

    print("=== Testing CheckingAccount ===")
    txn1 = Transaction("T001", datetime(2025, 8, 2), 100.0, "Food", "PizzaHut")
    txn2 = Transaction("T002", datetime(2025, 8, 3), 50.0, "Transport", "Uber")

    acct = CheckingAccount("Daily Expenses", overdraft_limit=200)
    acct.add_transaction(txn1)
    acct.add_transaction(txn2)

    print(acct)
    print(acct.get_transactions_by_category("Food"))
    print(acct.get_monthly_summary(8, 2025))

    print("\n=== Testing SavingsAccount ===")
    saving_txn1 = Transaction("S001", datetime(2025, 8, 4), -200.0, "Emergency", "ATM")
    saving_txn2 = Transaction("S002", datetime(2025, 8, 5), -100.0, "Education", "Online Transfer")

    savings = SavingsAccount("Emergency Fund", withdrawal_limit=1)
    savings.add_transaction(Transaction("S000", datetime(2025, 8, 1), 1000.0, "Initial Deposit", "Bank"))
    try:
        savings.add_transaction(saving_txn1)  # 1st withdrawal
        savings.add_transaction(saving_txn2)  # 2nd withdrawal 
    except ValueError as ve:
        print("Error during savings transaction:", ve)

    print(savings)
    print(savings.get_transactions_by_category("Emergency"))
    print(savings.get_monthly_summary(8, 2025))
