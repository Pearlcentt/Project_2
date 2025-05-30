from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional


class QueryModel(BaseModel):
    query: str = Field(..., description="The user's question or search query")


class DocumentResponse(BaseModel):
    """
    Response model for document retrieval.
    """
    documents: List[str] = Field(..., description="List of relevant document contents")


class GeminiResponse(BaseModel):
    """
    Response model for Gemini API calls.
    """
    output: str = Field(..., description="Generated response from Gemini")
    documents: List[str] = Field(default_factory=list, description="List of relevant document contents")


class LoginRequest(BaseModel):
    """
    Request model for user login.
    """
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")


class SignupRequest(BaseModel):
    """
    Request model for user signup.
    """
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password", min_length=8)
    name: Optional[str] = Field(None, description="User's full name")