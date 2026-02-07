import pandas as pd
import traceback
import json

class RecommendationAgent:
    def __init__(self, menu_df, prefs_df, order_items_df, orders_df, groq_client=None):
        self.menu_df = menu_df.copy()
        self.prefs_df = prefs_df.copy()
        self.order_items_df = order_items_df.copy()
        self.orders_df = orders_df.copy()
        self.client = groq_client
        
        # Consistent Data Cleaning: Strip spaces and normalize IDs
        self.menu_df['Item_ID'] = self.menu_df['Item_ID'].astype(str).str.strip()
        self.menu_df['Is_Active'] = self.menu_df['Is_Active'].astype(str).str.upper().str.strip()
        self.order_items_df['Item_ID'] = self.order_items_df['Item_ID'].astype(str).str.strip()

        # 🍽️ STRATEGIC CATEGORY MAPPING: Defining logical pairs for cross-selling
        self.category_pairings = {
            'Bread': {'pairs_with': ['Gravy', 'DryVeg'], 'message': 'Perfect with curry!'},
            'Rice': {'pairs_with': ['Gravy', 'Dessert', 'Raita'], 'message': 'Complete your meal!'},
            'Gravy': {'pairs_with': ['Bread', 'Rice'], 'message': 'Best with bread or rice!'},
            'Starter': {'pairs_with': ['Beverages', 'Smoothies'], 'message': 'Pair with a refreshing drink!'},
            'Snacks': {'pairs_with': ['Beverages', 'Smoothies'], 'message': 'Great with a drink!'}
        }

    def get_recommendations(self, email: str, current_item_id: str):
        """Advanced Hybrid Recommendations: History + Category Intelligence"""
        try:
            current_item_id = str(current_item_id).strip()
            item_match = self.menu_df[self.menu_df['Item_ID'] == current_item_id]
            
            if item_match.empty:
                return {"ai_pitch": "Explore our bestsellers!", "add_ons": self._get_popular_fallback()}

            item = item_match.iloc[0]
            
            # User Preference fetch (Mapping user dietary needs)
            user_row = self.prefs_df[self.prefs_df['Email'] == email]
            diet = user_row.iloc[0]['Dietary'] if not user_row.empty else "General"

            # Strategy 1: Logical Category Pairing
            pairing_info = self.category_pairings.get(item['Item_Category'], {'pairs_with': ['Beverages']})
            pairing_recs = self._get_items_by_category(pairing_info['pairs_with'], diet, current_item_id)
            
            # Strategy 2: Frequently Bought Together (Order History Analysis)
            history_recs = self._get_frequently_bought_together(current_item_id, diet)

            # --- Unified Deduplication Logic ---
            final_recs = []
            seen_ids = {current_item_id}
            
            for rec in (history_recs + pairing_recs):
                if rec['Item_ID'] not in seen_ids:
                    final_recs.append(rec)
                    seen_ids.add(rec['Item_ID'])
                if len(final_recs) >= 3: break # Limit for UI

            # Fallback
            if not final_recs:
                final_recs = self._get_popular_fallback(diet)[:3]

            # AI Pitch generation using LLM
            ai_pitch = self._generate_ai_pitch(item['Item_Name'], item['Item_Category'], final_recs)

            return {"ai_pitch": ai_pitch, "add_ons": final_recs}
        except Exception as e:
            traceback.print_exc()
            return {"ai_pitch": "Pairs great with your meal!", "add_ons": []}

    def create_ai_combo(self, email: str):
        """🤖 Automated Combo Logic: Bundling for higher order value"""
        try:
            user_row = self.prefs_df[self.prefs_df['Email'] == email]
            diet = user_row.iloc[0]['Dietary'] if not user_row.empty else "General"
            
            combo_items = []
            for cat in ['Rice', 'Gravy', 'Beverages']:
                items = self._get_items_by_category([cat], diet, None)
                if items: combo_items.append(items[0])

            if len(combo_items) < 2: return None

            total = sum(i['Current_Price'] for i in combo_items)
            discount = 15 # 15% Savings
            
            name, desc = self._generate_ai_combo_details(combo_items)

            return {
                "combo_name": name,
                "description": desc,
                "items": combo_items,
                "original_price": round(total, 2),
                "combo_price": round(total * (1 - discount/100), 2),
                "savings": round(total * (discount/100), 2),
                "discount_percent": discount
            }
        except: return None

    def _get_items_by_category(self, cats, diet, exclude_id):
        mask = (self.menu_df['Item_Category'].isin(cats)) & (self.menu_df['Is_Active'] == 'ACTIVE')
        if exclude_id: mask &= (self.menu_df['Item_ID'] != exclude_id)
        
        items = self.menu_df[mask].copy()
        
        # Strict Veg Filter
        if diet in ["Pure Veg", "Vegetarian"]:
            items = items[~items['Item_Name'].str.contains('Chicken|Egg|Meat|Fish|Mutton', case=False, na=False)]
        
        return [{"Item_ID": r['Item_ID'], "Item_Name": r['Item_Name'], "Current_Price": float(r['Current_Price']), "Category": r['Item_Category']} 
                for _, r in items.head(3).iterrows()]

    def _get_frequently_bought_together(self, item_id, diet):
        try:
            order_ids = self.order_items_df[self.order_items_df['Item_ID'] == item_id]['Order_ID'].unique()
            others = self.order_items_df[(self.order_items_df['Order_ID'].isin(order_ids)) & (self.order_items_df['Item_ID'] != item_id)]
            top_ids = others['Item_ID'].value_counts().head(2).index.tolist()
            return self._format_items_list(top_ids, diet, "Often added together")
        except: return []

    def _format_items_list(self, ids, diet, tag):
        active_menu = self.menu_df[self.menu_df['Is_Active'] == 'ACTIVE']
        res = []
        for i_id in ids:
            match = active_menu[active_menu['Item_ID'] == i_id]
            if not match.empty:
                row = match.iloc[0]
                if diet in ["Pure Veg", "Vegetarian"] and any(f in row['Item_Name'].upper() for f in ['CHICKEN', 'EGG', 'MEAT']): continue
                res.append({"Item_ID": row['Item_ID'], "Item_Name": row['Item_Name'], "Current_Price": float(row['Current_Price']), "tag": tag})
        return res

    def _get_popular_fallback(self, diet="General"):
        popular_ids = self.order_items_df['Item_ID'].value_counts().head(5).index.tolist()
        return self._format_items_list(popular_ids, diet, "Bestseller")

    def _generate_ai_pitch(self, name, cat, recs):
        if not recs or not self.client: return f"Make it a feast with these!"
        try:
            prompt = f"Write a 1-line appetizing pitch for adding {recs[0]['Item_Name']} to {name} ({cat}). Max 12 words."
            res = self.client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
            return res.choices[0].message.content.strip().replace('"', '')
        except: return "Perfect combo for your meal! 🍱"

    def _generate_ai_combo_details(self, items):
        if not self.client: return "Smart Value Combo", "Handpicked pairing for you."
        try:
            names = [i['Item_Name'] for i in items]
            prompt = f"Create a catchy 3-word Indian combo name and 1-line description for: {', '.join(names)}. Separate name and desc with a pipe |"
            res = self.client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
            text = res.choices[0].message.content.strip().split('|')
            return text[0].strip(), text[-1].strip()
        except: return "DineIQ Special", "The perfect balanced meal."