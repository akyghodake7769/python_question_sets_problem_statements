# student_workspace/solution.py

class MembershipSystem:
    """
    Club Membership System using Dictionary.
    Manages member registration, lookup, and deletion operations.
    """
    
    def __init__(self):
        """
        Initialize the membership system with an empty dictionary.
        
        The members dictionary maps member_id (string) to name (string).
        """
        self.members = {}
    
    def register_member(self, member_id: str, name: str):
        """
        Register a new member in the system.
        
        Parameters:
            member_id (str): Unique identifier for the member
            name (str): Full name of the member
        """
        self.members[member_id] = name
    
    def get_member(self, member_id: str) -> str:
        """
        Lookup a member's name by ID.
        
        Parameters:
            member_id (str): Unique identifier to look up
        
        Returns:
            str: Member's name if found, "Not Found" if member_id doesn't exist
        """
        if member_id in self.members:
            return self.members[member_id]
        return "Not Found"
    
    def remove_member(self, member_id: str):
        """
        Remove a member from the system.
        
        Parameters:
            member_id (str): Unique identifier to remove
        """
        if member_id in self.members:
            del self.members[member_id]
    
    def list_all_members(self) -> list:
        """
        Get all member names in the system.
        
        Returns:
            list: List containing all member names in the system.
                  Returns empty list if no members exist.
        """
        return list(self.members.values())
