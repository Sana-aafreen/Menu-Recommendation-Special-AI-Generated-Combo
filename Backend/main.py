import os
import sys
import pandas as pd
import traceback
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from groq import Groq
from dotenv import load_dotenv

# Path setup for custom agents
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from agents.menu_agent import MenuAgent
from agents.recommendation_agent import RecommendationAgent
from agents.pricing_agent import PricingAgent

load_dotenv()
app = FastAPI(title="DineIQ Enterprise - Smart Restaurant Core")

# --- 1. CONFIGURATION ---
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# Windows Specific Excel Path
DB_PATH = r"C:\Users\sumbu\Downloads\DineIQ-pre_main\DineIQ-pre_main\Backend\services\DineIQ_DB.xlsx"

# --- 2. DATABASE UTILITY ---
def load_db():
    """Real-time Excel sync utility"""
    try:
        data = {
            'menu': pd.read_excel(DB_PATH, sheet_name='Menu').fillna(0),
            'orders': pd.read_excel(DB_PATH, sheet_name='Orders').fillna(0),
            'items': pd.read_excel(DB_PATH, sheet_name='Order_Items').fillna(0),
            'prefs': pd.read_excel(DB_PATH, sheet_name='Customer_Preferences').fillna(0),
            'auth': pd.read_excel(DB_PATH, sheet_name='Customer_Auth').fillna(0)
        }
        # Standardize Strings
        for name in data:
            df = data[name]
            cols_to_strip = ['Item_ID', 'Order_ID', 'Customer_ID', 'Is_Active', 'Customer_Email']
            for col in cols_to_strip:
                if col in df.columns:
                    df[col] = df[col].astype(str).str.strip()
        return data
    except Exception as e:
        print(f"❌ Critical DB Error: {e}")
        return None

# --- 3. API MODELS ---
class EmailRequest(BaseModel):
    customer_email: str

class AddonRequest(BaseModel):
    customer_email: str
    item_id: str

class StrategyRequest(BaseModel):
    customer_email: str
    cart_items: List[Dict]

# --- 4. ENDPOINTS ---

@app.post("/menu")
async def get_menu(req: EmailRequest):
    db = load_db()
    user = db['auth'][db['auth']['Customer_Email'] == req.customer_email]
    cust_id = str(user.iloc[0]['Customer_ID']) if not user.empty else None
    
    worker = MenuAgent(db['menu'], db['orders'], db['items'])
    return {"menu": worker.get_smart_menu(cust_id)}

@app.post("/item-addons")
async def get_addons(req: AddonRequest):
    db = load_db()
    worker = RecommendationAgent(db['menu'], db['prefs'], db['items'], db['orders'], client)
    recs = worker.get_recommendations(req.customer_email, req.item_id)
    return {"smart_recommendations": recs}

@app.post("/checkout")
async def checkout(req: StrategyRequest):
    db = load_db()
    user = db['auth'][db['auth']['Customer_Email'] == req.customer_email]
    cust_id = str(user.iloc[0]['Customer_ID']) if not user.empty else "Guest"
    order_count = len(db['orders'][db['orders']['Customer_ID'] == cust_id])
    
    subtotal = sum(float(i.get('Current_Price', i.get('price', 0))) for i in req.cart_items)
    worker = PricingAgent(DB_PATH)
    return worker.get_pricing_strategy(subtotal, order_count, req.cart_items)

@app.post("/recommendation-strategy")
async def place_order(req: StrategyRequest):
    """Zomato-style Permanent Checkout with Excel Logging"""
    try:
        db = load_db()
        user = db['auth'][db['auth']['Customer_Email'] == req.customer_email]
        if user.empty: raise HTTPException(status_code=404, detail="User not found")
        
        cust_id = user.iloc[0]['Customer_ID']
        cust_name = user.iloc[0]['Customer_Name']
        new_order_id = f"Ord_{datetime.now().strftime('%m%d%H%M%S')}"
        total_price = sum(float(i.get('Current_Price', i.get('price', 0))) for i in req.cart_items)

        # 1. New Order Entry
        new_order_df = pd.DataFrame([{
            "Order_ID": new_order_id,
            "Customer_ID": cust_id,
            "Customer_Name": cust_name,
            "Order_Price": total_price,
            "Order_Created_DateTime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "Order_Status": "COMPLETED"
        }])

        # 2. New Order Items Entry
        new_items = []
        for i in req.cart_items:
            new_items.append({
                "Order_Item_ID": f"Itm_{datetime.now().strftime('%f')}",
                "Order_ID": new_order_id,
                "Item_ID": i.get('Item_ID'),
                "Item_Name": i.get('Item_Name'),
                "Item_Quantity": 1,
                "Item_Price": i.get('Current_Price', i.get('price', 0))
            })
        new_items_df = pd.DataFrame(new_items)

        # 3. SAVE EVERYTHING TO EXCEL
        with pd.ExcelWriter(DB_PATH, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            # Update Orders
            pd.concat([db['orders'], new_order_df], ignore_index=True).to_excel(writer, sheet_name='Orders', index=False)
            # Update Order Items
            pd.concat([db['items'], new_items_df], ignore_index=True).to_excel(writer, sheet_name='Order_Items', index=False)
            # Keep other sheets intact
            db['menu'].to_excel(writer, sheet_name='Menu', index=False)
            db['prefs'].to_excel(writer, sheet_name='Customer_Preferences', index=False)
            db['auth'].to_excel(writer, sheet_name='Customer_Auth', index=False)

        print(f"✅ Order {new_order_id} saved successfully!")
        return {"status": "success", "order_id": new_order_id, "total": total_price}

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Port 8002 is matched with your Streamlit script
    uvicorn.run(app, host="127.0.0.1", port=8002)