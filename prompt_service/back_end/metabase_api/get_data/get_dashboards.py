import requests
import os
import json

BASE_URL = "http://localhost:3000"  
API_KEY = "mb_qtEhHV7Xn7+7T08gq5kGESrWaLNeHvYdDHM0kBshRws="     

headers = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY
}

url = f"{BASE_URL}/api/dashboard"
response = requests.get(url, headers=headers)
response.raise_for_status()

dashboards = response.json()
print("📁 Danh sách dashboards:")

for dashboard in dashboards:
    print(f"- ID: {dashboard['id']}, Name: {dashboard['name']}")