import pandas as pd

class PerformanceManager:
    """
    Data Controller responsible for loading and merging academic datasets.
    """
    def __init__(self):
        # TODO: Initialize df_info and df_grades as None
        self.df_info = None
        self.df_grades = None

    def load_records(self, info_path: str, grades_path: str):
        """
        Reads CSV files into self.df_info and self.df_grades.
        """
        # TODO: Load CSVs using pandas
        pass

    def get_merged_data(self) -> pd.DataFrame:
        """
        Performs an inner join on 'Student_ID'.
        """
        # TODO: Merge df_info and df_grades
        pass

class AcademicAnalyst:
    """
    Logic Processor responsible for computing academic metrics.
    """
    def get_subject_averages(self, df: pd.DataFrame) -> dict:
        """
        Returns a dictionary of mean marks for each subject.
        """
        # TODO: Group by Subject and calculate mean of Marks
        pass

    def calculate_cgpa(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates CGPA: (Marks * Credits) / Total Credits for each student.
        """
        # TODO: Perform multi-column math and return DataFrame with 'CGPA' column
        pass

    def identify_anomalies(self, df: pd.DataFrame) -> list:
        """
        Identifies students where (Max Marks - Min Marks) > 20.
        """
        # TODO: Group by student and check deviation
        pass

    def find_top_students(self, df: pd.DataFrame, threshold: float) -> list:
        """
        Returns names of students with CGPA >= threshold.
        """
        # TODO: Filter by threshold
        pass

    def subject_topper(self, df: pd.DataFrame, subject: str) -> str:
        """
        Returns the topper for a given subject in format: "Topper: [Name] ([Marks])"
        """
        # TODO: Identify max value row for the subject
        pass
