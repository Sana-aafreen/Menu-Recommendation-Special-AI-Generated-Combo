import requests
import json

BASE_URL = "http://localhost:8002"
EMAIL = "test_debug@example.com"

def debug_menu():
    print(f"Fetching menu for {EMAIL}...")
    try:
        res = requests.post(f"{BASE_URL}/menu", json={"customer_email": EMAIL})
        if res.status_code == 200:
            data = res.json()
            sections = data.get('menu', {}).get('menu_sections', {})
            print("--- SECTIONS FOUND ---")
            for key in sections.keys():
                print(f"- '{key}' (Count: {len(sections[key])})")
                if len(sections[key]) > 0:
                    print(f"  Sample Item Category: {sections[key][0].get('Item_Category')}")
        else:
            print(f"Error: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"Connection Failed: {e}")

if __name__ == "__main__":
    debug_menu()
