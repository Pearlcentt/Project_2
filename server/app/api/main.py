# server/app/api/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.bm25.bm25 import BM25
from app.core.bm25.options import BM25Options
from app.core.utils.load_model import get_dense_model
from app.core.models.schemas import QueryModel
from app.core.gemini.gemini_api import call_gemini
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bm25_config = BM25Options()
bm25 = BM25(bm25_config)

bm25.insert_data(bm25_config.index_name, bm25_config.data_path)

df = pd.read_csv(bm25_config.data_path, encoding="utf-8-sig")
documents = df["content"].dropna().drop_duplicates().tolist()

@app.post("/api/retrieve")
def retrieve(query: QueryModel):
    sparse_results = bm25.search(bm25_config.index_name, query.query)
    dense_model = get_dense_model()
    reranked = dense_model(query.query, documents)
    return {"documents": reranked}

@app.post("/api/gemini")
def ask_gemini(query: QueryModel):
    result = call_gemini(query.query)
    return {"output": result}
