import pandas as pd
from tqdm import tqdm
from elasticsearch.helpers import bulk
from app.core.utils.es_client import get_es_client

def index_bm25_data(index_name: str, csv_path: str, mapping: dict):
    es = get_es_client()

    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=mapping)
        print(f"✅ Created index '{index_name}'")
    else:
        print(f"ℹ️ Index '{index_name}' already exists")

    df = pd.read_csv(csv_path, encoding="utf-8-sig")
    df.dropna(subset=["content"], inplace=True)
    df.drop_duplicates(subset=["content"], inplace=True)
    docs = df.to_dict(orient="records")

    actions = [
        {
            "_index": index_name,
            "_id": doc["id"],
            "_source": {
                "id": doc["id"],
                "chuong": doc["chuong"],
                "dieu": doc["dieu"],
                "content": doc["content"]
            },
        }
        for doc in tqdm(docs)
    ]

    success, _ = bulk(es, actions)
    print(f"✅ Indexed {success} documents into '{index_name}'")
