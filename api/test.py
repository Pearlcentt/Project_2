# Test both BM25 and Dense retrievers

import torch
import pandas as pd
import argparse
import colorama
from transformers import AutoTokenizer, RobertaConfig
from app.dense.dense_embedding import DenseEmbedding
from FlagEmbedding import FlagReranker
import time

from app.BM25.bm25 import BM25
from app.BM25.options import BM25Options
from app.dataset.data_utils import preprocess

parser = argparse.ArgumentParser()
parser.add_argument(
    "--top_k_bm25", default=15, type=int, help="Số lượng tài liệu lấy từ BM25"
)
parser.add_argument(
    "--top_k_dense", default=5, type=int, help="Số lượng tài liệu lấy từ mô hình dense"
)
parser.add_argument(
    "--sim_func_type", default="cosine", type=str, help="Hàm đo độ tương đồng"
)
parser.add_argument(
    "--pooler_type", default="avg", type=str, help="Loại pooler cho mô hình dense"
)
parser.add_argument("--dense_threshold", default=0.65, type=float, help="Ngưỡng dense")
parser.add_argument(
    "--token_level", default="word-level", type=str, help="Cấp độ tokenization"
)
parser.add_argument(
    "--data_path",
    default="app/data/final.csv",
    type=str,
)
parser.add_argument(
    "--dense_model_type",
    default="supsim-cse-vietnamese",
    type=str,
)
args = parser.parse_args()
args.device = "cuda" if torch.cuda.is_available() else "cpu"
print("Sử dụng thiết bị: ", args.device)
args.model_name_or_path = "app/model"

model_config = RobertaConfig.from_pretrained(
    args.model_name_or_path, finetuning_task=args.token_level
)
dense_model = DenseEmbedding.from_pretrained(
    args.model_name_or_path, config=model_config, args=args
)

df = pd.read_csv(args.data_path, encoding="utf-8")
df = df.dropna()
df = df.drop_duplicates(subset=["content"])
df = df.reset_index(drop=True)
df["content"] = (
    df["from"] + "\n" + df["chapter"] + "\n" + df["section"] + "\n" + df["content"]
)

col = df["content"].apply(lambda x: preprocess(x, False))
docs = col.tolist()

docs = df["content"].tolist()

bm25_options = BM25Options().args
bm25_options.top_k = args.top_k_bm25
bm25_options.token_level = args.token_level
bm25_options.data_path = args.data_path
bm25_options.index_name = "bm25_index"
bm25_options.index_mapping = {
    "mappings": {
        "properties": {
            "chuong": {"type": "text"},
            "dieu": {"type": "text"},
            "content": {"type": "text"},
        }
    }
}

bm25 = BM25(bm25_options)
bm25.insert_data(bm25_options.index_name, args.data_path)
dense_model.to(args.device)

reranker = FlagReranker("namdp-ptit/ViRanker", use_fp16=True, devices=args.device)

while True:
    query = input("Nhập câu truy vấn: ")
    if query == "exit":
        break
    if query == "":
        continue

    query = preprocess(query)

    colorama.init()
    colorama.ansi.autoreset = True

    print(colorama.Fore.BLUE + "***" * 30 + colorama.Fore.RESET)
    bm25_results = bm25.search(
        index_name=bm25_options.index_name,
        search_query=query,
    )

    docs = [preprocess(doc["content"]) for doc in bm25_results]

    if not docs:
        print("Không tìm thấy tài liệu nào phù hợp.")
        continue

    dense_model.eval()
    start = time.time()

    list_relevant = dense_model(query, docs)

    if not list_relevant:
        print("Không tìm thấy tài liệu nào phù hợp.")
        continue
    elif len(list_relevant) > args.top_k_dense:
        list_relevant = list_relevant[: args.top_k_dense]
    pairs = [[query, preprocess(doc, remove_nl=True)] for doc in list_relevant]
    scores = reranker.compute_score(pairs)

    scores_docs = zip(scores, list_relevant)

    sorted_scores_docs = sorted(scores_docs, key=lambda x: x[0], reverse=True)

    end = time.time()

    for score, doc in sorted_scores_docs:
        print("Điểm: ", score)
        print("Tài liệu: ", doc)
        print("===" * 30)

    print("Thời gian thực hiện: ", end - start, " giây")

    print(colorama.Fore.BLUE + "***" * 30 + colorama.Fore.RESET)
