from datetime import datetime
from typing import Dict

class Transaction:
    """
    Represents a financial transaction with details such as date, amount, category, and merchant.
    
    Attributes:
        transaction_id(str): Unique identifier for the transaction.
        date(datetime object): Date of the transaction. 
        amount (float): The amount of the transaction.
        category (str): The category of the transaction (e.g., 'Food', 'Utilities').
        merchant (str): The merchant involved in the transaction.
        description (str): Optional description of the transaction.
        account_type (str): Type of account used for the transaction (e.g., 'Credit Card', 'Bank Account').
    """
    def __init__(self,transaction_id: str, date: datetime, amount: float, category: str, merchant: str, description: str = "", account_type: str = "Bank Account"):
        """
        Initializes a Transaction object with the provided details.
        Args:
            transaction_id (str): Unique identifier for the transaction.
            date (datetime): Date of the transaction.
            amount (float): Amount spent in the transaction.
            category (str): Category of the transaction.
            merchant (str): Merchant name involved in the transaction.
            description (str, optional): Description of the transaction. Defaults to "".
            account_type (str, optional): Type of account used for the transaction. Defaults to "Bank Account".
        """
        self.transaction_id = self._validate_required(transaction_id, "Transaction ID")
        self.date = self._validate_date(date)
        self.amount = self._validate_amount(amount, "Amount")
        self.category = self._validate_required(category, "Category")
        self.merchant = self._validate_required(merchant, "Merchant")
        self.description = description
        self.account_type = self._validate_required(account_type, "Account Type")

    def __str__(self)->str:
        return (f"Transaction ID: {self.transaction_id}, Date: {self.date.strftime('%Y-%m-%d')}, "
                f"Amount: ${self.amount:.2f}, Category: {self.category}, Merchant: {self.merchant}, "
                f"Description: {self.description}, Account Type: {self.account_type}")
    def __repr__(self)->str:
        return (f"Transaction(transaction_id={self.transaction_id!r}, date={self.date!r}, "
                f"amount={self.amount!r}, category={self.category!r}, merchant={self.merchant!r}, "
                f"description={self.description!r}, account_type={self.account_type!r})")
    
    def to_dict(self)->Dict:
        """
        Converts the transaction to a dictionary format.
        
        Returns:
            Dict[str, str]: Dictionary representation of the transaction.
        """
        return {
            "transaction_id": self.transaction_id,
            "date": self.date.strftime('%Y-%m-%d'),
            "amount": f"${self.amount:.2f}",
            "category": self.category,
            "merchant": self.merchant,
            "description": self.description,
            "account_type": self.account_type
        }
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'Transaction':
        """
        Creates a Transaction object from a dictionary.
        
        Args:
            data (Dict[str, str]): Dictionary containing transaction details.
        
        Returns:
            Transaction: A Transaction object created from the provided dictionary.
        """
        return cls(
            transaction_id=data.get("transaction_id", ""),
            date=datetime.strptime(data.get("date", ""), '%Y-%m-%d'),
            amount=float(data.get("amount", 0.0).replace("$", "").replace(",", "")),
            category=data.get("category", ""),
            merchant=data.get("merchant", ""),
            description=data.get("description", ""),
            account_type=data.get("account_type", "Bank Account")
        )
        
    @property
    def month(self) -> int:
        """
        Returns the month of the transaction date.
        
        Returns:
            int: Month of the transaction date.
        """
        return self.date.month
    @property
    def year(self) -> int:
        """
        Returns the year of the transaction date.
        
        Returns:
            int: Year of the transaction date.
        """
        return self.date.year
    #----------------------------------------------------------
    # Validation Utilities
    #----------------------------------------------------------
    def _validate_required(self, value:str, field_name: str)->str:
        """
        Validates that a required field is not empty.
        
        Args:
            value: Value to validate.
            field_name (str): Name of the field being validated.
        
        Returns:
            The validated value if it is not empty.
        
        Raises:
            ValueError: If the value is empty.
        """
        if not value or not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} cannot be empty.")
        return value
    
    def _validate_amount(self, amount: float, field_name: str) -> float:
        """
        Validates that the amount is a positive number.
        
        Args:
            amount (float): Amount to validate.
            field_name (str): Name of the field being validated.
        
        Returns:
            float: The validated amount if it is positive.
        
        Raises:
            ValueError: If the amount is not a positive number.
        """
        if not isinstance(amount, (int, float)):
            raise TypeError(f"{field_name} must be a number.")
        if amount == 0:
            raise ValueError(f"{field_name} cannot be zero.")
        return amount
    
    def _validate_date(self, date: datetime) -> datetime:
        """
        Validates that the date is a valid datetime object.
        
        Args:
            date (datetime): Date to validate.
        
        Returns:
            datetime: The validated date if it is a valid datetime object.
        
        Raises:
            TypeError: If the date is not a datetime object.
        """
        if not isinstance(date, datetime):
            raise TypeError("Date must be a datetime object.")
        return date
    #----------------------------------------------------------
    # Comparison Methods
    #----------------------------------------------------------
    def __lt__(self, other):
        """
        Less than comparison based on date.
        
        Args:
            other (Transaction): Another Transaction object to compare with.
        
        Returns:
            bool: True if this transaction's date is earlier than the other, False otherwise.
        """
        return self.date < other.date
    def __eq__(self, other):
        """
        Equality comparison based on date.
        Args:
            other (Transaction): Another Transaction object to compare with.
        Returns:
            bool: True if this transaction's date is the same as the other, False otherwise.
        """
        return self.date == other.date
    def __gt__(self, other):
        """
        Greater than comparison based on date.
        Args:
            other (Transaction): Another Transaction object to compare with.
        Returns:
            bool: True if this transaction's date is later than the other, False otherwise.
        """
        return self.date > other.date
    def __le__(self, other):
        """
        Less than or equal to comparison based on date.
        
        Args:
            other (Transaction): Another Transaction object to compare with.
        
        Returns:
            bool: True if this transaction's date is earlier than or the same as the other, False otherwise.
        """
        return self.date <= other.date
    def __ge__(self, other):
        """
        Greater than or equal to comparison based on date.
        
        Args:
            other (Transaction): Another Transaction object to compare with.
        
        Returns:
            bool: True if this transaction's date is later than or the same as the other, False otherwise.
        """
        return self.date >= other.date
    def __ne__(self, other):
        """
        Not equal comparison based on date.
        
        Args:
            other (Transaction): Another Transaction object to compare with.
        
        Returns:
            bool: True if this transaction's date is not the same as the other, False otherwise.
        """
        return self.date != other.date
    def __hash__(self):
        """
        Returns a hash value for the transaction based on its transaction ID.
        
        Returns:
            int: Hash value of the transaction ID.
        """
        return hash(self.transaction_id)

