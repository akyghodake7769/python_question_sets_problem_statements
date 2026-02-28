"""
QP-211: Store Sales Monitor

A Python class for analyzing retail transaction data using pandas.
The class can load sales data, calculate revenue, filter bulk orders,
and identify top-selling products.
"""

import pandas as pd
import os


class SalesMonitor:
    """Analyzes retail transaction data for sales monitoring and analytics."""
    
    def __init__(self):
        """Initialize the SalesMonitor with an empty DataFrame."""
        self.df = None
    
    def load_data(self, file_path: str):
        """
        Load sales data from mock_sales.csv.
        
        Args:
            file_path (str): Path to the CSV file containing sales records
        """
        self.df = pd.read_csv(file_path)
    
    def calculate_revenue(self):
        """
        Create a new 'Revenue' column calculated as (Qty * UnitPrice).
        """
        if self.df is None:
            return
        
        self.df['Revenue'] = self.df['Qty'] * self.df['UnitPrice']
    
    def get_total_by_region(self, region_name: str) -> float:
        """
        Calculate the total revenue for a specific region.
        
        Args:
            region_name (str): The region to filter by
        
        Returns:
            float: The total revenue for the region (0.0 if region not found)
        """
        if self.df is None or len(self.df) == 0:
            return 0.0
        
        region_data = self.df[self.df['Region'] == region_name]
        if len(region_data) == 0:
            return 0.0
        
        return region_data['Revenue'].sum()
    
    def filter_bulk_orders(self, min_qty: int) -> int:
        """
        Count the number of bulk orders (Qty >= min_qty).
        
        Args:
            min_qty (int): Minimum quantity threshold for bulk orders
        
        Returns:
            int: Count of orders meeting the bulk threshold
        """
        if self.df is None:
            return 0
        
        return len(self.df[self.df['Qty'] >= min_qty])
    
    def top_product_name(self) -> str:
        """
        Identify the product with the highest total quantity sold.
        
        Returns:
            str: The name of the top-selling product by quantity
        """
        if self.df is None or len(self.df) == 0:
            return ""
        
        product_qty = self.df.groupby('Product')['Qty'].sum()
        top_product = product_qty.idxmax()
        return top_product
