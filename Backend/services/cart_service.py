import pandas as pd

class CartService:
    def __init__(self):
        # Cart data temporary store karne ke liye dictionary (In-memory)
        # Real scenario mein ye 'Order_Items.csv' ya Redis mein jata hai
        self.user_carts = {}

    def update_cart(self, customer_id, items):
        """
        User ke cart ko update karta hai.
        items: List of CartItem objects (dish_id, quantity)
        """
        self.user_carts[customer_id] = items
        print(f"🛒 Cart Updated for {customer_id}: {len(items)} items.")
        return items

    def get_cart(self, customer_id):
        """User ka current cart return karta hai"""
        return self.user_carts.get(customer_id, [])

    def clear_cart(self, customer_id):
        """Order success hone ke baad cart khali karne ke liye"""
        if customer_id in self.user_carts:
            del self.user_carts[customer_id]