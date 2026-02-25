# student_workspace/solution.py

import pandas as pd
import numpy as np

class InventoryTrends:
    """
    Store Inventory Trends Analysis using Pandas.
    Analyzes product inventory data with efficient DataFrame operations.
    """
    
    def __init__(self):
        """Initialize the InventoryTrends with an empty DataFrame."""
        self.df = None
    
    def load_inventory(self, file_path: str):
        """
        Load the CSV file into a Pandas DataFrame.
        
        Parameters:
            file_path (str): Path to the CSV file containing inventory data
        """
        self.df = pd.read_csv(file_path)
    
    def calculate_valuation(self) -> float:
        """
        Calculate total product valuation.
        Creates a 'Valuation' column (StockLevel * UnitCost) and returns the sum.
        
        Returns:
            float: Total valuation (sum of all product valuations)
        """
        if self.df is None or self.df.empty:
            return 0.0
        
        # Create Valuation column
        self.df['Valuation'] = self.df['StockLevel'] * self.df['UnitCost']
        
        # Return total valuation
        return float(self.df['Valuation'].sum())
    
    def category_mean_stock(self) -> dict:
        """
        Calculate mean stock level for each product category.
        
        Returns:
            dict: Dictionary with Category as key and mean StockLevel as value
        """
        if self.df is None or self.df.empty:
            return {}
        
        mean_by_category = self.df.groupby("Category")["StockLevel"].mean().round(2).to_dict()
        return mean_by_category
    
    def get_reorder_list(self, stock_limit: int) -> list:
        """
        Get list of products with stock level below a threshold.
        
        Parameters:
            stock_limit (int): Stock level threshold - return ProductIDs where StockLevel < stock_limit
        
        Returns:
            list: Sorted list of ProductID strings with low stock
        """
        if self.df is None or self.df.empty:
            return []
        
        reorder_items = self.df[self.df["StockLevel"] < stock_limit]["ProductID"].tolist()
        return sorted(reorder_items)
