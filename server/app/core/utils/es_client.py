from elasticsearch import Elasticsearch
import os

def get_es_client():
    return Elasticsearch(os.getenv("ES_HOST", "http://localhost:9200"))
