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
        """
        Load the CSV file into a Pandas DataFrame.
        
        Parameters:
            file_path (str): Path to the CSV file
        """
        self.df = pd.read_csv(file_path)
    
    def clean_records(self) -> int:
        """
        Drop all rows where 'HeartRate' is NaN.
        
        Returns:
            int: Number of rows removed (NaN records)
        """
        if self.df is None:
            return 0
        
        initial_count = len(self.df)
        self.df = self.df.dropna(subset=['HeartRate'])
        removed_count = initial_count - len(self.df)
        return removed_count
    
    def patient_averages(self) -> dict:
        """
        Calculate mean 'HeartRate' for each 'PatientID'.
        
        Returns:
            dict: Dictionary with PatientID as key and mean heart rate as value
        """
        if self.df is None or self.df.empty:
            return {}
        
        avg_by_patient = self.df.groupby("PatientID")["HeartRate"].mean().round(2).to_dict()
        return avg_by_patient
    
    def high_risk(self, threshold: int) -> list:
        """
        Return list of unique PatientIDs with at least one heart rate above threshold.
        
        Parameters:
            threshold (int): Heart rate threshold value
        
        Returns:
            list: Sorted list of unique PatientIDs with at least one reading above threshold
        """
        if self.df is None or self.df.empty:
            return []
        
        high_risk_patients = self.df[self.df["HeartRate"] > threshold]["PatientID"].unique().tolist()
        return sorted(high_risk_patients)
