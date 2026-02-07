import requests
import json
import sys

BASE_URL = "http://localhost:8002"

def test_auth():
    print(f"Testing Auth Flow against {BASE_URL}...", flush=True)
    
    # 1. Check User Loop
    print("\n1. Testing /auth/check-user (Phone: 9999999999)...", flush=True)
    try:
        res = requests.post(f"{BASE_URL}/auth/check-user", json={"method": "phone", "value": "9999999999"})
        print(f"Status: {res.status_code}", flush=True)
        print(f"Response: {res.json()}", flush=True)
    except Exception as e:
        print(f"FAILED: {e}", flush=True)

    # 2. Verify OTP Loop
    print("\n2. Testing /auth/verify-otp (OTP: 123456)...", flush=True)
    try:
        res = requests.post(f"{BASE_URL}/auth/verify-otp", json={"mobile": "9999999999", "otp": "123456", "email": "test@user.com"})
        print(f"Status: {res.status_code}", flush=True)
        print(f"Response: {res.json()}", flush=True)
    except Exception as e:
        print(f"FAILED: {e}", flush=True)

if __name__ == "__main__":
    test_auth()
