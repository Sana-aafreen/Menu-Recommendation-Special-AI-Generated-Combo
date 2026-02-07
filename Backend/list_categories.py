import pandas as pd
import os

DB_PATH = "services/DineIQ_DB.xlsx"

def list_cats():
    if not os.path.exists(DB_PATH):
        print("DB not found")
        return

    try:
        df = pd.read_excel(DB_PATH, sheet_name='Menu')
        # Filter active
        valid_status = ['ACTIVE', 'YES', 'TRUE', '1', 'AVAILABLE', 'Y']
        active = df[df['Is_Active'].astype(str).str.upper().str.strip().isin(valid_status)]
        
        cats = active['Item_Category'].astype(str).str.strip().unique()
        print("CATEGORIES_START")
        for c in sorted(cats):
            print(c)
        print("CATEGORIES_END")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_cats()
