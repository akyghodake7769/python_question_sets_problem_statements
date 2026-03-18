# student_workspace/solution.py
import pandas as pd
import numpy as np

class HealthMonitor:
    """
    Health Monitoring System using Pandas.
    Manages patient health data with efficient DataFrame operations.
    """
    
    def __init__(self):
        """Initialize the HealthMonitor with an empty DataFrame."""
        self.df = None
    
    def read_data(self, file_path: str):
        """Load the CSV file into a Pandas DataFrame."""
        self.df = pd.read_csv(file_path)
    
    def clean_records(self) -> int:
        """
        Drop all rows where 'HeartRate' is NaN.
        Returns:
            int: Number of rows removed.
        """
        # Hint: Use dropna() and return the count of removed rows.
        pass
    
    def find_highest_rate(self) -> int:
        """
        Find and return the maximum heart rate in the dataset.
        Returns:
            int: Peak heart rate value.
        """
        # Hint: Use the max() method on the HeartRate column.
        pass
    
    def patient_averages(self) -> dict:
        """
        Calculate mean 'HeartRate' for each 'PatientID'.
        Returns:
            dict: PatientID keys and mean heart rate values.
        """
        # Hint: Use groupby() and mean().
        pass
    
    def high_risk(self, threshold: int) -> list:
        """
        Return sorted list of unique PatientIDs above the threshold.
        """
        # Hint: Filter for HR > threshold and return sorted unique PatientIDs.
        pass
    
    def count_high_risk(self, threshold: int) -> int:
        """
        Count total unique patients with heart rate above threshold.
        """
        # Hint: Use high_risk() method to get the list and return its length.
        pass
