import requests
import json
import random

BASE_URL = "http://localhost:8002"
TEST_EMAIL = f"migtest_{random.randint(1000,9999)}@example.com"
TEST_PHONE = str(random.randint(9000000000, 9999999999))

def verify_migration():
    print(f"🚀 Starting Google Sheets Migration Test against {BASE_URL}...", flush=True)
    print(f"👤 Test User: {TEST_EMAIL} / {TEST_PHONE}", flush=True)

    # 1. Signup (Write to Cloud)
    print("\n[1] Testing Signup (Cloud Write)...", flush=True)
    try:
        payload = {"name": "Migration Tester", "email": TEST_EMAIL, "mobile": TEST_PHONE}
        res = requests.post(f"{BASE_URL}/auth/signup", json=payload)
        print(f"Status: {res.status_code}", flush=True)
        print(f"Response: {res.json()}", flush=True)
        if res.json().get("status") == "otp_sent":
            print("✅ Signup initiated successfully.", flush=True)
        else:
            print("❌ Signup failed.", flush=True)
    except Exception as e:
        print(f"FAILED: {e}", flush=True)

    # 2. Complete Registration via OTP (Triggers register_user -> Cloud POST)
    print("\n[2] Verifying OTP & Registering (Cloud POST)...", flush=True)
    try:
        # Note: verify-otp logic now calls auth_service.register_user
        payload = {"email": TEST_EMAIL, "mobile": TEST_PHONE, "otp": "123456"}
        res = requests.post(f"{BASE_URL}/auth/verify-otp", json=payload)
        print(f"Status: {res.status_code}", flush=True)
        print(f"Response: {res.json()}", flush=True)
        if res.json().get("status") == "ok":
            print("✅ Registration confirmed via Cloud.", flush=True)
        else:
            print("❌ Registration failed.", flush=True)
    except Exception as e:
        print(f"FAILED: {e}", flush=True)

    # 3. Check User (Read from Cloud)
    print("\n[3] Checking User Existence (Cloud Read)...", flush=True)
    try:
        payload = {"method": "email", "value": TEST_EMAIL}
        res = requests.post(f"{BASE_URL}/auth/check-user", json=payload)
        print(f"Status: {res.status_code}", flush=True)
        print(f"Response: {res.json()}", flush=True)
        if res.json().get("status") == "exists":
            print("✅ User found in Cloud DB!", flush=True)
        else:
            print("❌ User NOT found (Read/Write latency or failure).", flush=True)
    except Exception as e:
        print(f"FAILED: {e}", flush=True)

    # 4. Fetch Menu (Read Menu Sheet from Cloud)
    print("\n[4] Fetching Menu (Cloud Read)...", flush=True)
    try:
        payload = {"customer_email": TEST_EMAIL}
        res = requests.post(f"{BASE_URL}/menu", json=payload)
        print(f"Status: {res.status_code}", flush=True)
        if res.status_code == 200:
            data = res.json()
            items = len(data.get("menu", {}).get("menu_items", []))
            print(f"✅ Menu Fetched! Items count: {items}", flush=True)
        else:
            print(f"❌ Menu Fetch Failed: {res.text}", flush=True)
    except Exception as e:
        print(f"FAILED: {e}", flush=True)

if __name__ == "__main__":
    verify_migration()
