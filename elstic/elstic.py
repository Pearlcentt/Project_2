from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

if es.ping():
    print("✅ Connected!")
else:
    print("❌ Failed to connect")
