import requests
from create_dashboard import create_dashboard

BASE_URL = "http://localhost:3000/api/card" 
API_KEY = "mb_qtEhHV7Xn7+7T08gq5kGESrWaLNeHvYdDHM0kBshRws=" 


headers = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY
}

card_payload = {
    "name": "Student Enrollment Trend",
    "description": "Trend of student enrollment over the years.",
    "collection_id": 2,
    "display": "line",
    "dataset_query": {
      "type": "query",
      "database": 2,
      "query": {
        "source-table": 18,
        "aggregation": [
          ["count"]
        ],
        "breakout": [
          ["field", 115]
        ]
      }
    },
    "visualization_settings": {
      "graph": {
        "type": "line",
        "x-axis": "year",
        "y-axis": "count"
      }
    },
    "collection_position": None,
    "parameters": [],
    "param_values": []
}
card_payload["collection_id"] = 7
card_payload["dashboard_id"] = 26

card_res = requests.post(BASE_URL, json=card_payload, headers=headers)
print("Card created successfully:", card_res.content)
