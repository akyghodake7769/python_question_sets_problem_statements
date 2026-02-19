class ProductManager:
    """Manage product prices and perform operations."""

    def __init__(self):
        """Initialize product price list with sample data."""
        self.prices = [250, 1500, 350, 2000, 800, 1200, 450, 3000]

    def calculate_total_revenue(self):
        """
        Calculate and print the total revenue from all products.
        
        Processing:
            - Sum all prices in the list
        Output:
            - Print: "Total Revenue: {total}"
        """
        total = sum(self.prices)
        print(f"Total Revenue: {total}")

    def apply_discount(self):
        """
        Apply 10% discount to all prices and print discounted prices list.
        
        Processing:
            - Apply 10% discount: price * 0.9
            - Convert to int
            - Create new list with discounted prices
        Output:
            - Print: "Discounted Prices: {list}"
        """
        discounted = [int(price * 0.9) for price in self.prices]
        print(f"Discounted Prices: {discounted}")

    def count_categories(self):
        """
        Count and print affordable and premium products.
        
        Processing:
            - Affordable: price < 1000
            - Premium: price >= 1000
        Output:
            - Print: "Affordable Count: {count}, Premium Count: {count}"
        """
        affordable_count = len([price for price in self.prices if price < 1000])
        premium_count = len([price for price in self.prices if price >= 1000])
        print(f"Affordable Count: {affordable_count}, Premium Count: {premium_count}")
