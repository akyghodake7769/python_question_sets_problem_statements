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
        """ YOUR CODE HERE """
    
    def read_data(self, file_path: str):
        """
        Load the CSV file into a Pandas DataFrame.
        
        Parameters:
            file_path (str): Path to the CSV file
        """
        """ YOUR CODE HERE """
    
    def clean_records(self) -> int:
        """
        Drop all rows where 'HeartRate' is NaN.
        
        Returns:
            int: Number of rows removed (NaN records)
        """
        """ YOUR CODE HERE """
    
    def patient_averages(self) -> dict:
        """
        Calculate mean 'HeartRate' for each 'PatientID'.
        
        Returns:
            dict: Dictionary with PatientID as key and mean heart rate as value
        """
        """ YOUR CODE HERE """
    
    def high_risk(self, threshold: int) -> list:
        """
        Return list of unique PatientIDs with at least one heart rate above threshold.
        
        Parameters:
            threshold (int): Heart rate threshold value
        
        Returns:
            list: Sorted list of unique PatientIDs with at least one reading above threshold
        """
        """ YOUR CODE HERE """

