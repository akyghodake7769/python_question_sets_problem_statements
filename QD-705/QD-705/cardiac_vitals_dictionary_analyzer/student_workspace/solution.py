class HealthMonitor:
    """Health Monitoring System using Python Dictionaries."""
    
    def __init__(self):
        """Initialize with records set to None."""
        pass
    
    def read_data(self, file_path: str):
        """Load CSV into self.records dictionary."""
        pass
    
    def clean_records(self) -> int:
        """Drop all rows where 'HeartRate' is None and return count of dropped rows."""
        pass
    
    def find_highest_rate(self) -> int:
        """Return maximum heart rate."""
        pass
    
    def patient_averages(self) -> dict:
        """Return dict of {PatientID: mean_heart_rate} rounded to 2 decimal places."""
        pass
    
    def high_risk(self, threshold: int) -> list:
        """Return sorted list of unique PatientIDs above threshold."""
        pass
    
    def count_high_risk(self, threshold: int) -> int:
        """Return count of high-risk patients."""
        pass
