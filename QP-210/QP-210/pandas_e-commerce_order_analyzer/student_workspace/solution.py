"""
QP-210: E-Commerce Order Analyzer
"""

import pandas as pd


class OrderAnalyzer:
    """
    Analyzes e-commerce order data using Pandas DataFrame.
    Performs calculations such as revenue analysis, category breakdown, and filtering.
    """
    
    def __init__(self):
        """
        Initialize the OrderAnalyzer with an empty DataFrame.
        
        Attributes:
            self.df (pd.DataFrame or None): Will store the loaded order data
        """
        self.df = None
    
    def load_data(self, file_path: str):
        """
        Load order data from a CSV file into a Pandas DataFrame.
        
        Parameters:
            file_path (str): Path to the CSV file containing order data
        
        Expected CSV columns: OrderID, Category, Price, Quantity
        """
        self.df = pd.read_csv(file_path)
    
    def calculate_revenue(self) -> float:
        """
        Calculate the total revenue from all orders.
        
        Creates a 'Revenue' column (Price × Quantity) and returns the sum.
        
        Returns:
            float: Total revenue from all orders
        """
        if self.df is None or len(self.df) == 0:
            return 0.0
        
        self.df['Revenue'] = self.df['Price'] * self.df['Quantity']
        return self.df['Revenue'].sum()
    
    def category_quantity(self) -> dict:
        """
        Group orders by category and sum the quantities.
        
        Returns:
            dict: Dictionary mapping category names to total quantities
                  Format: {'Category1': total_qty, 'Category2': total_qty, ...}
        """
        if self.df is None or len(self.df) == 0:
            return {}
        
        category_sums = self.df.groupby('Category')['Quantity'].sum()
        return category_sums.to_dict()
    
    def filter_orders(self, min_rev: float) -> list:
        """
        Filter orders by minimum revenue threshold.
        
        Parameters:
            min_rev (float): Minimum revenue threshold for filtering
        
        Returns:
            list: List of OrderIDs where Revenue > min_rev
                  Returns empty list if no orders match criteria or DataFrame is empty
        """
        if self.df is None or len(self.df) == 0:
            return []
        
        # Ensure Revenue column exists
        if 'Revenue' not in self.df.columns:
            self.df['Revenue'] = self.df['Price'] * self.df['Quantity']
        
        filtered = self.df[self.df['Revenue'] > min_rev]
        return filtered['OrderID'].tolist()
