import requests
import json
import time

BASE_URL = "http://localhost:8002"

def print_result(name, response):
    print(f"--- {name} ---")
    try:
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error parsing response: {response.text}")

def test_auth():
    print(f"Testing Auth Endpoints at {BASE_URL}\n")
    
    # 0. Health Check
    try:
        print("0. Checking Health...")
        resp = requests.get(f"{BASE_URL}/health", timeout=5)
        print_result("Health Check", resp)
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return

    # 1. Test Check User (Not Found)
    print("\n1. Checking non-existent user...")
    resp = requests.post(f"{BASE_URL}/auth/check-user", json={
        "method": "email",
        "value": "nonexistent@example.com"
    }, timeout=10)
    print_result("Check User (Not Found)", resp)

    # 2. Test Signup
    print("\n2. Signing up new user...")
    resp = requests.post(f"{BASE_URL}/auth/signup", json={
        "name": "Test User",
        "email": "test@example.com",
        "mobile": "1234567890"
    })
    print_result("Signup", resp)

    # 3. Test Verify OTP (Success)
    print("\n3. Verifying OTP (Correct)...")
    resp = requests.post(f"{BASE_URL}/auth/verify-otp", json={
        "email": "test@example.com",
        "otp": "123456"
    })
    print_result("Verify OTP (Success)", resp)

    # 4. Test Verify OTP (Failure)
    print("\n4. Verifying OTP (Incorrect)...")
    resp = requests.post(f"{BASE_URL}/auth/verify-otp", json={
        "email": "test@example.com",
        "otp": "000000"
    })
    print_result("Verify OTP (Failure)", resp)

if __name__ == "__main__":
    try:
        test_auth()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to backend. Is it running on port 8002?")
