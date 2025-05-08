import os
import requests

API_KEY = os.getenv("GEMINI_API_KEY")
ENDPOINT = "https://api.gemini.google.com/generate"

def generate_answer(input_text: str) -> str:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "input": input_text
    }

    response = requests.post(ENDPOINT, headers=headers, json=payload)
    data = response.json()
    return data.get("output", "No output from Gemini")
