from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserBase(BaseModel):
    """
    Base user model with common fields.
    """
    email: EmailStr = Field(..., description="User's email address")
    name: Optional[str] = Field(None, description="User's full name")


class UserCreate(UserBase):
    """
    Model for user creation including password.
    """
    password: str = Field(..., description="User's password", min_length=8)


class User(UserBase):
    """
    Complete user model with additional fields.
    """
    hashed_password: str = Field(..., description="Hashed password")
    disabled: bool = Field(False, description="Whether the user is disabled")


class Token(BaseModel):
    """
    Model for JWT token response.
    """
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(..., description="Token type")


class UserResponse(BaseModel):
    """
    Response model for user signup and login.
    """
    user: User = Field(..., description="User information")
    token: str = Field(..., description="JWT access token")