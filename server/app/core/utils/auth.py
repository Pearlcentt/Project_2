from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from app.core.models.user import User
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {}


def verify_password(plain_password, hashed_password):
    """
    Verify a password against a hash.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    Generate password hash.
    """
    return pwd_context.hash(password)


def get_user_by_email(email: str):
    """
    Get user by email from the database.
    """
    if email in fake_users_db:
        user_dict = fake_users_db[email]
        return User(**user_dict)
    return None


def authenticate_user(email: str, password: str):
    """
    Authenticate a user based on email and password.
    """
    user = get_user_by_email(email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_user(user_data):
    """
    Create a new user in the database.
    """
    hashed_password = get_password_hash(user_data.password)
    user_dict = {
        "email": user_data.email,
        "hashed_password": hashed_password,
        "name": user_data.name,
        "disabled": False
    }
    fake_users_db[user_data.email] = user_dict
    return User(**user_dict)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT token.
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def verify_token(token: str):
    """
    Verify a JWT token and extract payload.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        return payload
    except JWTError:
        return None


def get_current_user(token: str):
    """
    Get current user from a token.
    """
    payload = verify_token(token)
    if payload is None:
        return None
    
    email: str = payload.get("sub")
    user = get_user_by_email(email)
    
    return user