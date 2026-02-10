class SupplyChainInventory:

    def __init__(self):
        """Initialize an empty inventory dictionary."""
        self.stock = {}

    def add_product(self, product_id: str, quantity: int) -> dict:
        """Add a new product or update existing product stock.        
        Args: product_id: Unique product identifier, quantity: Number of units to add
        Returns:    Updated stock dictionary """
        #your code here
        return self.stock

    def fulfill_order(self, product_id: str, quantity: int) -> dict:
        """Fulfill an order by deducting from stock
        Args: product_id: Unique product identifier, quantity: Number of units to deduct
        Returns: Updated stock dictionary
        Raises: ValueError: If product not found or insufficient stock """
        #your code here
        return self.stock

    def restock_return(self, product_id: str, quantity: int) -> dict:
        """Add returned goods back into stock.
        Args: product_id: Unique product identifier, quantity: Number of units to add back
        Returns: Updated stock dictionary """
        #your code here        
        return self.stock

    def list_available_products(self) -> list:
        """List all products with stock greater than 0
        Returns: List of product IDs with available stock """
        #your code ehere
        return [product_id for product_id, qty in self.stock.items() if qty > 0]

