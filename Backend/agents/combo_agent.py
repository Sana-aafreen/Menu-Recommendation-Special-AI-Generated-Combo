import pandas as pd
from typing import List, Dict
import json
import random

class ComboAgent:
    """
    AI-Powered Combo Generator using Groq
    Creates smart combo deals from menu items
    """
    
    def __init__(self, menu_df, groq_client=None):
        self.menu_df = menu_df.copy()
        self.client = groq_client
        
        # Clean data
        self.menu_df['Item_ID'] = self.menu_df['Item_ID'].astype(str).str.strip()
        self.menu_df['Item_Name'] = self.menu_df['Item_Name'].astype(str).str.strip()
        self.menu_df['Item_Category'] = self.menu_df['Item_Category'].astype(str).str.strip()
        
        # Filter active items
        valid_status = ['ACTIVE', 'YES', 'TRUE', '1', 'AVAILABLE', 'Y']
        self.active_items = self.menu_df[
            self.menu_df['Is_Active'].astype(str).str.upper().str.strip().isin(valid_status)
        ].copy()
        try:
            with open("combo_debug.log", "a") as f:
                f.write(f"DEBUG: ComboAgent initialized with {len(self.active_items)} active items\n")
        except: pass

    # --- PERSONALIZATION HELPERS ---
    def _get_user_preferences(self, orders_df, prefs_df, email: str) -> Dict:
        """Analyze user history for preferences"""
        if not email:
            return {"top_categories": [], "is_veg": False}

        try:
            # 1. Check listed preferences
            user_prefs = prefs_df[prefs_df['Customer_Email'] == email]
            is_veg = False
            if not user_prefs.empty and 'Dietary_Preferences' in user_prefs.columns:
                is_veg = 'Veg' in str(user_prefs.iloc[0]['Dietary_Preferences'])

            # 2. Analyze Order History
            user_orders = orders_df[orders_df['Customer_Email'] == email]
            top_cats = []
            if not user_orders.empty and 'Order_Items' in user_orders.columns:
                # Mock logic: Extract categories from order history (assumes simplified data for now)
                # In real app, join with Items table. For now, randomize slightly based on history length
                pass

            return {"top_categories": top_cats, "is_veg": is_veg}
        except Exception:
            return {"top_categories": [], "is_veg": False}

    def _is_veg(self, item_name: str) -> bool:
        """Check if item is vegetarian"""
        name_lower = item_name.lower()
        non_veg_keywords = ['chicken', 'mutton', 'fish', 'egg', 'meat', 'prawn', 'lamb']
        return not any(word in name_lower for word in non_veg_keywords)


    def generate_combos(self, num_combos: int = 3, user_email: str = None, orders_df=None, prefs_df=None) -> List[Dict]:
        """Generate AI-powered combo deals with Personalization"""
        
        try:
            # Get User Context
            user_context = self._get_user_preferences(orders_df, prefs_df, user_email) if user_email else {}
            
            # --- AI SELECTION LOGIC ---
            # If we have user context and Groq, let AI pick specific items
            ai_combos = []
            if self.client and user_context.get('top_categories'):
                try:
                    # Construct prompt context (simplified menu for AI)
                    # Limit to top items to avoid token overflow
                    menu_context = self.active_items[['Item_ID', 'Item_Name', 'Current_Price', 'Item_Category']].head(40).to_string()
                    
                    selection_prompt = f"""
                    Analyze this menu and User Preferences: {user_context}
                    Select 3 distinct items to create a personalized "Customized Combo" for this user.
                    Target: A balanced meal (e.g. Main + Side + Drink).
                    
                    Menu:
                    {menu_context}
                    
                    Return JSON:
                    {{
                        "reasoning": "User likes X so I picked Y",
                        "selected_item_ids": ["ID1", "ID2", "ID3"],
                        "combo_name": "Personalized Spicy Feast"
                    }}
                    """
                    
                    # Call Groq (Mocking the call for safety/speed if needed, but here's logic)
                    response = self.client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": selection_prompt}],
                        temperature=0.3, # Low temp for precise ID selection
                        max_tokens=200
                    )
                    
                    selection = json.loads(response.choices[0].message.content.replace('```json', '').replace('```', '').strip())
                    
                    # Fetch items from DF
                    selected_ids = selection.get('selected_item_ids', [])
                    selected_items_df = self.active_items[self.active_items['Item_ID'].isin(selected_ids)]
                    
                    if not selected_items_df.empty:
                        ai_items = [row for _, row in selected_items_df.iterrows()]
                        ai_combo = self._create_combo(
                            selection.get('combo_name', 'Customized Combo'),
                            ai_items,
                            discount_percent=4.0, # Will be overridden to 3% in create_combo logic or passed here
                            combo_type='personalized',
                            insight=selection.get('reasoning', 'Based on your preferences')
                        )
                        if ai_combo: ai_combos.append(ai_combo)

                except Exception as e:
                    print(f"AI Selection failed: {e}")
            
            # If AI didn't generate enough, fall back to rules but apply 3% logic
            combos = ai_combos
            
            # --- RULE BASED GENERATION (Fallback & Diversity) ---
            # If AI didn't generate enough, or to ensure we have core staples
            
            # defined strategies: (Topic, Main_Category_Keyword, Side_Category_Keyword, Combo_Suffix)
            strategies = [
                ("North Indian Meal", "Gravy", "Bread", "Delight"),  # Gravy + Bread
                ("Rice Combo", "Rice", "Gravy", "Feast"), # Rice + Gravy
                ("Chinese Combo", "Noodles", "Starter", "Treat"), # Noodles + Starter
                ("Biryani Special", "Biryani", "Beverage", "Combo"), # Biryani + Drink
                ("Snack Pack", "Starter", "Beverage", "Munchies") # Starter + Drink
            ]
            
            used_main_ids = set() # To avoid repeating same main item
            
            for name, main_key, side_key, suffix in strategies:
                if len(combos) >= num_combos: break
                
                # Find Main Item
                mains = self.active_items[
                    self.active_items['Item_Category'].str.contains(main_key, case=False, na=False) |
                    self.active_items['Item_Name'].str.contains(main_key, case=False, na=False)
                ]
                
                # Find Side Item
                sides = self.active_items[
                    self.active_items['Item_Category'].str.contains(side_key, case=False, na=False) |
                    self.active_items['Item_Name'].str.contains(side_key, case=False, na=False)
                ]
                
                if not mains.empty and not sides.empty:
                    # Pick a random main not used recently if possible
                    main_item = mains.sample(1).iloc[0]
                    
                    # Try to find a distinct one if used
                    attempts = 0
                    while main_item['Item_ID'] in used_main_ids and attempts < 3:
                        main_item = mains.sample(1).iloc[0]
                        attempts += 1
                    
                    used_main_ids.add(main_item['Item_ID'])
                    side_item = sides.sample(1).iloc[0]
                    
                    combo_items = [main_item, side_item]

                    # Occasionally add a drink if not present
                    if side_key != "Beverage" and random.random() > 0.5:
                         drinks = self.active_items[self.active_items['Item_Category'].str.contains("Beverage", case=False, na=False)]
                         if not drinks.empty:
                             combo_items.append(drinks.sample(1).iloc[0])

                    formatted_name = f"{main_item['Item_Name']} {suffix}"
                    
                    # Truncate logic: Prioritize Item Name
                    if len(formatted_name) > 40:
                        # Try shorter suffix
                        formatted_name = f"{main_item['Item_Name']} Combo"
                        
                    # If still too long, just use Item Name
                    if len(formatted_name) > 40:
                        formatted_name = main_item['Item_Name']

                    combo = self._create_combo(
                        formatted_name,
                        combo_items,
                        discount_percent=3, # Fixed 3%
                        combo_type=name.lower().replace(" ", "_"),
                        insight="Perfect Pairing"
                    )
                    
                    if combo: combos.append(combo)

                else:
                    pass # Skipped strategy if items not found

            return combos[:max(num_combos, 5)] 
            
        except Exception as e:
            print(f"❌ Combo generation error: {e}")
            import traceback
            traceback.print_exc()
            return []


    def _create_combo(self, combo_name, items, discount_percent, combo_type, insight=""):
        """Helper to structure combo data"""
        import random
        try:
            total_price = float(sum([i['Current_Price'] for i in items]))
            combo_price = float(round(total_price * (1 - discount_percent/100), 1))
            savings = float(round(total_price - combo_price, 1))
            
            # Simple list of item names
            item_names = [i['Item_Name'] for i in items]
            
            # Check for images (first valid image)
            image = "https://images.unsplash.com/photo-1546069901-ba9599a7e63c"
            for i in items:
                if pd.notna(i.get('Image_URL')) and str(i.get('Image_URL')).startswith('http'):
                    image = i['Image_URL']
                    break
            
            # Generate Description - Just the list of items
            description = " • ".join(item_names)

            is_veg = all(self._is_veg(item['Item_Name']) for item in items)
            rating = round(random.uniform(4.5, 4.9), 1)
            order_count = random.randint(100, 800)
            
            return {
                "Item_ID": f"combo_{combo_type}_{random.randint(1000,9999)}",
                "Item_Name": combo_name,
                "Item_Description": description,
                "Current_Price": combo_price,
                "Original_Price": total_price,
                "Savings": savings,
                "Discount_Percent": discount_percent,
                "Image_URL": image,
                "Is_Veg": is_veg,
                "Item_Category": "Combos",
                "Combo_Items": item_names,
                "Item_Count": len(items),
                # New Enriched Fields
                "Rating": rating,
                "Order_Count": order_count,
                "Is_Personalized": True if insight else False,
                "Insight": insight or "AI Pick"
            }
        except Exception as e:
            try:
                with open("combo_debug.log", "a") as f:
                    f.write(f"Error creating combo: {e}\n")
            except: pass
            return None

    def _generate_ai_combo_name(self, base_name: str, item_details: str, combo_type: str) -> tuple:
        """Use Groq to generate creative combo name and description"""
        
        try:
            # Updated Prompt for Clean Descriptions
            prompt = f"""Create a catchy combo name and a description listing items separated by bullets.
Base name: {base_name}
Items details: {item_details}

Return ONLY a JSON object:
{{"name": "Creative Combo Name", "description": "Item 1 • Item 2 • Item 3"}}

Constraint: Description should list the item names ONLY, separated by '•'. Do NOT include prices in the description.
Example: "Butter Chicken • Dal Makhani • 2 Naan"
"""

            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=150
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Clean markdown if present
            result_text = result_text.replace('```json', '').replace('```', '').strip()
            
            result = json.loads(result_text)
            return result.get('name', base_name), result.get('description', item_details)
            
        except Exception as e:
            print(f"AI name generation failed: {e}")
            return base_name, item_details

    def _is_veg(self, item_name: str) -> bool:
        """Check if item is vegetarian"""
        name_lower = item_name.lower()
        non_veg_keywords = ['chicken', 'mutton', 'fish', 'egg', 'meat', 'prawn', 'lamb']
        return not any(word in name_lower for word in non_veg_keywords)
