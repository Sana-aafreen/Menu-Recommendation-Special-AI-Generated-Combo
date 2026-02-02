import pandas as pd
import os

class ProfileService:
    def __init__(self):
        # Updated to your specific path
        self.db_path = r"C:\Users\sumbu\Downloads\DineIQ-pre_main\DineIQ-pre_main\Backend\services\DineIQ_DB.xlsx"

    def get_preferences(self, customer_id):
        """Links Auth data with Preferences using Email as the bridge"""
        try:
            if not os.path.exists(self.db_path):
                return {"diet": "Vegetarian", "Customer_Name": "Guest"}

            # 1. Auth Sheet se Customer details lo
            auth_df = pd.read_excel(self.db_path, sheet_name="Customer_Auth")
            auth_df['Customer_ID'] = auth_df['Customer_ID'].astype(str).str.strip()
            user_auth = auth_df[auth_df['Customer_ID'] == str(customer_id).strip()]

            if user_auth.empty:
                return {"diet": "Vegetarian", "Customer_Name": "Guest"}

            email = user_auth.iloc[0].get('Customer_Email')
            name = user_auth.iloc[0].get('Customer_Name', 'Guest')

            # 2. Preferences Sheet se mapping (Bridge: Email)
            pref_df = pd.read_excel(self.db_path, sheet_name="Customer_Preferences")
            user_pref = pref_df[pref_df['Email'].str.strip() == str(email).strip()]

            if not user_pref.empty:
                row = user_pref.iloc[0]
                return {
                    "diet": row.get('Dietary', 'Pure Veg'),
                    "main_course": row.get('Main Course', 'Paneer Butter Masala'),
                    "sweets": row.get('Sweets', 'Indian Sweets'),
                    "Customer_Name": name,
                    "email": email
                }
        except Exception as e:
            print(f"❌ ProfileService Error: {e}")
        
        return {"diet": "Pure Veg", "Customer_Name": "Guest"}

    def get_interaction_scores(self, customer_id):
        # Can be linked to 'Customer_Insights' sheet later
        return {"loyalty_score": 85}