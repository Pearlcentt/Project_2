from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import pandas as pd
from tqdm import tqdm

ES_HOST = "http://localhost:9200"
INDEX_NAME = "quy_che_index"

print(f"Connecting to Elasticsearch at {ES_HOST}...")
es = Elasticsearch(ES_HOST)

if es.ping():
    print("✅ Successfully connected to Elasticsearch!")
else:
    print("❌ Could not connect to Elasticsearch.")
    exit()

print("\n🔎 Running a test search query...\n")

search_keyword = "Sinh viên muốn chuyển trường cần làm gì?"  

query = {
    "query": {
        "match": {
            "content": search_keyword
        }
    }
}

response = es.search(index=INDEX_NAME, body=query)

hits = response["hits"]["hits"]
print(f"✅ Found {len(hits)} results for '{search_keyword}'\n")

for hit in hits:
    print(f"📌 Score: {hit['_score']}")
    print(f"➡️  {hit['_source']['chuong']}")
    print(f"➡️  {hit['_source']['dieu']}")
    print(f"📝 Nội dung (trích đoạn): {hit['_source']['content'][:300]}...\n")
    print("=" * 100)

print("🎉 Test complete!")
