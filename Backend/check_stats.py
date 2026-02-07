import requests

BASE_URL = "http://localhost:8002"

def check_stats():
    try:
        res = requests.get(f"{BASE_URL}/debug/stats")
        print(res.json())
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_stats()
