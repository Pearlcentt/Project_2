import torch
from torch.utils.data import Dataset, DataLoader
from transformers import PreTrainedTokenizer
import pandas as pd

from dataset.data_utils import process_and_tokenize


class OursDataset(Dataset):
    def __init__(self, args, tokenizer: PreTrainedTokenizer, mode: str = "train"):
        super(OursDataset, self).__init__()

        self.args = args
        self.tokenizer = tokenizer

        self.data = pd.read_csv("data/final_question.csv")

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        data_point = self.data.iloc[idx]

        question = data_point["questions"]

        document = data_point["content"]

        input_ids_q, attn_mask_q = process_and_tokenize(
            question,
            self.tokenizer,
            self.args.max_seq_len_query,
        )

        input_ids_d, attn_mask_d = process_and_tokenize(
            document,
            self.tokenizer,
            self.args.max_seq_len_document,
        )

        return (
            torch.tensor(input_ids_q, dtype=torch.long),
            torch.tensor(attn_mask_q, dtype=torch.long),
            torch.tensor(input_ids_d, dtype=torch.long),
            torch.tensor(attn_mask_d, dtype=torch.long),
        )
