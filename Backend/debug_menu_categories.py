import requests
import json

BASE_URL = "http://127.0.0.1:8002"

def check_categories():
    print("Fetching Menu Categories...")
    try:
        # /menu is a POST request requiring EmailRequest model
        payload = {"customer_email": "guest@dineiq.com"} 
        # Note: Frontend uses /menu endpoint which maps to get_smart_menu
        
        res = requests.post(f"{BASE_URL}/menu", json=payload)
        
        if res.status_code == 200:
            data = res.json()
            if 'menu' in data and 'menu_sections' in data['menu']:
                sections = data['menu']['menu_sections']
                print(f"✅ Found {len(sections)} sections:")
                for section_name, items in sections.items():
                    print(f"   - {section_name} ({len(items)} items)")
                    if len(items) > 0:
                        # Print first item's category to see if it matches
                        first_item = items[0]
                        cat = first_item.get('Item_Category', 'N/A')
                        print(f"     Sample Category: {cat}")
            else:
                print("❌ 'menu_sections' not found in response")
                print(json.dumps(data, indent=2))
        else:
            print(f"❌ /menu failed: {res.status_code}")
            print(res.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_categories()
