class EventManager:
    """
    Event Data Management System using Dictionaries.
    Manages events with efficient dictionary-based operations.
    """

    def __init__(self):
        """
        Initialize the EventManager.
        Create storage for event data using dictionaries.
        """
        self.events = {}

    def add_event(self, event_id: str, event_data: dict) -> bool:
        """
        Add a new event to the manager.
        
        Parameters:
            event_id (str): Unique identifier for the event
            event_data (dict): Dictionary containing event details (name, type, timestamp)
        
        Returns:
            bool: True if event added successfully, False if event_id already exists
        """
        if event_id in self.events:
            return False
        self.events[event_id] = event_data
        return True

    def get_event(self, event_id: str) -> dict:
        """
        Get event details by event ID.
        
        Parameters:
            event_id (str): The event identifier to retrieve
        
        Returns:
            dict: Event data if found, empty dict if not found
        """
        return self.events.get(event_id, {})

    def filter_events_by_type(self, event_type: str) -> list:
        """
        Get all events of a specific type.
        
        Parameters:
            event_type (str): The type of events to filter (e.g., "login", "error")
        
        Returns:
            list: List of event IDs matching the event type, empty list if none found
        """
        matching_events = []
        for event_id, event_data in self.events.items():
            if event_data.get('type') == event_type:
                matching_events.append(event_id)
        return matching_events

    def get_event_summary(self) -> dict:
        """
        Get summary statistics about all events.
        
        Returns:
            dict: Contains 'total_events', 'unique_types', 'event_ids'
                  Returns zeros if no events
        """
        if len(self.events) == 0:
            return {
                'total_events': 0,
                'unique_types': 0,
                'event_ids': []
            }
        
        unique_types = set()
        for event_data in self.events.values():
            if 'type' in event_data:
                unique_types.add(event_data['type'])
        
        return {
            'total_events': len(self.events),
            'unique_types': len(unique_types),
            'event_ids': list(self.events.keys())
        }
