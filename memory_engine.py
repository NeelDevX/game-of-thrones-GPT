import json, os
from openai import OpenAI
from config import OPENAI_API_KEY, MODEL_NAME

client = OpenAI(api_key=OPENAI_API_KEY)


def load_long_memory():
    if not os.path.exists("memory.json"):
        return []
    with open("memory.json", "r") as f:
        return json.load(f).get("memory", [])


def save_long_memory(memory_item):
    data = load_long_memory()
    data.append(memory_item)
    with open("memory.json", "w") as f:
        json.dump({"memory": data}, f, indent=4)


def summarize_for_memory(text):
    summary = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "Summarize this into ONE short memory fact."},
            {"role": "user", "content": text},
        ],
    )
    return summary.choices[0].message.content
