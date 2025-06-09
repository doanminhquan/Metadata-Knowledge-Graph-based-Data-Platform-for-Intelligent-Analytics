import os
import json
import requests
from collections import defaultdict

BASE_URL = "http://localhost:3000"
API_KEY = "mb_qtEhHV7Xn7+7T08gq5kGESrWaLNeHvYdDHM0kBshRws="

headers = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY
}

db_tables_map = defaultdict(list)

table_list_url = f"{BASE_URL}/api/table"
table_list_response = requests.get(table_list_url, headers=headers)
table_list_response.raise_for_status()
tables = table_list_response.json()

def simplify_table_detail(raw_detail, table_name, table_id, db_id):
    simplified_fields = [
        {
            "name": field.get("name"),
            "display_name": field.get("display_name"),
            "base_type": field.get("base_type"),
            "semantic_type": field.get("semantic_type"),
            "id": field.get("id"),
        }
        for field in raw_detail.get("fields", [])
        if not field.get("name", "").startswith("_hoodie")  # loại bỏ metadata field
    ]

    return {
        "table_name": table_name,
        "table_id": table_id,
        "db_id": db_id,
        "fields": simplified_fields
    }

for table in tables:
    table_id = table['id']
    table_name = table['name']
    db_id = str(table['db_id'])  

    print(f"\n📄 Table Name: {table_name} (ID: {table_id}), Database Id: {db_id}")

    table_detail_response = requests.get(f"{BASE_URL}/api/table/{table_id}/query_metadata", headers=headers)
    table_detail_response.raise_for_status()
    raw_detail = table_detail_response.json()

    simplified_detail = simplify_table_detail(raw_detail, table_name, table_id, db_id)

    print("📊 Columns:")
    for field in simplified_detail.get('fields', []):
        print(f" - {field['display_name']} ({field['name']}): {field['base_type']}, semantic: {field.get('semantic_type')}")

    output_dir = os.path.join("/data/prompt_service/back_end/metabase_api/prompt_data/tables", db_id)
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, f"{table_name}.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(simplified_detail, f, ensure_ascii=False, indent=2)

    db_tables_map[db_id].append(simplified_detail)

    print(f"✅ Đã lưu file: {output_file}")

for db_id, table_list in db_tables_map.items():
    output_dir = os.path.join("/data/prompt_service/back_end/metabase_api/prompt_data/tables", db_id, "all_tables")
    os.makedirs(output_dir, exist_ok=True)
    tables_file = os.path.join(output_dir, "tables.txt")
    with open(tables_file, "w", encoding="utf-8") as f:
        json.dump(table_list, f, ensure_ascii=False, indent=2)
    print(f"📥 Đã tạo {tables_file}")
