from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List, Optional

from app.core.bm25.bm25 import BM25
from app.core.bm25.options import BM25Options
from app.core.utils.load_model import get_dense_model
from app.core.models.schemas import QueryModel, DocumentResponse, GeminiResponse
from app.core.gemini.gemini_api import call_gemini, format_prompt_with_context
from app.core.models.user import UserCreate, UserResponse, User, Token
from app.core.utils.auth import create_access_token, verify_token, get_current_user, authenticate_user, create_user, get_user_by_email

import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="HUST Q&A API", description="Retrieving documents and generating answers")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bm25_config = BM25Options()
bm25 = BM25(bm25_config)
bm25.insert_data(bm25_config.index_name, bm25_config.data_path)

df = pd.read_csv(bm25_config.data_path, encoding="utf-8-sig")
documents = df["content"].dropna().drop_duplicates().tolist()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")

@app.post("/api/auth/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login endpoint that provides access token using OAuth2 form data"""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token, token_type="bearer")

@app.post("/api/auth/login", response_model=UserResponse) 
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login endpoint that matches frontend service expectations"""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return UserResponse(
        user=user,
        token=access_token
    )

@app.post("/api/auth/signup", response_model=UserResponse)
async def signup(user_data: UserCreate):
    if get_user_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    new_user = create_user(user_data)
    access_token = create_access_token(data={"sub": new_user.email})
    
    return UserResponse(
        user=new_user,
        token=access_token
    )

@app.get("/api/auth/verify")
async def verify_auth(token: str = Depends(oauth2_scheme)):
    """Verify authentication token endpoint"""
    user = get_current_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {"verified": True}

@app.post("/api/retrieve", response_model=DocumentResponse)
async def retrieve(query: QueryModel, token: str = Depends(oauth2_scheme)):
    """Retrieves relevant documents using BM25 and dense reranking"""
    user = get_current_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    sparse_results = bm25.search(bm25_config.index_name, query.query)
    sparse_docs = [doc["content"] for doc in sparse_results]
    
    dense_model = get_dense_model()
    reranked = dense_model(query.query, documents)
    
    return DocumentResponse(documents=reranked if reranked else sparse_docs[:bm25_config.top_k])

@app.post("/api/gemini", response_model=GeminiResponse)
async def ask_gemini(query: QueryModel, token: str = Depends(oauth2_scheme)):
    user = get_current_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    result = call_gemini(query.query)
    return GeminiResponse(output=result)

@app.post("/api/ask", response_model=GeminiResponse)
async def ask_with_context(query: QueryModel, token: str = Depends(oauth2_scheme)):
    user = get_current_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    sparse_results = bm25.search(bm25_config.index_name, query.query)
    sparse_docs = [doc["content"] for doc in sparse_results]
    
    dense_model = get_dense_model()
    reranked = dense_model(query.query, documents)
    
    relevant_docs = reranked if reranked else sparse_docs[:bm25_config.top_k]
    
    prompt_with_context = format_prompt_with_context(query.query, relevant_docs)
    
    result = call_gemini(prompt_with_context)
    
    return GeminiResponse(output=result)