import csv

class HealthMonitor:
    """
    Health Monitoring System using Python Lists.
    Manages patient health data with list-of-lists operations.
    """
    
    def __init__(self):
        """Initialize with records set to None."""
        self.records = None
    
    def read_data(self, file_path: str):
        """Load CSV into self.records list of lists."""
        self.records = []
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            try:
                header = next(reader)
            except StopIteration:
                return
            for row in reader:
                if len(row) < 3:
                    continue
                patient_id, day, heart_rate = row[0], row[1], row[2]
                hr_val = None
                if heart_rate and heart_rate.strip():
                    try:
                        hr_val = int(heart_rate.strip())
                    except ValueError:
                        hr_val = None
                self.records.append([patient_id, day, hr_val])
    
    def clean_records(self) -> int:
        """Drop all rows where 'HeartRate' (index 2) is None."""
        if self.records is None:
            return 0
        initial_count = len(self.records)
        self.records = [r for r in self.records if r[2] is not None]
        return initial_count - len(self.records)
    
    def find_highest_rate(self) -> int:
        """Return maximum heart rate."""
        if self.records is None or not self.records:
            return 0
        rates = [r[2] for r in self.records if r[2] is not None]
        return max(rates) if rates else 0
    
    def patient_averages(self) -> dict:
        """Return dict of {PatientID: mean_heart_rate} rounded to 2 decimal places."""
        if self.records is None or not self.records:
            return {}
        groups = {}
        for r in self.records:
            if r[2] is not None:
                pid = r[0]
                groups.setdefault(pid, []).append(r[2])
        
        averages = {}
        for pid, rates in groups.items():
            averages[pid] = round(sum(rates) / len(rates), 2)
        return averages
    
    def high_risk(self, threshold: int) -> list:
        """Return sorted list of unique PatientIDs above threshold."""
        if self.records is None or not self.records:
            return []
        high_risk_pts = set()
        for r in self.records:
            if r[2] is not None and r[2] > threshold:
                high_risk_pts.add(r[0])
        return sorted(list(high_risk_pts))
    
    def count_high_risk(self, threshold: int) -> int:
        """Return count of high-risk patients."""
        return len(self.high_risk(threshold))
