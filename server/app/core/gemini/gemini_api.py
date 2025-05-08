# app/core/gemini/gemini_api.py
import os
import requests

def call_gemini(input_text: str):
    api_key = os.getenv("GEMINI_API_KEY")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    res = requests.post(
        "https://api.gemini.google.com/generate",
        headers=headers,
        json={"input": input_text}
    )
    return res.json().get("output", "No response.")
