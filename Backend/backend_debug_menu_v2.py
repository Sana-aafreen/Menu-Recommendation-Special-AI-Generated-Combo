import requests
import json

URL = "http://127.0.0.1:8002/menu"
PAYLOAD = {"email": "test@example.com"}

try:
    print(f"Fetching {URL}...")
    response = requests.post(URL, json=PAYLOAD)
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ API Response Success")
        print(f"Status: {data.get('status')}")
        
        sections = data.get('menu_sections', {})
        print(f"\n📂 Menu Sections Found: {len(sections)}")
        print(f"Keys: {list(sections.keys())}")
        
        for cat, items in sections.items():
            print(f"\n👉 Section: {cat} ({len(items)} items)")
            if items:
                example = items[0]
                print(f"   Sample Item Keys: {list(example.keys())}")
                print(f"   Sample Name: {example.get('Item_Name') or example.get('name')}")
                print(f"   Sample Price: {example.get('Current_Price') or example.get('price')}")
                print(f"   Sample Is_Veg: {example.get('Is_Veg')} (Type: {type(example.get('Is_Veg'))})")
                print(f"   Sample Dietary_Type: {example.get('Dietary_Type')}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"❌ Exception: {e}")
