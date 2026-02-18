class StudentScoreAnalyzer:
    """Analyzer class for student scores with multiple operations."""
    
    def __init__(self):
        """Initializes an empty scores array."""
        self.scores = []
    
    def load_scores(self, scores_list):
        """
        Loads a list of student scores into the analyzer.
        
        Args:
            scores_list (list): List of student scores (integers 0-100)
        """
        self.scores = scores_list
        print(f"Loaded scores: {self.scores}")
    
    def create_status_dict(self):
        """
        Creates a dictionary mapping each score to its pass/fail status.
        Score >= 80 is 'Pass', Score < 80 is 'Fail'
        
        Returns:
            dict: Dictionary with scores as keys and status as values
        """
        # TODO: Implement this function
        # Create and return a dictionary where each score maps to 'Pass' or 'Fail'
        # Pass if score >= 80, Fail otherwise
        pass
    
    def highest_score(self):
        """
        Finds and prints the highest score in the list.
        
        Returns:
            int: The maximum score value
        """
        # TODO: Implement this function
        # Find and return the highest score from self.scores
        # Use max() function
        pass
    
    def average_score(self):
        """
        Calculates and prints the average score of all students.
        Formula: average = sum(scores) / count(scores)
        
        Returns:
            float: The average score rounded to 1 decimal place
        """
        # TODO: Implement this function
        # Calculate the average: sum(scores) / len(scores)
        # Round to 1 decimal place using round()
        # Return the average
        pass
    
    def passing_scores_desc(self):
        """
        Filters scores >= 80 and returns them in descending order.
        
        Returns:
            list: List of passing scores sorted in descending order
        """
        # TODO: Implement this function
        # 1. Filter scores >= 80
        # 2. Sort them in descending order
        # 3. Return the sorted list
        pass
    
    def display_all_results(self):
        """
        Displays all analysis results for the loaded scores.
        Calls all methods and shows complete summary.
        """
        print("\n" + "="*60)
        print("STUDENT SCORE ANALYSIS REPORT")
        print("="*60)
        self.create_status_dict()
        self.highest_score()
        self.average_score()
        self.passing_scores_desc()
        print("="*60 + "\n")


# Main Program - Test your implementation
if __name__ == "__main__":
    # Initialize analyzer
    analyzer = StudentScoreAnalyzer()
    
    # Load sample scores
    scores = [45, 78, 92, 55, 88, 67, 95, 52]
    analyzer.load_scores(scores)
    
    # Display all results
    analyzer.display_all_results()
