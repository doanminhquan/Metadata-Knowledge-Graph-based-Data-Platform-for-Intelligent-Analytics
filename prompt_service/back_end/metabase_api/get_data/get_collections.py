import requests

BASE_URL = "http://localhost:3000"  
API_KEY = "mb_qtEhHV7Xn7+7T08gq5kGESrWaLNeHvYdDHM0kBshRws="     

headers = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY
}

url = f"{BASE_URL}/api/collection"
response = requests.get(url, headers=headers)
response.raise_for_status()

collections = response.json()

print("📁 Danh sách collections:")
for col in collections:
    print(f"- ID: {col['id']}, Name: {col['name']}")
