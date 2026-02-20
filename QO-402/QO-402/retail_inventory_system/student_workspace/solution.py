class RetailStore:
    """Manage retail store inventory and operations."""

    def __init__(self):
        """Initialize the store with an empty inventory."""
        self.inventory = {}

    def register_product(self, name: str, price: float, stock: int) -> str:
        """
        Register a new product with price and initial stock.
        
        Parameters:
            name (str): Product name
            price (float): Product price
            stock (int): Initial stock quantity
        
        Returns:
            str: Confirmation message "Product [name] registered."
        """
        self.inventory[name] = {"price": price, "stock": stock}
        return f"Product {name} registered."

    def restock_item(self, name: str, quantity: int) -> str:
        """
        Increase stock for an existing product.
        
        Parameters:
            name (str): Product name
            quantity (int): Quantity to add
        
        Returns:
            str: Status message with new stock level or "Product not found."
        """
        if name in self.inventory:
            self.inventory[name]["stock"] += quantity
            new_stock = self.inventory[name]["stock"]
            return f"Restocked {name}. Now: {new_stock}"
        else:
            return "Product not found."

    def complete_sale(self, name: str, quantity: int) -> str:
        """
        Process a sale transaction with stock validation.
        
        Parameters:
            name (str): Product name
            quantity (int): Quantity to sell
        
        Returns:
            str: Bill string, insufficient stock message, or out of catalog message
        """
        if name not in self.inventory:
            return "Out of catalog."
        
        if self.inventory[name]["stock"] < quantity:
            return "Insufficient stock."
        
        # Calculate total and deduct stock
        price = self.inventory[name]["price"]
        total = price * quantity
        self.inventory[name]["stock"] -= quantity
        
        return f"Bill: ${total}"

    def inventory_report(self) -> float:
        """
        Calculate total monetary value of all inventory.
        
        Returns:
            float: Sum of (price × stock) for all products
        """
        total_value = 0
        for product_data in self.inventory.values():
            total_value += product_data["price"] * product_data["stock"]
        
        return total_value
