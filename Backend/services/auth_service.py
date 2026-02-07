import pandas as pd
import random
import os
import traceback

class AuthService:
    def __init__(self, db_path):
        self.db_path = db_path

    def authenticate(self, email, password):
        # Temporary logic for testing
        if email and password:
            return {"Customer_ID": "Cust_0001", "Customer_Name": "Guest User"}
        return None

    def register_user(self, name, email, mobile):
        """Registers a new user to Local Excel"""
        try:
            print(f"Attempting to register: {email}")
            
            if not os.path.exists(self.db_path):
                 print(f"❌ DB not found for registration: {self.db_path}")
                 return False

            # 1. Check if user exists (Read from Local)
            # We need to read all sheets anyway to write back safely
            all_dfs = pd.read_excel(self.db_path, sheet_name=None)
            
            auth_df = all_dfs.get('Customer_Auth', pd.DataFrame())
            
            if not auth_df.empty and 'Customer_Email' in auth_df.columns:
                 if email in auth_df['Customer_Email'].astype(str).str.strip().values:
                     print(f"User {email} already exists.")
                     return True
                         
            # 2. Create New User Payload
            new_id = f"Cust_{random.randint(10000, 99999)}"
            new_user = {
                "Customer_ID": new_id,
                "Customer_Name": name or "New User",
                "Customer_Email": email,
                "Customer_Phone": mobile,
                "Is_Active": True
            }
            
            # 3. Append to DF
            if not auth_df.empty:
                updated_auth_df = pd.concat([auth_df, pd.DataFrame([new_user])], ignore_index=True)
            else:
                updated_auth_df = pd.DataFrame([new_user])
                
            all_dfs['Customer_Auth'] = updated_auth_df

            # 4. Write to Excel
            print(f"💾 Registering {email} (ID: {new_id}) to Local DB...")
            with pd.ExcelWriter(self.db_path, engine='openpyxl') as writer:
                for sheet_name, df in all_dfs.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            print(f"✅ User registered successfully!")
            return True

        except Exception as e:
            print(f"❌ Registration Error: {e}")
            traceback.print_exc()
            return False