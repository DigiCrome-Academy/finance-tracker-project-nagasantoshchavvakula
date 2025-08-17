from datetime import datetime
from typing import Dict

class InvestmentPortfolio :

    class Holding :
        """        
        Represents a single holding in the investment portfolio.
        Args:
            symbol (str): The stock symbol of the holding.
            shares (float): The number of shares held.
            purchase_price (float): The price at which the shares were purchased.
            current_price (float): The current market price of the shares.
            purchase_date (datetime): The date when the shares were purchased.
        """

        def __init__(self,symbol:str,shares:float,purchase_price:float,current_price:float,purchase_date:datetime):
            self.symbol = self._validate_required(symbol, "Symbol")
            self.shares=self._validate_positive(shares, "Shares")
            self.purchase_price=self._validate_positive(purchase_price, "Purchase Price")
            self.current_price=self._validate_positive(current_price, "Current Price")
            self.purchase_date=purchase_date

        def _validate_required(self, value, field_name):
            if not value:
                raise ValueError(f"{field_name} is required.")
            return value
        def _validate_positive(self, value, field_name):
            if value < 0:
                raise ValueError(f"{field_name} must be a positive integer.")
            return value
        
    def __init__(self,portfolio_name:str,holdings:Dict[str, "InvestmentPortfolio.Holding"]=None,cash_balance:float=0.0):
        """
        Initializes the investment portfolio.
        Args:
            portfolio_name (str): The name of the portfolio.
            holdings (Dict[str, Holding]): A dictionary of holdings in the portfolio.
            cash_balance (float): The cash balance available in the portfolio.
        """
        self.portfolio_name = self._validate_required(portfolio_name, "Portfolio Name")
        self.holdings = holdings if holdings is not None else {}
        self.cash_balance = self._validate_positive(cash_balance, "Cash Balance")

    def _validate_required(self, value, field_name):
        if not value:
            raise ValueError(f"{field_name} is required.")
        return value
    def _validate_positive(self, value, field_name):
        if value < 0:
            raise ValueError(f"{field_name} must be a positive number.")
        return value
    
    def add_holding(self,symbol:str,shares:float,purchase_price:float,current_price:float, purchase_date:datetime):
        """
        Adds a new holding to the portfolio.
        Args:
        symbol (str): The stock symbol of the holding.
        shares (float): The number of shares held.
        purchase_price (float): The price at which the shares were purchased.
        current_price (float): The current market price of the shares.
        purchase_date (datetime): The date when the shares were purchased.

        """
        total_cost=shares*purchase_price
        if total_cost > self.cash_balance:
            raise ValueError("Insufficient cash balance to add the holding.")
        
        holding = self.Holding(symbol,shares,purchase_price,current_price,purchase_date)
        self.holdings[symbol] = holding
        self.cash_balance -= total_cost

    def remove_holding(self,symbol:str):
        """
        Removes a holding from the portfolio.
        Args:
        symbol (str): The stock symbol of the holding to be removed.

        """
        if symbol in self.holdings:
            holding = self.holdings.pop(symbol)
            self.cash_balance += holding.shares * holding.current_price
        else:
            raise ValueError(f"Holding with symbol {symbol} does not exist in the portfolio.")
        
    def update_prices(self,price:Dict[str,float]):
        """
        Updates the current prices of all holdings in the portfolio.
        Args:
        price (Dict[str,float]): A dictionary of stock symbols and their current prices.

        """
        for symbol,price in price.items():
            if symbol in self.holdings:
                self.holdings[symbol].current_price = self.holdings[symbol]._validate_positive(price, "Updated Price")
            else:
                raise ValueError(f"Holding with symbol {symbol} does not exist in the portfolio.")
            
    def calculate_total_value(self)->float:
        """
        Calculates the total value of the portfolio.
        Returns:
        float: The total value of the portfolio.

        """
        total_value=self.cash_balance
        for holding in self.holdings.values():
            total_value += holding.shares * holding.current_price
        return total_value
    
    def get_asset_allocation(self)->Dict[str,float]:
        """
        Calculates the asset allocation of the portfolio.
        Returns:
        Dict[str,float]: A dictionary of the asset allocation of the portfolio.

        """
        total_value=self.calculate_total_value()
        if total_value == 0:
            return {symbol: 0.0 for symbol in self.holdings}
        allocation = {}
        for symbol,holding in self.holdings.items():
            allocation[symbol] = round((holding.shares * holding.current_price / total_value)*100,2)
        return allocation
        
    #-----------------------Analytics Methods-----------------------------------
    def market_value(self) -> float:
        """
        Calculates the market value of the portfolio.
        Returns:
        float: The market value of the portfolio.

        """
        return self.calculate_total_value()
    
    def cost_basis(self) -> float:
        """
        Calculates the cost basis of the portfolio.
        Returns:
        float: The cost basis of the portfolio.

        """
        return sum(h.shares * h.purchase_price for h in self.holdings.values())
    
    def profit_loss(self) -> float:
        """
        Calculates the profit/loss of the portfolio.
        Returns:
        float: The profit/loss of the portfolio.

        """
        return self.market_value() - self.cost_basis()
    
    def return_percentage(self) -> float:
        """
        Calculates the return percentage of the portfolio.
        Returns:
        float: The return percentage of the portfolio.

        """
        return (self.profit_loss() / self.cost_basis()) * 100.0
    
    def summary(self) -> dict:
        """
        Returns a dictionary containing the portfolio's market value, cost basis, profit/loss, and return
        percentage.
        Returns:
        dict: A dictionary containing the portfolio's market value, cost basis, profit/loss, and return percentage.

        """
        return {
                "Portfolio Name": self.portfolio_name,
                "Total Value": self.calculate_total_value(),
                "Cash Balance": self.cash_balance,
                "Holdings": {
                    symbol: {
                        "Shares": h.shares,
                        "Purchase Price": h.purchase_price,
                        "Current Price": h.current_price,
                        "Purchase Date": h.purchase_date.strftime('%Y-%m-%d')
                    }
                    for symbol, h in self.holdings.items()
                },
                "Asset Allocation": self.get_asset_allocation(),
                "Market Value": self.market_value(),
                "Cost Basis": self.cost_basis(),
                "Profit/Loss": self.profit_loss(),
                "Return Percentage": self.return_percentage()
            }
    def get_summary(self) -> str:
        """
        Returns a string containing the portfolio's summary.
        Returns:
        str: A string containing the portfolio's summary.
        
        """
        summary = self.summary()
        return (
            f"Portfolio Name: {summary['Portfolio Name']}\n"
            f"Total Value: ${summary['Total Value']:.2f}\n"
            f"Cash Balance: ${summary['Cash Balance']:.2f}\n"
            f"Holdings: ${summary["Holdings"]}\n"
            f"Asset Allocation: {summary['Asset Allocation']}\n"
            f"Market Value: ${summary['Market Value']:.2f}\n"
            f"Cost Basis: ${summary['Cost Basis']:.2f}\n"
            f"Profit/Loss: ${summary['Profit/Loss']:.2f}\n"
            f"Return Percentage: {summary['Return Percentage']:.2f}%\n"
            )
 #----------------------Example Usage---------------------------------
if __name__ == "__main__":
    portfolio = InvestmentPortfolio("My Investment Portfolio", cash_balance=10000.0)
    portfolio.add_holding("AAPL", 10, 150.0, 160.0, datetime(2023, 1, 1))
    portfolio.add_holding("GOOGL", 2, 2500.0, 2800.0, datetime(2023, 2, 1))

    # Update current market prices
    portfolio.update_prices({"AAPL": 170.0, "GOOGL": 2900.0})

    print(portfolio.get_summary())

        






            