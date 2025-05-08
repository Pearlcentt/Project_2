# app/core/utils/load_model.py
import torch
from transformers import RobertaConfig
from app.core.dense.dense_embedding import DenseEmbedding

_dense_model = None

def get_dense_model(model_path="model", token_level="word-level", device=None):
    global _dense_model
    if _dense_model is None:
        config = RobertaConfig.from_pretrained(model_path, finetuning_task=token_level)
        args = type("Args", (), {})()
        args.model_name_or_path = model_path
        args.token_level = token_level
        args.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
        _dense_model = DenseEmbedding.from_pretrained(model_path, config=config, args=args)
        _dense_model.to(args.device)
        _dense_model.eval()
    return _dense_model
