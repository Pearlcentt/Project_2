import pandas as pd
from elasticsearch.helpers import bulk
from tqdm import tqdm
from elasticsearch import Elasticsearch

INDEX_NAME = "quy_che_index"

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")

index_mapping = {
    "mappings": {
        "properties": {
            "id": {"type": "keyword"},
            "chuong": {"type": "text"},
            "dieu": {"type": "text"},
            "content": {"type": "text"}
        }
    }
}

if not es.indices.exists(index=INDEX_NAME):
    es.indices.create(index=INDEX_NAME, body=index_mapping)
    print(f"✅ Index '{INDEX_NAME}' created.")
else:
    print(f"ℹ️ Index '{INDEX_NAME}' already exists.")


# Load CSV into pandas DataFrame
df = pd.read_csv("../data/processed/chuong_dieu_structured.csv", encoding="utf-8-sig")

# Convert to list of dicts
chunks = df.to_dict(orient="records")

def bulk_insert_to_elasticsearch(es, index_name, chunks):
    actions = []
    for chunk in tqdm(chunks):
        doc = {
            "_index": index_name,
            "_id": chunk["id"],  # unique UUID
            "_source": {
                "id": chunk["id"],
                "chuong": chunk["chuong"],
                "dieu": chunk["dieu"],
                "content": chunk["content"]
            }
        }
        actions.append(doc)

    from elasticsearch.helpers import bulk
    success, _ = bulk(es, actions)
    print(f"✅ Successfully indexed {success} documents.")

# Insert the data
bulk_insert_to_elasticsearch(es, INDEX_NAME, chunks)
