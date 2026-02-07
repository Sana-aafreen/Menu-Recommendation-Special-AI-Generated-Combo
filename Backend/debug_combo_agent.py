import pandas as pd
import sys
import os
from dotenv import load_dotenv

# Add parent directory to path to import backend modules
from agents.combo_agent import ComboAgent

def load_local_db():
    try:
        # Adjust path to your actual Excel file
        db_path = os.path.join(os.path.dirname(__file__), "services", "DineIQ_DB.xlsx")
        print(f"Loading DB from: {db_path}")
        return pd.read_excel(db_path, sheet_name=None)
    except Exception as e:
        print(f"Error loading DB: {e}")
        return None

def debug_combos():
    db = load_local_db()
    if db is None:
        return

    # Initialize Groq for testing
    load_dotenv()
    from groq import Groq
    
    api_key = os.getenv("GROQ_API_KEY")
    client = Groq(api_key=api_key) if api_key else None
    print(f"Groq Client Initialized: {client is not None}")

    menu_df = db['Menu']
    agent = ComboAgent(menu_df, client)

    with open("debug_summary.txt", "w", encoding="utf-8") as f:
        f.write(f"Total Active Items: {len(agent.active_items)}\n")
        
        f.write("\n--- Generating Combos with AI & User Context ---\n")
        
        # Simulating User Context
        orders_data = {
            'User_Email': ['test@user.com'] * 5,
            'Item_Name': ['Spicy Chicken', 'Butter Naan', 'Coke', 'Chicken Biryani', 'Paneer Tikka'],
            'Category': ['Gravy', 'Bread', 'Beverage', 'Rice', 'Starter']
        }
        orders_df = pd.DataFrame(orders_data)
        
        combos = agent.generate_combos(
            num_combos=5, 
            user_email='test@user.com',
            orders_df=orders_df
        )
        f.write(f"\nGenerated {len(combos)} combos:\n")
        for c in combos:
            f.write(f"- {c['Item_Name']}\n")
            f.write(f"  Desc: {c['Item_Description']}\n")
            f.write(f"  Price: {c['Current_Price']} (Save {c['Savings']})\n")
            f.write(f"  Stats: {c.get('Rating')}⭐ ({c.get('Order_Count')} orders)\n")
            f.write(f"  Personalized: {c.get('Is_Personalized')}\n")
            f.write(f"  Insight: {c.get('Insight')}\n")

if __name__ == "__main__":
    debug_combos()
