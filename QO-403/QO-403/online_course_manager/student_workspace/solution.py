class CourseManager:
    """Manage online courses and student registrations."""

    def __init__(self):
        """Initialize the course manager with an empty courses dictionary."""
        self.courses = {}

    def add_course(self, course_id: str, title: str, capacity: int) -> None:
        """
        Add a new course to the manager.
        
        Parameters:
            course_id (str): Unique course identifier
            title (str): Course title/name
            capacity (int): Maximum number of students allowed
        
        Returns:
            None
        """
        self.courses[course_id] = {
            "title": title,
            "max": capacity,
            "students": []
        }

    def register_student(self, course_id: str, name: str) -> str:
        """
        Register a student to a course with capacity validation.
        
        Parameters:
            course_id (str): Course identifier
            name (str): Student name
        
        Returns:
            str: "Invalid ID" if course doesn't exist
                 "Course Full" if at capacity
                 "Enrolled in [title]" if successful
        """
        if course_id not in self.courses:
            return "Invalid ID"
        
        course = self.courses[course_id]
        
        if len(course["students"]) >= course["max"]:
            return "Course Full"
        
        course["students"].append(name)
        return f"Enrolled in {course['title']}"

    def get_available_seats(self, course_id: str) -> int:
        """
        Calculate available seats in a course.
        
        Parameters:
            course_id (str): Course identifier
        
        Returns:
            int: Number of available seats if course exists
                 -1 if course doesn't exist
        """
        if course_id not in self.courses:
            return -1
        
        course = self.courses[course_id]
        available = course["max"] - len(course["students"])
        return available

    def remove_student(self, course_id: str, name: str) -> str:
        """
        Remove a student from a course.
        
        Parameters:
            course_id (str): Course identifier
            name (str): Student name
        
        Returns:
            str: "Removed [name] from [title]" if successful
                 "Registration not found" if course/student doesn't exist
        """
        if course_id not in self.courses:
            return "Registration not found"
        
        course = self.courses[course_id]
        
        if name not in course["students"]:
            return "Registration not found"
        
        course["students"].remove(name)
        return f"Removed {name} from {course['title']}"
