from fastapi import FastAPI
from elasticsearch import Elasticsearch

app = FastAPI(title="Quy chế Đào tạo Search API")

# Elasticsearch client
es = Elasticsearch("http://localhost:9200")

@app.get("/")
async def root():
    return {"message": "API is running!"}

@app.get("/search")
async def search(query: str):
    search_query = {
        "query": {
            "match": {
                "content": query
            }
        }
    }

    response = es.search(index="quy_che_index", body=search_query)
    
    results = []
    for hit in response["hits"]["hits"]:
        results.append({
            "score": hit["_score"],
            "chuong": hit["_source"]["chuong"],
            "dieu": hit["_source"]["dieu"],
            "content_snippet": hit["_source"]["content"][:300]
        })

    return {"results": results}
