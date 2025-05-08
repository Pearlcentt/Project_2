import torch
import numpy as np
from typing import List
from transformers import (
    AutoTokenizer,
    RobertaPreTrainedModel,
    PretrainedConfig,
    RobertaModel,
)
from pyvi.ViTokenizer import tokenize
from dense.modules import Pooler, SimilarityFunction
from dataset.data_utils import preprocess


class DenseEmbedding(RobertaPreTrainedModel):
    def __init__(self, config: PretrainedConfig, args):
        super().__init__(config)
        self.args = args
        self.config = config

        self.pooling = Pooler(pooler_type=args.pooler_type)
        self.sim_fn = SimilarityFunction(sim_func_type=args.sim_func_type)
        self.roberta = RobertaModel(config, add_pooling_layer=False)

        self.tokenizer = AutoTokenizer.from_pretrained(
            "VoVanPhuc/sup-SimCSE-VietNamese-phobert-base"
        )

    def get_output(self, text: List[str]):
        if isinstance(text, str):
            text = [text]

        text = list(map(tokenize, text))

        inputs = self.tokenizer(
            text, padding=True, truncation=True, return_tensors="pt"
        ).to(self.args.device)

        with torch.no_grad():
            outputs = self.roberta(**inputs)
            pooled_output = self.pooling(inputs["attention_mask"], outputs)

        return pooled_output

    def forward(
        self,
        query,
        documents,
    ):
        query = preprocess(query)

        query_embedding = self.get_output(query)
        document_embeddings = self.get_output(documents)

        scores = self.sim_fn(query_embedding, document_embeddings).view(-1).tolist()

        ind = np.argsort(scores)[-self.args.top_k_dense :][::-1]

        ind = [x for x in ind if scores[x] >= self.args.dense_threshold]

        if len(ind) == 0:
            return None

        best_documents = list(map(documents.__getitem__, ind))

        return best_documents


class FQAModel(RobertaPreTrainedModel):
    def __init__(self, config: PretrainedConfig, args):
        super().__init__(config)
        self.args = args
        self.config = config

        self.pooling = Pooler(pooler_type=args.pooler_type)
        self.sim_fn = SimilarityFunction(name_fn=args.sim_fn)
        self.roberta = RobertaModel(config, add_pooling_layer=False)
        self.tokenizer = AutoTokenizer.from_pretrained(args.model_name_or_path)

    def get_output(self, text: List[str]):
        if isinstance(text, str):
            text = [text]

        text = list(map(tokenize, text))

        inputs = self.tokenizer(
            text, padding=True, truncation=True, return_tensors="pt"
        ).to(self.args.device)

        with torch.no_grad():
            outputs = self.roberta(**inputs)
            pooled_output = self.pooling(inputs["attention_mask"], outputs)

        return pooled_output

    def forward(self, query, documents):
        query = preprocess(query)

        query_embedding = self.get_output(query)
        document_embeddings = self.get_output(documents)

        scores = self.sim_fn(query_embedding, document_embeddings).view(-1).tolist()

        ind = np.argsort(scores)[-1:][::-1]

        best_documents = list(map(documents.__getitem__, ind))[0]

        return scores[0], best_documents
