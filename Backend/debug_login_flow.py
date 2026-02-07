import requests
import json
import random

BASE_URL = "http://localhost:8002"

def debug_login():
    print("--- 1. Testing /auth/check-user (User Existence) ---")
    # Case A: Existing User ?
    # Let's try to check a user we expect to be there or not.
    # We will try a known user if we can, or just see the response structure.
    
    payload = {
        "method": "email",
        "value": "sumbu@example.com" # Just a test email
    }
    
    try:
        print(f"Sending POST to {BASE_URL}/auth/check-user with {payload}")
        res = requests.post(f"{BASE_URL}/auth/check-user", json=payload)
        print(f"Status: {res.status_code}")
        print(f"Response: {res.text}")
    except Exception as e:
        print(f"ERROR: {e}")

    print("\n--- 2. Testing /auth/signup (New User) ---")
    # Case B: Signup
    new_email = f"debug_{random.randint(1000,9999)}@test.com"
    payload = {
        "name": "Debug User",
        "email": new_email,
        "mobile": str(random.randint(9000000000, 9999999999))
    }
    
    try:
        print(f"Sending POST to {BASE_URL}/auth/signup with {payload}")
        res = requests.post(f"{BASE_URL}/auth/signup", json=payload)
        print(f"Status: {res.status_code}")
        print(f"Response: {res.text}")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    debug_login()
