import pandas as pd

class StudentTracker:
    """Academic Performance Management System using Pandas."""

    def __init__(self):
        """Initialize an empty DataFrame with student performance records."""
        self.data = pd.DataFrame(columns=['StudentName', 'Score', 'Subject'])

    def record_grade(self, name: str, score: float, subject: str) -> None:
        """
        Add a new student performance record to the DataFrame.
        
        Parameters:
            name (str): Student's name
            score (float): Score obtained
            subject (str): Subject name
        
        Returns:
            None
        """
        new_record = pd.DataFrame({
            'StudentName': [name],
            'Score': [score],
            'Subject': [subject]
        })
        self.data = pd.concat([self.data, new_record], ignore_index=True)

    def get_subject_avg(self, subject: str) -> float:
        """
        Calculate the average score for a specific subject.
        
        Parameters:
            subject (str): Subject name
        
        Returns:
            float: Average score for the subject, or 0.0 if subject not found
        """
        subject_data = self.data[self.data['Subject'] == subject]
        if subject_data.empty:
            return 0.0
        return subject_data['Score'].mean()

    def get_top_scorers(self, threshold: float) -> list:
        """
        Get list of unique student names with scores above threshold.
        
        Parameters:
            threshold (float): Minimum score to qualify
        
        Returns:
            list: Unique student names with scores > threshold, or empty list
        """
        top_students = self.data[self.data['Score'] > threshold]
        return list(top_students['StudentName'].unique())

    def get_summary_stats(self) -> dict:
        """
        Get summary statistics about the records.
        
        Returns:
            dict: Contains 'total_records' (int) and 'unique_students' (int)
        """
        return {
            'total_records': len(self.data),
            'unique_students': self.data['StudentName'].nunique()
        }
