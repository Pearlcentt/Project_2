import os

class BM25Options:
    """
    Configurable options for BM25 retrieval.
    """

    def __init__(self):
        self.es_host = os.getenv("ES_HOST", "http://localhost:9200")
        self.index_name = os.getenv("BM25_INDEX_NAME", "quy_che_index")
        self.data_path = os.getenv("BM25_DATA_PATH", "data/final.csv")
        self.top_k = int(os.getenv("BM25_TOP_K", 5))
        self.token_level = os.getenv("BM25_TOKEN_LEVEL", "word-level")
        self.index_mapping = {
            "mappings": {
                "properties": {
                    "chuong": {"type": "text"},
                    "dieu": {"type": "text"},
                    "content": {"type": "text"},
                }
            }
        }
