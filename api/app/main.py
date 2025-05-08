from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.BM25.bm25 import BM25
from app.BM25.options import BM25Options
from app.gemini.gemini_api import generate_answer
from app.models.schemas import QueryModel

app = FastAPI()
args = BM25Options().args
bm25 = BM25(args)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/retrieve")
def retrieve(query: QueryModel):
    try:
        results = bm25.search(args.index_name, query.query)
        documents = [item["content"] for item in results]
        return {"documents": documents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/gemini")
def gemini(query: QueryModel):
    try:
        result = generate_answer(query.query)
        return {"output": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
