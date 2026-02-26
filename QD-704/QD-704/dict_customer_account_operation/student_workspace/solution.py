class CustomerManager:
    """Manage customer dictionary and perform required operations."""

    def __init__(self):
        self.customers = {
            "C101": {"name": "Tushar", "region": "North", "balance": 1500.50},
            "C102": {"name": "Pooja", "region": "South", "balance": 2500.00},
            "C103": {"name": "Karan", "region": "North", "balance": 900.75},
            "C104": {"name": "Deepa", "region": "West", "balance": 5000.25},
            "C105": {"name": "Amit", "region": "North", "balance": 1000.00}
        }

    def count_customers_by_region(self, region):
        """Print total number of customers in the given region."""
        total = sum(1 for c in self.customers.values() if c.get("region") == region)
        print(f"Total Customers in {region}: {total}")

    def find_highest_balance_customer(self):
        """Find and print the customer with the highest account balance."""
        if not self.customers:
            print("No customers found")
            return
        highest_id, highest = max(self.customers.items(), key=lambda it: it[1].get("balance", 0))
        name = highest.get("name")
        balance = highest.get("balance")
        print(f"Highest Balance Customer: {name} ({highest_id}) - {balance:.2f}")

    def check_customer(self, customer_id):
        """Check existence of a customer by ID and print details."""
        if customer_id in self.customers:
            c = self.customers[customer_id]
            print(f"Customer {customer_id}: {c.get('name')} - Balance: {c.get('balance'):.2f}")
        else:
            print(f"Customer {customer_id} not found")
