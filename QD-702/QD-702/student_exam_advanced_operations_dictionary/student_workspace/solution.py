class StudentResultManager:
    """Manage student exam results and perform analysis operations."""

    def __init__(self):
        """Initialize student results dictionary with sample data."""
        self.students = {
            "S001": {"name": "Arjun", "math": 85, "science": 92, "english": 78},
            "S002": {"name": "Nisha", "math": 95, "science": 88, "english": 90},
            "S003": {"name": "Rohan", "math": 72, "science": 79, "english": 85},
            "S004": {"name": "Divya", "math": 88, "science": 95, "english": 92},
            "S005": {"name": "Karan", "math": 80, "science": 82, "english": 88}
        }

    def calculate_student_averages(self):
        """
        Calculate and print average score for each student across all subjects.
        
        Processing:
            - For each student, calculate average of math, science, english
            - Round to 1 decimal place
        Output:
            - Print: "Student Averages: {dictionary with student_id: average}"
        """
        averages = {}
        """Your code here"""
        print(f"Student Averages: {averages}")

    def find_highest_average(self):
        """
        Find and print the student with the highest average score.
        
        Processing:
            - Calculate average for each student
            - Find student with maximum average
        Output:
            - Print: "Highest Average: {name} ({student_id}) - {average}"
        """
        highest_avg = -1
        highest_student_id = None
        highest_name = None
        
        for student_id, scores in self.students.items():
            """Your code here"""
            print(f"Highest Average: {highest_name} ({highest_student_id}) - {highest_avg}")

    def calculate_subject_averages(self):
        """
        Calculate and print average score for each subject across all students.
        
        Processing:
            - Sum scores for each subject across all students
            - Divide by number of students
            - Round to 1 decimal place
        Output:
            - Print: "Subject Averages: {dictionary with subject: average}"
        """
        total_math = 0
        total_science = 0
        total_english = 0
        num_students = len(self.students)
        
        for scores in self.students.values():
            """Your code here"""
        
        subject_averages = {
            """Your code here"""
        }
        
        print(f"Subject Averages: {subject_averages}")

