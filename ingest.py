import requests
import os
from datetime import datetime


def get_fact():
    url = "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("text")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching fact: {e}")
        return None
    
    
def get_facts(n=10):
    facts = []
    for _ in range(n):
        fact = get_fact()
        if fact:
            facts.append(fact)
    return facts


def save_facts_to_txt(facts):
    if not facts:
        print("No facts to save.")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    folder_path = "data/raw"
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, f"facts_{timestamp}.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        for fact in facts:
            f.write(fact + "\n")  # each fact on its own line

    print(f"{len(facts)} facts saved to '{file_path}'")
    if os.path.getsize(file_path) > 0:
        print("Ingestion successful!")
    return file_path
