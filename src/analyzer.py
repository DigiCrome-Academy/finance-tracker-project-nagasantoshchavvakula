import numpy as np

class FinancialAnalyzer:
    """
    A class for analyzing financial data and providing insights.
    :param data: A list or array of numerical values representing financial data.
    
    """
    def __init__(self, data):
        self.data = data

    def calculate_moving_averages(self, window_size):
        """
        Calculate the moving average of the data.
        
        :param window_size: The size of the moving window.
        :return: A list containing the moving averages.
        """
        if window_size <= 0:
            raise ValueError("Window size must be a positive integer.")
        
        return np.convolve(self.data, np.ones(window_size)/window_size, mode='valid')
    
    def analyze_spending_patterns(self):
        """
        Analyze spending patterns in the data.
        
        :return: A dictionary with average spending and total spending.
        """
        # total_spending = np.sum(self.data)
        # average_spending = np.mean(self.data)
        # standard_deviation = np.std(self.data)
        
        return {
            'total_spending': np.sum(self.data),
            'average_spending': np.mean(self.data),
            'standard_deviation': np.std(self.data),
            'maximum_spending': np.max(self.data),
            'minimum_spending': np.min(self.data)
        }
    
    def project_future_balance(self, months_ahead):
        """
        Project future balance based on current data.
        
        :param months_ahead: Number of months to project into the future.
        :return: Projected balance after the specified number of months.
        """
        if months_ahead < 0:
            raise ValueError("Months ahead must be a non-negative integer.")
        
        monthly_average = np.mean(self.data)
        return np.sum(self.data) + (monthly_average * months_ahead)
    
    def calculate_portfolio_metrics(self, portfolio):
        """
        Calculate metrics for a given portfolio.
        
        :param portfolio: A dictionary with asset names as keys and their values as amounts.
        :return: A dictionary with total value and average value per asset.
        """
        # total_value = sum(portfolio.values())
        # average_value = total_value / len(portfolio) if portfolio else 0
        values = np.array(list(portfolio.values()))
        return {
            'total_value': np.sum(values),
            'average_value': np.mean(values),
            'standard_deviation_per_asset': np.std(values),
            'maximum_value_per_asset': np.max(values),
        }
    
    def optimize_budget_allocation(self, budget, priorities):
        """
        Optimize budget allocation based on priorities.
        
        :param budget: Total budget available.
        :param priorities: A dictionary with categories as keys and their priority as values.
        :return: A dictionary with allocated budget per category.
        """
        priorities = {k: v for k, v in priorities.items() if v > 0} # Filter out non-positive priorities 
        total_priority = np.sum(list(priorities.values()))
        allocation = {category: (budget * (priority / total_priority)) for category, priority in priorities.items()}
        
        return allocation
    
    def correlation_with(self, other_data):
        """
        Calculate the correlation between the current data and another dataset.
        
        :param other_data: A list or array of numerical values to compare against.
        :return: Correlation coefficient between the two datasets.
        """
        other_data = np.array(other_data)
        if len(self.data) != len(other_data):
            raise ValueError("Both datasets must have the same length.")
        
        return np.corrcoef(self.data, other_data)[0, 1]
    
    def trend_analysis(self):
        """
        Perform trend analysis on the data.
        
        :return: A dictionary with trend direction and strength.
        """
        x = np.arange(len(self.data))
        y = np.array(self.data)
        
        # Perform linear regression
        A = np.vstack([x, np.ones(len(x))]).T
        m, c = np.linalg.lstsq(A, y, rcond=None)[0]
        
        trend_direction = 'upward' if m > 0 else 'downward' if m < 0 else 'stable'
        trend_strength = abs(m)
        
        return {
            'trend_direction': trend_direction,
            'trend_strength': trend_strength
        }
    
    def normalize_data(self):
        """
        Normalize the data to a 0-1 range.
        
        :return: A list containing the normalized data.
        """
        min_val = np.min(self.data)
        max_val = np.max(self.data)
        
        if max_val - min_val == 0:
            return [0.0] * len(self.data)
        return (self.data - min_val) / (max_val - min_val)
    
if __name__ == "__main__":
    # Example usage
    """
    Example usage of the FinancialAnalyzer class.
    """
    data = [100, 150, 200, 250, 300, 350, 400]
    analyzer = FinancialAnalyzer(data)
    
    print("Moving Averages:", analyzer.calculate_moving_averages(window_size=3))
    print("Spending Patterns:", analyzer.analyze_spending_patterns())
    print("Projected Future Balance (6 months):", analyzer.project_future_balance(months_ahead=6))
    
    portfolio = {'stocks': 5000, 'bonds': 3000, 'real_estate': 2000}
    print("Portfolio Metrics:", analyzer.calculate_portfolio_metrics(portfolio))
    
    budget = 1000
    priorities = {'rent': 5, 'food': 3, 'entertainment': 2}
    print("Budget Allocation:", analyzer.optimize_budget_allocation(budget, priorities))
    
    other_data = [110, 160, 210, 260, 310, 360, 410]
    print("Correlation with other data:", analyzer.correlation_with(other_data))
    
    print("Trend Analysis:", analyzer.trend_analysis())
    print("Normalized Data:", analyzer.normalize_data())

    


        