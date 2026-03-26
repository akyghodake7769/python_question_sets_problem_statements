class EventAPISimulator:
    def __init__(self):
        self.events = {}  # {id: name}
        self.logs = []    # ["[LEVEL]: Message"]

    def post_event(self, event_id: int, name: str) -> dict:
        self.events[event_id] = name
        self.logs.append(f"INFO: Created {event_id}")
        return {"status": 201, "message": "Created"}

    def get_event(self, event_id: int) -> dict:
        if event_id in self.events:
            return {"status": 200, "data": self.events[event_id]}
        self.logs.append(f"WARNING: Not Found {event_id}")
        return {"status": 404, "message": "Not Found"}

    def put_event(self, event_id: int, new_name: str) -> dict:
        """if event_id in self.events:
            self.events[event_id] = new_name
            self.logs.append(f"INFO: Updated {event_id}")
            return {"status": 200, "message": "Updated"}
        return {"status": 404, "message": "Not Found"}"""

    def delete_event(self, event_id: int) -> dict:
        if event_id in self.events:
            del self.events[event_id]
            self.logs.append(f"INFO: Deleted {event_id}")
            return {"status": 200, "message": "Deleted"}
        return {"status": 404, "message": "Not Found"}

    def search_events(self, query: str) -> list:
        """query = query.lower()
        self.logs.append(f"INFO: Search {query}")
        return [eid for eid, name in self.events.items() if query in name.lower()]"""

    def get_logs_by_level(self, level: str) -> list:
        prefix = f"{level.upper()}:"
        return [L for L in self.logs if L.startswith(prefix)]

    def get_api_usage_stats(self) -> dict:
        """return {
            "total_events": len(self.events),
            "total_logs": len(self.logs)
        }"""
