import pandas as pd
from typing import List, Dict

class MenuAgent:
    def __init__(self, menu_df, orders_df, order_items_df):
        self.menu_df = menu_df.copy()
        self.orders_df = orders_df.copy()
        self.order_items_df = order_items_df.copy()
        
        # Clean data for perfect matching
        for df in [self.menu_df, self.orders_df, self.order_items_df]:
            for col in ['Item_ID', 'Order_ID', 'Customer_ID']:
                if col in df.columns:
                    df[col] = df[col].astype(str).str.strip()
        
        # Standardize Status
        if 'Is_Active' in self.menu_df.columns:
            self.menu_df['Is_Active'] = self.menu_df['Is_Active'].astype(str).str.upper().str.strip()

    def get_smart_menu(self, cust_id: str = None) -> Dict:
        """Categorized Menu with Emergency Fallback"""
        try:
            menu_sections = {}
            
            # 1. Try strict filter
            active_menu = self.menu_df[self.menu_df['Is_Active'] == 'ACTIVE']

            # 🚨 EMERGENCY FALLBACK: If ACTIVE filter returns nothing, show everything
            if active_menu.empty:
                print("⚠️ WARNING: No 'ACTIVE' items found. Displaying all items for debugging.")
                active_menu = self.menu_df
            
            # --- Organize Sections ---
            
            # Section: Favorites
            if cust_id:
                fav_items = self._get_user_favorites(cust_id, active_menu)
                if fav_items: menu_sections["Your Favorites ⭐"] = fav_items

            # Section: Popular
            popular_items = self._get_popular_items(active_menu, limit=5)
            if popular_items: menu_sections["Popular Items 🔥"] = popular_items

            # Section: Budget
            budget_items = active_menu.sort_values(by='Current_Price').head(6).to_dict('records')
            menu_sections["Pocket Friendly 💰"] = budget_items

            # Section: Full Category-wise Menu
            for category in sorted(active_menu['Item_Category'].unique()):
                cat_items = active_menu[active_menu['Item_Category'] == category]
                menu_sections[category] = cat_items.to_dict('records')

            return {
                "status": "success",
                "menu_sections": menu_sections,
                "total_categories": len(menu_sections)
            }
            
        except Exception as e:
            print(f"MenuAgent Error: {e}")
            return {"status": "error", "message": str(e)}

    def _get_user_favorites(self, cust_id, active_menu):
        try:
            cust_orders = self.orders_df[self.orders_df['Customer_ID'] == cust_id]['Order_ID']
            if cust_orders.empty: return []
            user_items = self.order_items_df[self.order_items_df['Order_ID'].isin(cust_orders)]
            fav_ids = user_items['Item_ID'].value_counts().head(5).index.tolist()
            return active_menu[active_menu['Item_ID'].isin(fav_ids)].to_dict('records')
        except: return []

    def _get_popular_items(self, active_menu, limit):
        try:
            top_ids = self.order_items_df['Item_ID'].value_counts().head(limit).index.tolist()
            return active_menu[active_menu['Item_ID'].isin(top_ids)].to_dict('records')
        except: return []