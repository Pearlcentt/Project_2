import torch
import torch.nn as nn
import torch.nn.functional as F


class Pooler(nn.Module):
    def __init__(self, pooler_type: str = "cls"):
        super(Pooler, self).__init__()
        self.pooler_type = pooler_type

    def forward(self, attention_mask, outputs):
        last_hidden_state = outputs.last_hidden_state
        hidden_states = outputs.hidden_states

        if self.pooler_type == "cls":
            return last_hidden_state[:, 0]
        elif self.pooler_type == "avg":
            return (last_hidden_state * attention_mask.unsqueeze(-1)).sum(
                1
            ) / attention_mask.sum(-1).unsqueeze(-1)

        else:
            raise ValueError("Invalid pooler type. Choose 'cls' or 'mean'.")


class SimilarityFunction(nn.Module):
    def __init__(self, sim_func_type: str = "dot"):
        super(SimilarityFunction, self).__init__()
        self.sim_func_type = sim_func_type

    def forward(self, pooled_output, pooled_output_positive):
        if self.sim_func_type == "cosine":
            sim_scores = F.cosine_similarity(
                pooled_output, pooled_output_positive.unsqueeze(1), dim=-1
            )
        elif self.sim_func_type == "dot":
            sim_scores = torch.matmul(
                pooled_output, torch.transpose(pooled_output_positive, 0, 1)
            )
        else:
            raise ValueError(
                "Invalid similarity function type. Choose 'cosine' or 'dot'."
            )

        return sim_scores
