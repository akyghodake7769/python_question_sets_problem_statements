"""
QOD-408: Student Grade System

A Python class to manage student records using dictionaries.
The class allows students to be registered with their grades,
grades can be updated, and comprehensive statistics can be retrieved.
"""


class GradeSystem:
    """Manages student grade records using a nested dictionary."""
    
    def __init__(self):
        """Initialize an empty dictionary named self.records."""
        self.records = {}
    
    def add_student(self, roll_id: str, name: str, grade: float):
        """
        Add a new student record to the system.
        
        Args:
            roll_id (str): The student's roll ID
            name (str): The student's name
            grade (float): The student's grade
        """
        self.records[roll_id] = {"name": name, "grade": grade}
    
    def update_grade(self, roll_id: str, new_grade: float) -> bool:
        """
        Update the grade for an existing student.
        
        Args:
            roll_id (str): The student's roll ID
            new_grade (float): The new grade to update
        
        Returns:
            bool: True if update was successful, False if roll_id doesn't exist
        """
        if roll_id in self.records:
            self.records[roll_id]["grade"] = new_grade
            return True
        return False
    
    def get_average(self) -> float:
        """
        Calculate and return the average grade of all students.
        
        Returns:
            float: Average grade rounded to 2 decimal places, or 0.0 if no students
        """
        if not self.records:
            return 0.0
        total = sum(student["grade"] for student in self.records.values())
        average = total / len(self.records)
        return round(average, 2)
    
    def get_student_info(self, roll_id: str) -> str:
        """
        Get formatted information about a student.
        
        Args:
            roll_id (str): The student's roll ID
        
        Returns:
            str: Formatted string "Name: <name>, Grade: <grade>"
                 or "Student Not Found" if roll_id doesn't exist
        """
        if roll_id in self.records:
            student = self.records[roll_id]
            return f"Name: {student['name']}, Grade: {student['grade']}"
        return "Student Not Found"
    
    def remove_student(self, roll_id: str):
        """
        Remove a student record from the system.
        
        Args:
            roll_id (str): The student's roll ID to remove
        """
        if roll_id in self.records:
            del self.records[roll_id]
