import requests
import os
import json

BASE_URL = "http://localhost:3000"  
API_KEY = "mb_qtEhHV7Xn7+7T08gq5kGESrWaLNeHvYdDHM0kBshRws="     

headers = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY
}

url = f"{BASE_URL}/api/card"
response = requests.get(url, headers=headers)
response.raise_for_status()

collections = response.json()

print("📁 Danh sách cards:")
cards = []
for col in collections:
    collection_id = col['collection']['id']
    
    if collection_id == 2:
        cards.append(col)

output_dir = f"/data/prompt_service/back_end/metabase_api/prompt_data/cards/"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "cards.txt")
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(cards, f, ensure_ascii=False, indent=2)
print(f"✅ Đã lưu file: {output_file}")