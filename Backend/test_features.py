import requests
import json
import time

BASE_URL = "http://localhost:8002"
EMAIL = "test_verification@example.com"

def test_offers():
    print(f"\n--- Testing /offers ---")
    try:
        res = requests.get(f"{BASE_URL}/offers")
        print(f"Status: {res.status_code}")
        if res.status_code == 200:
            data = res.json()
            print(f"Offers count: {len(data.get('offers', []))}")
            return True
    except Exception as e:
        print(f"FAIL: {e}")
    return False

def test_save_preferences():
    print(f"\n--- Testing /auth/save-preferences ---")
    payload = {
        "email": EMAIL,
        "preferences": {
            "1": "Pure Veg", # Diet
            "2": "Coke",     # Bev
            "9": "Spicy"     # Spice
        }
    }
    try:
        res = requests.post(f"{BASE_URL}/auth/save-preferences", json=payload)
        print(f"Status: {res.status_code}")
        print(f"Response: {res.json()}")
        return res.status_code == 200
    except Exception as e:
        print(f"FAIL: {e}")
    return False

def test_menu_personalization():
    print(f"\n--- Testing /menu (Personalization) ---")
    # Should reflect "Pure Veg" from above
    payload = {"customer_email": EMAIL}
    try:
        res = requests.post(f"{BASE_URL}/menu", json=payload)
        print(f"Status: {res.status_code}")
        if res.status_code == 200:
            data = res.json()
            menu = data.get('menu', {})
            sections = menu.get('menu_sections', {})
            print(f"Sections found: {list(sections.keys())}")
            print(f"User Diet Detected: {menu.get('user_diet')}")
            return True
    except Exception as e:
        print(f"FAIL: {e}")
    return False

def test_recommendations():
    print(f"\n--- Testing /item-addons (Pairing) ---")
    # Assuming Item matches one in DB, e.g., a Biryani ID or Name
    # Need a valid Item ID. Let's try to get one from menu first
    try:
        # Get an item ID first
        menu_res = requests.post(f"{BASE_URL}/menu", json={"customer_email": EMAIL}).json()
        sections = menu_res['menu']['menu_sections']
        item_id = "101" # Default/Fallback
        
        # Try to find a real ID
        for cat, items in sections.items():
            if items:
                item_id = items[0]['Item_ID']
                print(f"Using Item ID: {item_id} ({items[0]['Item_Name']})")
                break
        
        payload = {
            "customer_email": EMAIL,
            "item_id": str(item_id)
        }
        res = requests.post(f"{BASE_URL}/item-addons", json=payload)
        print(f"Status: {res.status_code}")
        if res.status_code == 200:
            data = res.json()
            recs = data.get('smart_recommendations', {})
            print(f"AI Pitch: {recs.get('ai_pitch')}")
            print(f"Add-ons count: {len(recs.get('add_ons', []))}")
            return True
    except Exception as e:
        print(f"FAIL: {e}")
    return False

if __name__ == "__main__":
    if test_save_preferences():
        test_menu_personalization()
    test_offers()
    test_recommendations()
