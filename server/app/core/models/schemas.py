from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional


class QueryModel(BaseModel):
    query: str = Field(..., description="The user's question or search query")


class DocumentResponse(BaseModel):
    documents: List[str] = Field(..., description="List of relevant document contents")


class GeminiResponse(BaseModel):
    output: str = Field(..., description="Generated response from Gemini")