if __name__ == "__main__":
    print("=== Running Transaction Tests ===")
    from datetime import datetime

    # 1. Valid transaction test
    try:
        txn1 = Transaction("TX001", datetime(2025, 8, 3), 200.0, "Food", "McDonalds", "Lunch", "Bank Account")
        print("Valid transaction created successfully:")
        print(txn1)
        print("Dict format:", txn1.to_dict())
    except Exception as e:
        print("Failed to create valid transaction:", e)

    # 2. Zero amount test
    try:
        txn2 = Transaction("TX002", datetime(2025, 8, 3), 0.0, "Bills", "Electric Co.")
    except ValueError as e:
        print("Correctly caught zero amount error:", e)

    # 3. Empty transaction_id test
    try:
        txn3 = Transaction("", datetime(2025, 8, 3), 100.0, "Rent", "Landlord")
    except ValueError as e:
        print("Correctly caught empty transaction_id error:", e)

    # 4. Test from_dict
    txn_dict = {
        "transaction_id": "TX004",
        "date": "2025-08-04",
        "amount": "$150.00",
        "category": "Shopping",
        "merchant": "Amazon",
        "description": "Books",
        "account_type": "Bank Account"
    }
    txn4 = Transaction.from_dict(txn_dict)
    print("Transaction created from dict:")
    print(txn4)

    # 5. Comparison tests
    txn5 = Transaction("TX005", datetime(2025, 7, 1), 50.0, "Transport", "Uber")
    txn6 = Transaction("TX006", datetime(2025, 8, 1), 75.0, "Transport", "Lyft")
    print("txn5 < txn6:", txn5 < txn6)
    print("txn5 == txn6:", txn5 == txn6)
    print("txn6 > txn5:", txn6 > txn5)

    print("\n=== Transaction Tests Completed ===")
