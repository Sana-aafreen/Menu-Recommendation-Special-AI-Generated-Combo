import requests
import json

# User provided URL - usually needs /exec at the end if not present
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbziwt_310-tDnkzPTpgbgW89M6jxjDXQVbRIn7k-JzBiezCzoDcjhPjDDbZDjVrLf4N5w/exec"

def probe_api():
    print(f"Probing: {APPS_SCRIPT_URL}")
    
    # 1. Try GET (Read Data)
    try:
        print("\n--- GET Request ---")
        response = requests.get(APPS_SCRIPT_URL)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            try:
                data = response.json()
                print("Response JSON Keys:", data.keys())
                # Preview one sheet if possible
                if 'Menu' in data:
                    print(f"Menu Items Count: {len(data['Menu'])}")
                    print("Sample Item:", data['Menu'][0])
                elif 'data' in data:
                    # Some scripts return {data: {Sheet1: ...}}
                    print("Data Keys:", data['data'].keys())
            except:
                print("Response Text (Not JSON):", response.text[:200])
        else:
            print("Error Response:", response.text)
    except Exception as e:
        print(f"GET Failed: {e}")

    # 2. Try Simple POST (Check if it accepts writes)
    # Sending a dummy action usually used in such scripts
    try:
        print("\n--- POST Request (Probe) ---")
        payload = {"action": "test", "sheet": "Logs", "data": {"test": "ping"}}
        response = requests.post(APPS_SCRIPT_URL, json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}")
    except Exception as e:
        print(f"POST Failed: {e}")

if __name__ == "__main__":
    probe_api()
