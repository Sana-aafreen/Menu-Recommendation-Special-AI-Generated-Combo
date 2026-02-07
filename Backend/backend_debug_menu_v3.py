import requests
import json

URL = "http://127.0.0.1:8002/menu"

# Found in main.py: req.customer_email
print("--- Attempt 2: Correct Key ---")
PAYLOAD = {"customer_email": "test@example.com"}

try:
    response = requests.post(URL, json=PAYLOAD)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("\n✅ API Response Success")
        print(f"Status: {data.get('status')}")
        
        # Backend returns {"menu": {"menu_sections": ...}} based on line 106
        # return {"menu": worker.get_smart_menu(...)}
        
        menu_wrapper = data.get('menu', {})
        if not menu_wrapper:
             print("⚠️ 'menu' key missing in response!")
             print(json.dumps(data, indent=2))
        
        sections = menu_wrapper.get('menu_sections', {})
        print(f"\n📂 Menu Sections Found: {len(sections)}")
        print(f"Keys: {list(sections.keys())}")
        
        for cat, items in sections.items():
            print(f"\n👉 Section: {cat} ({len(items)} items)")
            if items:
                example = items[0]
                print(f"   Sample Item Keys: {list(example.keys())}")
                print(f"   Sample Name: {example.get('Item_Name') or example.get('name')}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"❌ Exception: {e}")
