import requests
from .create_dashboard import create_dashboard

BASE_URL = "http://localhost:3000/api/card" 
API_KEY = "mb_qtEhHV7Xn7+7T08gq5kGESrWaLNeHvYdDHM0kBshRws=" 


headers = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY
}

def upload_card(card_payloads, collection_id, dashboard_id):
    results = []
    for card_payload in card_payloads:
        card_payload["collection_id"] = collection_id
        card_payload["dashboard_id"] = dashboard_id
        card_res = requests.post(BASE_URL, json=card_payload, headers=headers)
        results.append(f"Card created successfully:, {card_payload['name']}")

    return results

# card_payload = {
#     "name": "Student Enrollment Trend",
#     "description": "Trend of student enrollment over the years.",
#     "collection_id": 2,
#     "display": "line",
#     "dataset_query": {
#       "type": "query",
#       "database": 2,
#       "query": {
#         "source-table": 18,
#         "aggregation": [
#           ["count"]
#         ],
#         "breakout": [
#           ["field", 115]
#         ]
#       }
#     },
#     "visualization_settings": {
#       "graph": {
#         "type": "line",
#         "x-axis": "year",
#         "y-axis": "count"
#       }
#     },
#     "collection_position": None,
#     "parameters": [],
#     "param_values": []
# }
