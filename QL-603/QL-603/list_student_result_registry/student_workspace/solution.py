class ResultRegistry:
    """Manage student scores and provide analysis operations."""

    def __init__(self):
        """Initialize the score list with sample data."""
        self.scores = [45, 78, 92, 55, 88, 67, 95, 52]

    def create_status_dict(self) -> dict:
        """Map each score to its pass/fail status."""
        status_dict = {}
        for score in self.scores:
            if score >= 80:
                status_dict[score] = "Pass"
            else:
                status_dict[score] = "Fail"
        return status_dict

    def find_highest_score(self) -> int:
        """Find and return the highest score."""
        return max(self.scores)

    def calculate_average(self) -> float:
        """Calculate and return the average score rounded to 1 decimal place."""
        average = sum(self.scores) / len(self.scores)
        return round(average, 1)

    def get_passing_scores(self) -> list:
        """Get all passing scores (>= 80) sorted in descending order."""
        passing = [score for score in self.scores if score >= 80]
        return sorted(passing, reverse=True)

    def get_failed_scores(self) -> list:
        """Get all failed scores (< 80) sorted in ascending order."""
        failed = [score for score in self.scores if score < 80]
        return sorted(failed)

    def count_pass_fail(self) -> dict:
        """Count the total number of passing and failing students."""
        d = self.create_status_dict()
        vals = list(d.values())
        return {'Pass': vals.count('Pass'), 'Fail': vals.count('Fail')}
