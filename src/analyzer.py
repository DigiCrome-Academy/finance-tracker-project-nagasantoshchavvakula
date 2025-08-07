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
    
#-------------------------- Statistical Analysis ---------------------------------
    def correlation_matrix(self,categories):
        """        Calculate the correlation matrix for multiple categories of data.
        :param categories: A dictionary where keys are category names and values are lists of numerical data
        :return: A correlation matrix as a NumPy array.

        """
        data_matrix = np.array(list(categories.values()))
        return np.corrcoef(data_matrix) 
    
    def calculate_percentiles(self):
        """Calculate various percentiles of the data.
        :return: A dictionary with 25th, 50th, 75th, 90th, and 95th percentiles.

        """
        return {
            '25th_percentile': np.percentile(self.data, 25),
            '50th_percentile': np.percentile(self.data, 50),
            '75th_percentile': np.percentile(self.data, 75),
            '90th_percentile': np.percentile(self.data, 90),
            '95th_percentile': np.percentile(self.data, 95)
        }
    
    def detect_outliers(self):
        """Detect outliers in the data using the IQR method.
        :return: A list of outliers.
        """
        q1 = np.percentile(self.data, 25)
        q3 = np.percentile(self.data, 75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        return [x for x in self.data if x < lower_bound or x > upper_bound]
    
    def time_series_analysis(self):
        """
        Perform time series analysis to detect seasonality and trends.
        :return: A tuple indicating whether seasonality and trend are detected. 

        """
        differenced = np.diff(self.data)
        seasonality_detected = np.std(differenced) > 0.1  # Example threshold for seasonality
        trend_detected = np.std(differenced) > 0.1  # Example threshold for trend
        return seasonality_detected, trend_detected
    
    def spending_recommendation(self,threshold_ratio=0.2):
        """
        Provide recommendations based on spending data.
        :param threshold_ratio: The ratio of spending above which a recommendation is made.
        :return: A list of recommendations based on spending patterns.
        :rtype: list
        :raises ValueError: If threshold_ratio is not between 0 and 1.

        """
        total = np.sum(self.data)
        threshold = total * threshold_ratio
        recommendations = []
        for i, value in enumerate(self.data):
            if value > threshold:
                recommendations.append(f"Consider reducing spending in category {i+1} which is {value} (above threshold of {threshold})")
        return recommendations if recommendations else ["No spending categories exceed the threshold."]
    
if __name__ == "__main__":
    # Create a FinancialAnalyzer instance with sample data
    data = [100, 120, 110, 130, 140, 150, 160, 170, 180, 190]
    analyzer = FinancialAnalyzer(data)

    # Calculate moving averages
    print("Moving Averages:", analyzer.calculate_moving_averages(3))

    # Spending recommendations
    print("Spending Recommendations:", analyzer.spending_recommendation(threshold_ratio=0.1))

    # Spending analysis
    print("Spending Analysis:", analyzer.analyze_spending_patterns())

    # Project future balance
    print("Future Balance:", analyzer.project_future_balance(6))

    # Portfolio metrics
    portfolio = {'stocks': 1000, 'bonds': 500, 'real_estate': 1500}
    print("Portfolio Metrics:", analyzer.calculate_portfolio_metrics(portfolio))

    # Budget allocation
    budget = 2000
    priorities = {'essentials': 0.5, 'savings': 0.3, 'entertainment': 0.2}
    print("Budget Allocation:", analyzer.optimize_budget_allocation(budget, priorities))

    # Correlation with another dataset
    other_data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    print("Correlation with other data:", analyzer.correlation_with(other_data))

    # Trend analysis
    print("Trend Analysis:", analyzer.trend_analysis())

    # Normalized data
    print("Normalized Data:", analyzer.normalize_data())

    # Correlation matrix between categories (as dictionary of lists)
    categories = {
        'food': [100, 120, 110],
        'transport': [130, 140, 150],
        'entertainment': [160, 170, 180]
    }
    print("Correlation Matrix:\n", analyzer.correlation_matrix(categories))

    # Percentiles
    print("Percentiles:", analyzer.calculate_percentiles())

    # Detect outliers
    print("Outliers:", analyzer.detect_outliers())

    # Standard deviation (extracted from analyze_spending_patterns)
    std_dev = analyzer.analyze_spending_patterns()['standard_deviation']
    print("Standard Deviation:", std_dev)

    # Time series analysis
    print("Time Series Analysis:", analyzer.time_series_analysis())





    


        