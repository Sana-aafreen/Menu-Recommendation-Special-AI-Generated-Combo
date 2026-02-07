import pandas as pd
import os
import traceback
from datetime import datetime

class ProfileService:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_preferences(self, customer_id=None, email=None):
        """Links Auth data with Preferences using Email as the bridge"""
        try:
            if not os.path.exists(self.db_path):
                return {"diet": "Vegetarian", "Customer_Name": "Guest"}

            # Read Excel
            xls = pd.ExcelFile(self.db_path)
            
            # --- Auth Lookup ---
            if not email and customer_id and 'Customer_Auth' in xls.sheet_names:
                auth_df = pd.read_excel(xls, 'Customer_Auth')
                if 'Customer_ID' in auth_df.columns:
                    auth_df['Customer_ID'] = auth_df['Customer_ID'].astype(str).str.strip()
                if 'Customer_Email' in auth_df.columns:
                    user_auth = auth_df[auth_df['Customer_ID'] == str(customer_id).strip()]
                    if not user_auth.empty:
                        email = user_auth.iloc[0].get('Customer_Email')
            
            if not email:
                return {"diet": "Vegetarian", "Customer_Name": "Guest"}

            # --- Prefs Lookup ---
            if 'Customer_Preferences' not in xls.sheet_names:
                 return {"diet": "Vegetarian", "Customer_Name": "Guest"}
                 
            pref_df = pd.read_excel(xls, 'Customer_Preferences')
            # Safe Clean
            if 'Email' in pref_df.columns:
                 pref_df['Email'] = pref_df['Email'].astype(str).str.strip()
                 user_pref = pref_df[pref_df['Email'] == str(email).strip()]

                 if not user_pref.empty:
                    row = user_pref.iloc[0]
                    return {
                        "diet": row.get('Dietary', 'Pure Veg'),
                        "main_course": row.get('Main Course', 'Paneer Butter Masala'),
                        "sweets": row.get('Sweets', 'Indian Sweets'),
                        "email": email
                    }
        except Exception as e:
            print(f"❌ ProfileService Error: {e}")
            traceback.print_exc()
        
        return {"diet": "Pure Veg", "Customer_Name": "Guest"}

    def save_preferences(self, email: str, preferences: dict):
        """Saves user preferences to Local Excel"""
        try:
            new_row = {
                "Email": email,
                "Dietary": preferences.get("1", "Pure Veg"), # Mapping ID 1 from UI
                "Beverage_Pref": preferences.get("2", ""),
                "Dessert_Pref": preferences.get("3", ""),
                "Comfort_Food": preferences.get("4", ""),
                "Spice_Level": preferences.get("9", "Balanced"),
                "Last_Updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            print(f"💾 Saving Prefs for {email} to Local DB...")
            
            # Read all sheets
            if os.path.exists(self.db_path):
                all_dfs = pd.read_excel(self.db_path, sheet_name=None)
            else:
                all_dfs = {}
                
            if 'Customer_Preferences' in all_dfs:
                # Remove old prefs for this email if exist? Or just append?
                # Usually we want latest. Let's append for history or update?
                # Let's append new row.
                all_dfs['Customer_Preferences'] = pd.concat([all_dfs['Customer_Preferences'], pd.DataFrame([new_row])], ignore_index=True)
            else:
                all_dfs['Customer_Preferences'] = pd.DataFrame([new_row])
            
            with pd.ExcelWriter(self.db_path, engine='openpyxl') as writer:
                for sheet_name, df in all_dfs.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            print(f"✅ Preferences saved for {email}")
            return True

        except Exception as e:
            print(f"❌ Failed to save preferences: {e}")
            traceback.print_exc()
            return False

    def get_interaction_scores(self, customer_id):
        return {"loyalty_score": 85}