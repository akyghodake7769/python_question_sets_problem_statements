class Book:
    """
    Data Entity representing a single book.
    """
    def __init__(self, title: str, category: str):
        # TODO: Initialize title, category, is_available=True, days_borrowed=0
        pass

class DigitalLibraryManager:
    """
    Manager class for the library catalog and fine system.
    """
    def __init__(self):
        # TODO: Initialize empty catalog dictionary
        pass

    def add_book(self, title: str, category: str) -> str:
        # TODO: Create Book object and store in self.catalog
        return ""

    def borrow_book(self, title: str) -> str:
        # TODO: Toggle is_available to False and reset days
        return ""

    def pass_time(self, title: str, days: int) -> str:
        # TODO: Increase days_borrowed if book is out
        return ""

    def get_fine(self, title: str) -> float:
        # TODO: Logic: After 14 days, fine $5/day (Tech) or $2/day (others)
        return 0.0

    def available_in_category(self, category: str) -> list:
        # TODO: Filter catalog by category and availability
        return []

    def return_book(self, title: str) -> str:
        # TODO: Check fine. If fine > 0, return "Fine Due: $[fine]..."
        # Else: set available=True, return "Returned successfully."
        return ""
