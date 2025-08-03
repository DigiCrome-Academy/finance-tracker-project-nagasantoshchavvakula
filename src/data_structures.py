from typing import List, Dict, Tuple, Set, Any


# 1. Use list to store transaction categories
def creating_category_list() -> List[str]:
    """Creates a list of default transaction categories.

    Returns:
        List[str]: List of default categories.
    """
    return ["Food", "Utilities", "Transport", "Entertainment", "Healthcare", "Investment"]


def adding_category(categories: List[str], new_category: str) -> None:
    """Adds a new category to the list if it's not already present.

    Args:
        categories (List[str]): Existing list of categories.
        new_category (str): Category to be added.
    """
    if new_category not in categories:
        categories.append(new_category)


def removing_category(categories: List[str], category: str) -> None:
    """Removes a category from the list if it exists.

    Args:
        categories (List[str]): List of existing categories.
        category (str): Category to remove.
    """
    if category in categories:
        categories.remove(category)


# 2. Use dictionary to create category-to-budget mapping
def creating_category_to_budget_mapping(categories: List[str], default_budget: float = 0.0) -> Dict[str, float]:
    """Creates a budget mapping for each category.

    Args:
        categories (List[str]): List of categories.
        default_budget (float, optional): Default budget for each category. Defaults to 0.0.

    Returns:
        Dict[str, float]: Dictionary mapping categories to budgets.
    """
    return {category: default_budget for category in categories}


def updating_budget(budget_map: Dict[str, float], category: str, amount: float) -> None:
    """Updates the budget for a specific category.

    Args:
        budget_map (Dict[str, float]): Existing budget mapping.
        category (str): Category to update.
        amount (float): New budget amount.
    """
    budget_map[category] = amount


# 3. Use tuples for immutable transaction records
def creating_transaction_record(date: str, amount: float, category: str, merchant: str) -> Tuple[str, float, str, str]:
    """Creates an immutable transaction record.

    Args:
        date (str): Date of the transaction.
        amount (float): Amount spent.
        category (str): Transaction category.
        merchant (str): Merchant name.

    Returns:
        Tuple[str, float, str, str]: A transaction record as a tuple.
    """
    return (date, amount, category, merchant)


# 4. Use sets for unique merchant names
def creating_unique_merchant_set() -> Set[str]:
    """Initializes an empty set to store merchant names.

    Returns:
        Set[str]: Empty set of merchants.
    """
    return set()


def adding_merchant(merchants: Set[str], merchant: str) -> None:
    """Adds a merchant to the set of unique merchants.

    Args:
        merchants (Set[str]): Set of existing merchants.
        merchant (str): New merchant to add.
    """
    merchants.add(merchant)


# 5. Use list of dictionaries for transaction history
def creating_transaction_history() -> List[Dict[str, Any]]:
    """Initializes an empty list for storing transaction history.

    Returns:
        List[Dict[str, Any]]: Empty list of transaction records.
    """
    return []


def adding_transaction(
    history: List[Dict[str, Any]],
    date: str,
    amount: float,
    category: str,
    merchant: str
) -> None:
    """Adds a new transaction to the history.

    Args:
        history (List[Dict[str, Any]]): List of past transactions.
        date (str): Transaction date.
        amount (float): Transaction amount.
        category (str): Category of the transaction.
        merchant (str): Merchant involved in the transaction.
    """
    transaction = {
        "date": date,
        "amount": amount,
        "category": category,
        "merchant": merchant
    }
    history.append(transaction)


# 6. Functions to manipulate data
def total_spent_by_category(history: List[Dict[str, Any]], category: str) -> float:
    """Calculates total amount spent in a specific category.

    Args:
        history (List[Dict[str, Any]]): Transaction history.
        category (str): Category to calculate total for.

    Returns:
        float: Total amount spent in the category.
    """
    return sum(t["amount"] for t in history if t["category"] == category)


def filtered_transactions_by_merchant(history: List[Dict[str, Any]], merchant: str) -> List[Dict[str, Any]]:
    """Filters transactions by merchant name.

    Args:
        history (List[Dict[str, Any]]): Transaction history.
        merchant (str): Merchant name to filter by.

    Returns:
        List[Dict[str, Any]]: List of transactions from the specified merchant.
    """
    return [t for t in history if t["merchant"].lower() == merchant.lower()]


def search_transactions_by_amount_range(
    history: List[Dict[str, Any]], min_amt: float, max_amt: float
) -> List[Dict[str, Any]]:
    """Searches for transactions within a specified amount range.

    Args:
        history (List[Dict[str, Any]]): Transaction history.
        min_amt (float): Minimum amount.
        max_amt (float): Maximum amount.

    Returns:
        List[Dict[str, Any]]: Transactions within the amount range.
    """
    return [t for t in history if min_amt <= t["amount"] <= max_amt]


def summarize_by_category(history: List[Dict[str, Any]]) -> Dict[str, float]:
    """Summarizes total spending by category.

    Args:
        history (List[Dict[str, Any]]): Transaction history.

    Returns:
        Dict[str, float]: Mapping of categories to total spending.
    """
    summary = {}
    for transaction in history:
        cat = transaction["category"]
        summary[cat] = summary.get(cat, 0.0) + transaction["amount"]
    return summary

if __name__ == "__main__":
    # Example usage of the functions
    categories = creating_category_list()
    print("Initial Categories:", categories)

    adding_category(categories, "Savings")
    print("After Adding Category:", categories)

    removing_category(categories, "Utilities")
    print("After Removing Category:", categories)

    budget_map = creating_category_to_budget_mapping(categories, 100.0)
    print("Initial Budget Mapping:", budget_map)

    updating_budget(budget_map, "Food", 150.0)
    print("Updated Budget Mapping:", budget_map)

    transaction = creating_transaction_record("2023-10-01", 50.0, "Food", "Supermarket")
    print("Transaction Record:", transaction)

    merchants = creating_unique_merchant_set()
    adding_merchant(merchants, "Supermarket")
    print("Unique Merchants:", merchants)

    history = creating_transaction_history()
    adding_transaction(history, "2023-10-01", 50.0, "Food", "Supermarket")
    print("Transaction History:", history)

    total_food_spent = total_spent_by_category(history, "Food")
    print("Total Spent on Food:", total_food_spent)

