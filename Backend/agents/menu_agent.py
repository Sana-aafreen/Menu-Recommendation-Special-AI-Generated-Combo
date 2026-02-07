import pandas as pd
from typing import List, Dict

class MenuAgent:
    """
    MenuAgent optimized for DineIQ_DB.xlsx structure
    Works with existing columns without requiring additional data
    """
    
    def __init__(self, menu_df, orders_df, order_items_df):
        self.menu_df = menu_df.copy()
        self.orders_df = orders_df.copy()
        self.order_items_df = order_items_df.copy()
        
        # Clean Data - Strip whitespace and normalize IDs
        self.menu_df['Item_ID'] = self.menu_df['Item_ID'].astype(str).str.strip()
        self.menu_df['Item_Name'] = self.menu_df['Item_Name'].astype(str).str.strip()
        self.menu_df['Item_Category'] = self.menu_df['Item_Category'].astype(str).str.strip()
        
        self.orders_df['Order_ID'] = self.orders_df['Order_ID'].astype(str).str.strip()
        self.orders_df['Customer_ID'] = self.orders_df['Customer_ID'].astype(str).str.strip()
        
        self.order_items_df['Order_ID'] = self.order_items_df['Order_ID'].astype(str).str.strip()
        self.order_items_df['Item_ID'] = self.order_items_df['Item_ID'].astype(str).str.strip()
        self.order_items_df['Item_Name'] = self.order_items_df['Item_Name'].astype(str).str.strip()
        
        # Category-based images (fallback)
        self.category_images = {
            'Bread': 'https://images.unsplash.com/photo-1509440159596-0249088772ff',
            'Rice': 'https://images.unsplash.com/photo-1516714435131-44d6b64dc6a2',
            'Gravy': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe',
            'Dry Veg': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd',
            'Starter': 'https://images.unsplash.com/photo-1599487488170-d11ec9c172f0',
            'Snacks': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Beverages': 'https://images.unsplash.com/photo-1437418747212-8d9709afab22',
            'Smoothies': 'https://images.unsplash.com/photo-1505252585461-04db1eb84625',
            'Dessert': 'https://images.unsplash.com/photo-1488477181946-6428a0291777',
            'Raita': 'https://images.unsplash.com/photo-1596797038530-2c107229654b',
        }
        
        # Veg items detector (common names)
        self.veg_keywords = ['paneer', 'aloo', 'gobi', 'dal', 'roti', 'naan', 'rice', 
                            'veg', 'vegetable', 'bhindi', 'palak', 'matar', 'raita',
                            'lassi', 'juice', 'smoothie', 'salad']

    def _is_veg_item(self, item_name: str) -> bool:
        """Detect if item is vegetarian based on name"""
        name_lower = item_name.lower()
        
        # Non-veg keywords
        non_veg = ['chicken', 'mutton', 'fish', 'egg', 'meat', 'prawn', 'lamb']
        if any(word in name_lower for word in non_veg):
            return False
        
        # Veg keywords
        if any(word in name_lower for word in self.veg_keywords):
            return True
        
        # Default to veg if uncertain (safer for Indian restaurants)
        return True

    def _get_image_for_item(self, category: str, item_name: str) -> str:
        """Get appropriate image based on category or item name"""
        # Try exact category match
        if category in self.category_images:
            return self.category_images[category]
        
        # Fuzzy match on item name
        name_lower = item_name.lower()
        if 'paneer' in name_lower or 'butter' in name_lower:
            return 'https://images.unsplash.com/photo-1585937421612-70a008356fbe'
        elif 'biryani' in name_lower or 'rice' in name_lower:
            return 'https://images.unsplash.com/photo-1516714435131-44d6b64dc6a2'
        elif 'naan' in name_lower or 'roti' in name_lower:
            return 'https://images.unsplash.com/photo-1509440159596-0249088772ff'
        elif 'dal' in name_lower:
            return 'https://images.unsplash.com/photo-1546833999-b9f581a1996d'
        elif 'dessert' in name_lower or 'sweet' in name_lower:
            return 'https://images.unsplash.com/photo-1488477181946-6428a0291777'
        
        # Default
        return 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c'

    def _get_item_description(self, category: str, item_name: str) -> str:
        """Generate description based on category"""
        descriptions = {
            'Bread': 'Freshly baked bread',
            'Rice': 'Aromatic basmati rice',
            'Gravy': 'Rich and flavorful curry',
            'Dry Veg': 'Delicious dry preparation',
            'Starter': 'Perfect appetizer',
            'Snacks': 'Tasty snack',
            'Beverages': 'Refreshing beverage',
            'Smoothies': 'Healthy smoothie',
            'Dessert': 'Sweet treat',
            'Raita': 'Cool yogurt accompaniment'
        }
        return descriptions.get(category, f'Delicious {category}')

    def get_smart_menu(self, email: str = None, user_prefs: Dict = None) -> Dict:
        """Get menu organized smartly for DineIQ frontend"""
        
        try:
            menu_sections = {}
            
            # Filter ACTIVE items
            valid_status = ['ACTIVE', 'YES', 'TRUE', '1', 'AVAILABLE', 'Y']
            active_df = self.menu_df[
                self.menu_df['Is_Active'].astype(str).str.upper().str.strip().isin(valid_status)
            ].copy()
            
            if active_df.empty:
                print("⚠️ WARNING: No active items found. Using all items.")
                active_df = self.menu_df.copy()

            print(f"\n{'='*60}")
            print(f"📊 MENU LOADING FOR: {email or 'Guest'}")
            print(f"{'='*60}")
            print(f"Total items in database: {len(self.menu_df)}")
            print(f"Active items: {len(active_df)}")
            
            # Helper to convert row to frontend format
            def format_item(row) -> dict:
                item_name = str(row['Item_Name'])
                category = str(row['Item_Category'])
                
                return {
                    'Item_ID': str(row['Item_ID']),
                    'Item_Name': item_name,
                    'Item_Description': self._get_item_description(category, item_name),
                    'Current_Price': float(row['Current_Price']),
                    'Image_URL': self._get_image_for_item(category, item_name),
                    'Is_Veg': self._is_veg_item(item_name),
                    'Item_Category': category,
                    'Dietary_Type': 'Veg' if self._is_veg_item(item_name) else 'Non-Veg'
                }

            # 1. USER'S FAVORITES (from order history)
            if email:
                try:
                    # Find customer ID from email
                    matching_orders = self.orders_df[
                        self.orders_df['Customer_ID'].str.contains(email.split('@')[0], case=False, na=False)
                    ]
                    
                    if not matching_orders.empty:
                        order_ids = matching_orders['Order_ID'].unique()
                        past_items = self.order_items_df[
                            self.order_items_df['Order_ID'].isin(order_ids)
                        ]['Item_Name'].unique()
                        
                        fav_items = active_df[active_df['Item_Name'].isin(past_items)]
                        if not fav_items.empty:
                            menu_sections["Your Favorites"] = [
                                format_item(row) for _, row in fav_items.iterrows()
                            ]
                            print(f"✅ Favorites: {len(fav_items)} items")
                except Exception as e:
                    print(f"⚠️ Favorites error: {e}")

            # 2. BESTSELLERS (most ordered items)
            try:
                popular_names = self.order_items_df['Item_Name'].value_counts().head(6).index
                bestsellers = active_df[active_df['Item_Name'].isin(popular_names)]
                
                if not bestsellers.empty:
                    menu_sections["Bestseller"] = [
                        format_item(row) for _, row in bestsellers.iterrows()
                    ]
                    print(f"✅ Bestsellers: {len(bestsellers)} items")
            except Exception as e:
                print(f"⚠️ Bestsellers error: {e}")

            # 3. CHEF'S SPECIAL (premium items - top 30% by price)
            try:
                sorted_by_price = active_df.sort_values(by='Current_Price', ascending=False)
                n = len(sorted_by_price)
                chef_special = sorted_by_price.head(max(1, int(n * 0.3)))
                
                if not chef_special.empty:
                    menu_sections["Chef Special"] = [
                        format_item(row) for _, row in chef_special.head(8).iterrows()
                    ]
                    print(f"✅ Chef Special: {len(chef_special)} items")
            except Exception as e:
                print(f"⚠️ Chef Special error: {e}")

            # 4. COMBOS (if you add combos to your menu, they'll appear here)
            combo_keywords = ['combo', 'meal', 'family', 'pack', 'thali']
            combo_items = active_df[
                active_df['Item_Name'].str.lower().str.contains('|'.join(combo_keywords), na=False)
            ]
            
            if not combo_items.empty:
                menu_sections["Combos"] = [
                    format_item(row) for _, row in combo_items.iterrows()
                ]
                print(f"✅ Combos: {len(combo_items)} items")

            # 5. CATEGORY SECTIONS (all categories)
            categories = active_df['Item_Category'].unique()
            print(f"\n📂 Categories found: {', '.join(categories)}")
            
            for category in sorted(categories):
                cat_items = active_df[active_df['Item_Category'] == category]
                
                if not cat_items.empty:
                    menu_sections[category] = [
                        format_item(row) for _, row in cat_items.iterrows()
                    ]
                    print(f"  • {category}: {len(cat_items)} items")

            print(f"\n{'='*60}")
            print(f"📦 FINAL MENU STRUCTURE:")
            print(f"{'='*60}")
            total_in_sections = sum(len(items) for items in menu_sections.values())
            for section, items in menu_sections.items():
                print(f"  {section}: {len(items)} items")
            print(f"\nTotal items across all sections: {total_in_sections}")
            print(f"{'='*60}\n")

            return {
                "status": "success",
                "menu_sections": menu_sections,
                "total_items": len(active_df),
                "categories": list(menu_sections.keys())
            }
            
        except Exception as e:
            print(f"\n❌ MENU AGENT ERROR:")
            print(f"{'='*60}")
            import traceback
            traceback.print_exc()
            print(f"{'='*60}\n")
            
            return {
                "status": "error",
                "menu_sections": {},
                "message": str(e)
            }

    def get_upsell_items(self, categories: List[str] = ['Dessert', 'Beverages']) -> Dict[str, List[Dict]]:
        """Get specific category items for upsell (e.g. Sweets, Drinks)"""
        try:
            upsells = {}
            # Active items only
            valid_status = ['ACTIVE', 'YES', 'TRUE', '1', 'AVAILABLE', 'Y']
            active_df = self.menu_df[
                self.menu_df['Is_Active'].astype(str).str.upper().str.strip().isin(valid_status)
            ].copy()

            for cat in categories:
                # Fuzzy match for category
                cat_items = active_df[
                    active_df['Item_Category'].str.lower().str.contains(cat.lower(), na=False)
                ]
                
                if not cat_items.empty:
                    # Return top 5 items
                    items_list = []
                    for _, row in cat_items.head(5).iterrows():
                        items_list.append({
                             'Item_ID': str(row['Item_ID']),
                             'Item_Name': str(row['Item_Name']),
                             'Current_Price': float(row['Current_Price']),
                             'Image_URL': self._get_image_for_item(row['Item_Category'], str(row['Item_Name'])),
                             'Item_Category': str(row['Item_Category']),
                             'Is_Veg': self._is_veg_item(str(row['Item_Name']))
                        })
                    upsells[cat] = items_list
            
            return upsells
        except Exception as e:
            print(f"Upsell Error: {e}")
            return {}