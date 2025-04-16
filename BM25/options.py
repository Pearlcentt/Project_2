from argparse import ArgumentParser


class BM25Options:
    """
    Options for the BM25 algorithm.
    """

    def __init__(self):
        parser = ArgumentParser(description="BM25 Options")
        parser.add_argument(
            "--es_host",
            type=str,
            default="http://localhost:9200",
            help="Elasticsearch host URL",
        )
        parser.add_argument(
            "--index_name",
            type=str,
            default="quy_che_index",
            help="Elasticsearch index name",
        )
        parser.add_argument(
            "--index_mapping",
            type=dict,
            default={
                "mappings": {
                    "properties": {
                        "chuong": {"type": "text"},
                        "dieu": {"type": "text"},
                        "content": {"type": "text"},
                    }
                }
            },
        )
