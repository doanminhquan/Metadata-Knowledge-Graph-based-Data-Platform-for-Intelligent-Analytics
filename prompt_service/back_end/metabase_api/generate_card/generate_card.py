import requests
import os
import json
from openai import OpenAI
from .upload_card import upload_card
from .create_dashboard import create_dashboard

def get_llm():
    api_key = ""

    client = OpenAI(
        api_key = api_key,
    )

    return client

def get_extra_information():
    with open("/data/prompt_service/back_end/metabase_api/prompt_data/tables/2/all_tables/tables.txt", "r", encoding="utf-8") as f:
        table_information = f.read()

    with open("/data/prompt_service/back_end/metabase_api/prompt_data/tables/3/all_tables/tables.txt", "r", encoding="utf-8") as f:
        aggregated_table_information = f.read()

    with open("/data/prompt_service/back_end/metabase_api/prompt_data/cards/cards.txt", "r", encoding="utf-8") as f:
        card_sample = f.read()

    with open("/data/prompt_service/back_end/metabase_api/prompt_data/metabase_format.txt", "r", encoding="utf-8") as f:
        metabase_format = f.read()

    with open("/data/prompt_service/back_end/metabase_api/prompt_data/request_sample.txt", "r", encoding="utf-8") as f:
        request_sample = f.read()

    return table_information, aggregated_table_information, card_sample, metabase_format, request_sample


def generate_card_prompt(llm_client, table_information, 
                    aggregated_table_information, card_sample, 
                    metabase_format, request_sample, user_prompt):

    prompt_content = f"""
        I want to generate multiple Metabase visualizations (cards) programmatically using the Metabase API.

        What I will provide:
        1. Table Information: Schema and structure of the original database tables: {table_information}
        2. Sample Cards: JSON definitions of sample visualizations/cards that can serve as templates or references: {card_sample}
        3. Metabase Format Guidelines: The expected format for creating cards using the Metabase API: {metabase_format}
        4. Working Sample JSONs: Successfully used JSON request bodies that can serve as a base pattern: {request_sample}

        User Request: {user_prompt}

        Your Task:
        - Generate a list of new JSON card definitions that fulfill the user's request.
        - {{For each card: Create a short, general explanation describing what information the card presents and how it is relevant to the request. Explanations must avoid technical details and be written in plain language (e.g., "This chart shows student enrollment over the years...").}}
        - {{Add a field called "dashboard_name" for cards. This should be a short and relevant name suggesting which dashboard the cards belongs to, based on the cards’ purpose and context. The name should be practical, user-friendly, and aligned with the user's request.}}
        - If possible, include cards using multiple sources across the set.

        Output Requirements:
        - Return a Python-style dictionary with three keys: "cards", "explanation", and "dashboard_name":
        {{
            "cards": [...],
            "explanation": ["{{visualization_name(must be English)}} - ...", "{{visualization_name(must be English)}} - ...", ..., {{Summary(Overall information of the dashboard)}} - ...],
            "dashboard_name": "..."
        }}
        - Do not include any comments or annotations (such as //, #, or extra field notes) in the JSON output.
        - Ensure the explanation and dashboard_name lists are the same length and order as the cards list.
        - The language of the explanation (except for visualization_name) must match the language of the user_prompt.
        - Do not use SQL queries. Use only Metabase native format, based on the structure of card_sample.
        - Do not wrap the output in triple backticks or label it as a code block.
        - The output must be directly parsable by Python’s json.loads().
    """

    model = "gpt-4o-mini"

    response = llm_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt_content}
        ],
    )

    output = response.choices[0].message.content

    output_dir = "/data/prompt_service/back_end/metabase_api/generate_card/cards_results"
    
    file_list = [f for f in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, f))]
    file_count = len(file_list)

    new_filename = f"{file_count + 1}.txt"
    output_path = os.path.join(output_dir, new_filename)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"Card definitions saved to: {output_path}")

    return output

    
def handle_user_request(user_prompt):
    table_information, aggregated_table_information, card_sample, metabase_format, request_sample = get_extra_information()
    llm = get_llm()
    output = generate_card_prompt(
        llm_client = llm,
        table_information = table_information, 
        aggregated_table_information = aggregated_table_information,
        card_sample = card_sample,
        metabase_format = metabase_format,
        request_sample = request_sample,
        user_prompt = user_prompt 
    )

    output = json.loads(output)
    card_payloads = output["cards"]
    explanations = output["explanation"]
    dashboard_name = output["dashboard_name"]
    dashboard_id = create_dashboard(dashboard_name)["id"]
    print("Uploaded card", upload_card(card_payloads, 7, dashboard_id))
    return explanations

# Aggregate some information

# handle_user_request("Generate a visualize that shows the trend of student enrollment over the years.")

