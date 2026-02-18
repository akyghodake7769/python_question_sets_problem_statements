class ScoreManager:
    """Manage and analyze student scores."""

    def __init__(self):
        """Initialize with predefined score list."""
        self.scores = [45, 78, 92, 55, 88, 67, 95, 52]

    def create_status_dict(self):
        """
        Create a dictionary mapping each score to its status.
        
        Logic:
        - If score >= 80 → status = "Pass"
        - If score < 80 → status = "Fail"
        
        Returns:
            Dictionary with scores as keys and Pass/Fail as values
        """
        status_dict = {}
        """Your code here"""
        return status_dict

    def find_highest_score(self):
        """
        Find the highest score in the list.
        
        Returns:
            Integer - the maximum score
        """
        """Your code here"""

    def calculate_average(self):
        """
        Calculate the average score.
        
        Returns:
            Float - average rounded to 1 decimal place
        """
        """Your code here"""
        return round(avg, 1)

    def get_passing_scores(self):
        """
        Get all passing scores (>= 80) sorted in descending order.
        
        Returns:
            List of passing scores in descending order
        """
        passing = []
        for score in self.scores:
            if score >= 80:
                passing.append(score)
        passing.sort(reverse=True)
        return passing

