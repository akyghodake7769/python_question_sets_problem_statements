class RetailInventorySystem:
    def __init__(self):
        self.inventory = {}

    def register_product(self, name: str, price: float, stock: int) -> str:
        self.inventory[name] = {'price': price, 'stock': stock}
        return f"Product {name} registered."

    def restock_item(self, name: str, quantity: int) -> str:
        if name in self.inventory:
            self.inventory[name]['stock'] += quantity
            return f"Restocked {name}. Now: {self.inventory[name]['stock']}"
        return "Product not found."

    def complete_sale(self, name: str, quantity: int) -> str:
        if name in self.inventory:
            if self.inventory[name]['stock'] >= quantity:
                self.inventory[name]['stock'] -= quantity
                total = self.inventory[name]['price'] * quantity
                return f"Bill: ${total}"
            return "Insufficient stock."
        return "Out of catalog."

    def inventory_report(self) -> float:
        total_value = sum(item['price'] * item['stock'] for item in self.inventory.values())
        return float(total_value)

    def get_product_info(self, name: str) -> dict:
        if name in self.inventory:
            return self.inventory[name]
        return "Product not found."

    def remove_product(self, name: str) -> str:
        if name in self.inventory:
            del self.inventory[name]
            return f"Removed {name} from catalog."
        return "Product not found."
