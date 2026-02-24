class EventManager:
    """
    Event Data Management System using Dictionaries.
    Manages events with efficient dictionary-based operations.
    """

    def __init__(self):
        """
        Initialize the EventManager with empty event registry.
        
        Returns:
            None
        """
        self.events = {}

    def add_event(self, event_id: str, event_data: dict) -> bool:
        """
        Successfully add a new event.
        
        Parameters:
            event_id (str): Unique identifier for the event
            event_data (dict): Dictionary containing event details
        
        Returns:
            bool: True if event added successfully, False if event_id already exists
        """
        if event_id in self.events:
            return False
        self.events[event_id] = event_data
        return True

    def fetch_all(self) -> dict:
        """
        Retrieve the dictionary of all events.
        
        Returns:
            dict: Dictionary containing all events
        """
        return self.events

    def update_event(self, event_id: str, event_data: dict) -> bool:
        """
        Correctly update an existing event.
        
        Parameters:
            event_id (str): The event identifier to update
            event_data (dict): New event data to update with
        
        Returns:
            bool: True if event updated successfully, False if event_id doesn't exist
        """
        if event_id not in self.events:
            return False
        self.events[event_id] = event_data
        return True

    def delete_event(self, event_id: str) -> bool:
        """
        Correctly delete an event resource.
        
        Parameters:
            event_id (str): The event identifier to delete
        
        Returns:
            bool: True if event deleted successfully, False if event_id doesn't exist
        """
        if event_id not in self.events:
            return False
        del self.events[event_id]
        return True
