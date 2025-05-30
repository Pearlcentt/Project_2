import torch
from transformers import RobertaConfig
from FlagEmbedding import FlagReranker
from app.core.dense.dense_embedding import DenseEmbedding

_dense_model = None


def get_dense_model(model_path="/app/model/", token_level="word-level", device=None):
    global _dense_model
    if _dense_model is None:
        config = RobertaConfig.from_pretrained(
            model_path, finetuning_task=token_level, local_files_only=True
        )
        args = type("Args", (), {})()
        args.model_name_or_path = model_path
        args.token_level = token_level
        args.pooler_type = "cls"
        args.sim_func_type = "dot"
        args.top_k_dense = 5
        args.dense_threshold = 0.65
        args.device = device or torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )
        _dense_model = DenseEmbedding.from_pretrained(
            model_path, config=config, args=args, local_files_only=True
        )
        _dense_model.to(args.device)
        _dense_model.eval()
    return _dense_model


def get_reranker(model_path="/app/model/", device=None):
    """
    Returns the reranker model.
    """
    reranker = FlagReranker("namdp-ptit/ViRanker")
    return reranker
