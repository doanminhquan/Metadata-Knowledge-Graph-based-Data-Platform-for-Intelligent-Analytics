import requests

BASE_URL = "http://localhost:3000/api/dashboard" 
API_KEY = "mb_qtEhHV7Xn7+7T08gq5kGESrWaLNeHvYdDHM0kBshRws=" 


headers = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY
}


def create_dashboard(name):
    dashboard_payload = {
        "collection_id": 7,
        "name": name,
        "cache_ttl": 1,
        "description": "",
    }

    res = requests.post(BASE_URL, json=dashboard_payload, headers=headers)
    res.raise_for_status()
    return res.json()
