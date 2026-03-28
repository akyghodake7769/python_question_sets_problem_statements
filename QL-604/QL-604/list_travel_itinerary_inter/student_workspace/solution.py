class ItineraryPlanner:
    def __init__(self, cities: list):
        # TODO: Initialize self.destinations with the provided list of cities
        pass

    def add_destination(self, city: str) -> bool:
        # TODO: Append city only if it's not empty and not a sequential duplicate
        # Return True if added, else False
        return False

    def get_total_stops(self) -> int:
        # TODO: Return the number of unique stops in the itinerary
        return 0

    def get_stop_index(self, city: str) -> int:
        # TODO: Return the index of the first occurrence of the city, or -1 if not found
        return -1

    def remove_destination(self, city: str) -> bool:
        # TODO: Remove the first occurrence of the city and return True if successful
        return False

    def get_reversed_itinerary(self) -> list:
        # TODO: Return a new list with cities in reverse order and UPPERCASE
        return []

    def has_duplicates(self) -> bool:
        # TODO: Return True if any city appears more than once, otherwise False
        return False

    def format_itinerary(self) -> str:
        # TODO: Return cities joined by " -> ". If empty, return "No Destinations".
        # Append " (X stops)" to the end of the string.
        return ""
