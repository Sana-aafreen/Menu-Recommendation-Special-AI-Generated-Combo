import requests
import json

API_URL = "http://127.0.0.1:8002/menu"

def test_combo_generation():
    print("Testing Combo Generation...")
    
    payload = {"customer_email": "test@example.com"}
    
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            data = response.json()
            menu = data.get('menu', {})
            
            # INSPECT CATEGORIES
            items = menu.get('menu_items', []) # Or however it's structured in response
            # Response structure of /menu is {"menu": {"menu_sections": {...}, "items": [...]?}} 
            # Actually MenuAgent returns a dict with 'menu_sections'.
            # We need to find where the raw items are or iterate sections.
            
            categories = set()
            section_dict = menu.get('menu_sections', {})
            print(f"DEBUG: Found sections: {list(section_dict.keys())}")
            
            for section, items in section_dict.items():
                for i in items:
                    categories.add(i.get('Item_Category', 'Unknown'))
            
            print(f"DEBUG: Available Categories: {sorted(list(categories))}")
            
            sections = menu.get('menu_sections', {})
            combos = sections.get('Combos', [])
            
            print(f"\n✅ Fetched {len(combos)} Combos:")
            
            for i, c in enumerate(combos, 1):
                print(f"{i}. {c.get('Item_Name')} (Type: {c.get('Item_Category')})")
                print(f"   Items: {c.get('Item_Description')}")
                print(f"   Price: {c.get('Current_Price')} | Discount: {c.get('Discount_Percent')}%")
                print("-" * 40)

        else:
            print(f"❌ API Error: {response.text}")

    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    test_combo_generation()
