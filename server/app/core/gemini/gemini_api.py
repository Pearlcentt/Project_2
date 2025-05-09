import os
import google.generativeai as genai
from dotenv import load_dotenv
from typing import List, Optional

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set")

genai.configure(api_key=GOOGLE_API_KEY)


def call_gemini(prompt: str) -> str:
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        response = model.generate_content(prompt)
        
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return f"Error generating response: {str(e)}"


def format_prompt_with_context(query: str, relevant_docs: List[str]) -> str:
    context = "\n\n".join([f"Document {i+1}:\n{doc}" for i, doc in enumerate(relevant_docs)])
    
    prompt = f"""
    Use the following pieces of context to answer the user's question. 
    If you don't know the answer based on the context, just say that you don't know.
    Don't try to make up an answer.

    CONTEXT:
    {context}

    USER QUESTION: 
    {query}

    ANSWER:
    """
    return prompt