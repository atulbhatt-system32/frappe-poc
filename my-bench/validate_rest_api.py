import requests
import json

API_KEY = "c5d580d52b4b00a"
API_SECRET = "ed31b8046fcb7d7"
BASE_URL = "http://mysite.localhost:8000/api/resource"

headers = {
    "Authorization": f"token {API_KEY}:{API_SECRET}",
    "Content-Type": "application/json"
}

def validate_api():
    print("--- 1. Testing Authorized Read (Test Entity) ---")
    # Get all Test Entities
    res = requests.get(f"{BASE_URL}/Test Entity", headers=headers)
    print(f"Status: {res.status_code}")
    if res.status_code == 200:
        data = res.json().get("data", [])
        print(f"Found {len(data)} records.")
        if data:
            name = data[0]['name']
            # Get specific record
            res_single = requests.get(f"{BASE_URL}/Test Entity/{name}", headers=headers)
            print(f"Read Single Record ({name}): {res_single.status_code}")
    
    print("\n--- 2. Testing Authorized Create (Test Entity) ---")
    payload = {
        "doctype": "Test Entity",
        "field_a": 10,
        "field_b": 50,
        "field_c": 500  # Though UI calculated, API usually allows setting (unless validated on server)
    }
    res_create = requests.post(f"{BASE_URL}/Test Entity", headers=headers, json=payload)
    print(f"Create Status: {res_create.status_code}")
    if res_create.status_code == 200:
        print(f"New Record Name: {res_create.json()['data']['name']}")

    print("\n--- 3. Testing Unauthorized Read (Sales Invoice) ---")
    res_unauth = requests.get(f"{BASE_URL}/Sales Invoice", headers=headers)
    print(f"Status (Expected 403): {res_unauth.status_code}")
    if res_unauth.status_code == 403:
        print("Success: Unauthorized access blocked.")
    else:
        print("Warning: Unauthorized access was NOT blocked as expected.")

if __name__ == "__main__":
    validate_api()
