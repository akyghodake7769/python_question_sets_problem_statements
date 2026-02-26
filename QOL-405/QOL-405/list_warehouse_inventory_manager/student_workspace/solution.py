"""
QL-603: List Warehouse Inventory Manager

A Python class to track warehouse stock using lists.
The class allows users to add new items, remove specific items, 
and query the current status of the inventory.
"""


class InventoryManager:
    """Manages warehouse inventory using a Python list."""
    
    def __init__(self):
        """Initialize an empty list named self.inventory."""
        self.inventory = []
    
    def add_item(self, item_name: str):
        """
        Add the given item_name string to the self.inventory list.
        
        Args:
            item_name (str): The name of the item to add to inventory
        """
        self.inventory.append(item_name)
    
    def remove_item(self, item_name: str):
        """
        Remove the first occurrence of item_name from the list.
        If item is not present, do not raise an error.
        
        Args:
            item_name (str): The name of the item to remove from inventory
        """
        if item_name in self.inventory:
            self.inventory.remove(item_name)
    
    def list_items(self) -> list:
        """
        Return the current self.inventory list.
        
        Returns:
            list: The current inventory list
        """
        return self.inventory
    
    def count_items(self) -> int:
        """
        Return the total number of items in the inventory.
        
        Returns:
            int: The count of items in inventory
        """
        return len(self.inventory)
