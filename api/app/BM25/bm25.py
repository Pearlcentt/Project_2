from elasticsearch import Elasticsearch
from typing import List, Dict, Union
from app.BM25.options import BM25Options
import pandas as pd


class BM25:
    """
    A wrapper class around elastic search to simplify usage and accomodate for communication with the frontend.
    """

    def __init__(self, args: BM25Options):
        """
        Initialize the BM25 class with the given arguments.

        :param args: Arguments containing the Elasticsearch host and other configurations. Currently, this should be a BM25.options object.
        :type args: BM25Options
        """
        self.args = args
        self.es = Elasticsearch(self.args.es_host)

    def ping(self):
        """
        Check if the elasticsearch server is reachable.
        """
        return self.es.ping()

    def search(
        self, index_name: str, search_query: str
    ) -> List[Dict[str, Union[str, float]]]:
        """
        Search for a query in the specified index.

        :param index_name: The name of the index to search in.
        :type index_name: str
        :param search_query: The query string to search for.
        :type search_query: str
        :return: A list of search results, each containing the score, chapter, article, and content.
        :rtype: list of dict
        :raises ConnectionError: If the Elasticsearch server is not reachable.
        :raises ValueError: If the specified index does not exist.
        """

        if not self.ping():
            raise ConnectionError("Elasticsearch server is not reachable.")

        if not self.es.indices.exists(index=index_name):
            raise ValueError(f"Index '{index_name}' does not exist.")

        query = {"query": {"match": {"content": search_query}}}
        response = self.es.search(index=index_name, body=query)

        hits = response["hits"]["hits"]
        results = []

        for hit in hits:
            result = {
                "score": hit["_score"],
                "chuong": hit["_source"]["chuong"],
                "dieu": hit["_source"]["dieu"],
                "content": hit["_source"]["content"],
            }
            results.append(result)

        return results

    def _bulk_insert_to_elasticsearch(self, index_name, chunks):
        """
        Insert data into Elasticsearch in bulk.

        :param index_name: The name of the index to insert data into.
        :type index_name: str
        :param chunks: The data to be inserted, in the form of a list of dictionaries.
        :type chunks: list of dict
        """
        actions = []
        for chunk in chunks:
            doc = {
                "_index": index_name,
                "_id": chunk["id"],  # unique UUID
                "_source": {
                    "id": chunk["id"],
                    "chuong": chunk["chapter"],
                    "dieu": chunk["section"],
                    "content": chunk["content"],
                },
            }
            actions.append(doc)

        from elasticsearch.helpers import bulk

        success, _ = bulk(self.es, actions)
        print(f"✅ Successfully indexed {success} documents.")

    def insert_data(self, index_name, data_path):
        """
        Insert data from a CSV file into Elasticsearch.

        :param index_name: The name of the index to insert data into.
        :type index_name: str
        :param data_path: The path to the CSV file containing the data.
        :type data_path: str
        :raises ConnectionError: If the Elasticsearch server is not reachable.
        """

        index_mapping = self.args.index_mapping

        if not self.ping():
            raise ConnectionError("Elasticsearch server is not reachable.")

        if not self.es.indices.exists(index=index_name):
            print(f"Index '{index_name}' does not exist. Creating it now.")
            self.es.indices.create(index=index_name, body=index_mapping)
            print(f"Index '{index_name}' created.")

        df = pd.read_csv(data_path, encoding="utf-8-sig")
        chunks = df.to_dict(orient="records")

        self._bulk_insert_to_elasticsearch(index_name, chunks)

    def insert_folder(self, index_name, folder_path):
        """
        Insert all CSV files in a folder into Elasticsearch.

        :param index_name: The name of the index to insert data into.
        :type index_name: str
        :param folder_path: The path to the folder containing CSV files.
        :type folder_path: str
        """
        import os

        if not os.path.exists(folder_path):
            raise ValueError(f"Folder '{folder_path}' does not exist.")

        for file in os.listdir(folder_path):
            if file.endswith(".csv"):
                file_path = os.path.join(folder_path, file)
                self.insert_data(index_name, file_path)
