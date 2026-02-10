class SupplyChainInventory:
    """Supply Chain Inventory Tracker for retail chain product management."""

    def __init__(self):
        """Initialize an empty inventory dictionary."""
        self.stock = {}

    def add_product(self, product_id: str, quantity: int) -> dict:
        """
        Add a new product or update existing product stock.
        
        Args:
            product_id: Unique product identifier
            quantity: Number of units to add
        
        Returns:
            Updated stock dictionary
        """
        if product_id in self.stock:
            self.stock[product_id] += quantity
        else:
            self.stock[product_id] = quantity
        return self.stock

    def fulfill_order(self, product_id: str, quantity: int) -> dict:
        """
        Fulfill an order by deducting from stock.
        
        Args:
            product_id: Unique product identifier
            quantity: Number of units to deduct
        
        Returns:
            Updated stock dictionary
        
        Raises:
            ValueError: If product not found or insufficient stock
        """
        if product_id not in self.stock:
            raise ValueError(f"Product {product_id} not found in inventory")
        
        if self.stock[product_id] < quantity:
            raise ValueError(f"Insufficient stock for {product_id}. Available: {self.stock[product_id]}, Requested: {quantity}")
        
        self.stock[product_id] -= quantity
        return self.stock

    def restock_return(self, product_id: str, quantity: int) -> dict:
        """
        Add returned goods back into stock.
        
        Args:
            product_id: Unique product identifier
            quantity: Number of units to add back
        
        Returns:
            Updated stock dictionary
        """
        if product_id in self.stock:
            self.stock[product_id] += quantity
        else:
            self.stock[product_id] = quantity
        return self.stock

    def list_available_products(self) -> list:
        """
        List all products with stock greater than 0.
        
        Returns:
            List of product IDs with available stock
        """
        return [product_id for product_id, qty in self.stock.items() if qty > 0]
