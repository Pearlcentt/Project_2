import os
import torch
from dotenv import load_dotenv
from transformers import set_seed, AutoTokenizer, RobertaConfig
import matplotlib.pyplot as plt

from train.trainer import Trainer
from dataset.dataset import OursDataset
from dense.dense_model import DenseModel

# Load .env variables
load_dotenv()


class TrainConfig:
    def __init__(self):
        self.model_dir = os.getenv("MODEL_DIR")
        self.data_dir = os.getenv("DATA_DIR")
        self.token_level = os.getenv("TOKEN_LEVEL", "word-level")
        self.model_type = os.getenv("MODEL_TYPE", "phobert")
        self.do_train = os.getenv("DO_TRAIN", "false").lower() == "true"
        self.pretrained = os.getenv("PRETRAINED", "false").lower() == "true"
        self.pretrained_path = os.getenv("PRETRAINED_PATH")

        self.seed = int(os.getenv("SEED", 42))
        self.num_train_epochs = float(os.getenv("NUM_TRAIN_EPOCHS", 2))
        self.batch_size = int(os.getenv("BATCH_SIZE", 32))
        self.dataloader_drop_last = os.getenv("DATALOADER_DROP_LAST", "true").lower() == "true"
        self.dataloader_num_workers = int(os.getenv("DATALOADER_NUM_WORKERS", 0))
        self.dataloader_pin_memory = os.getenv("DATALOADER_PIN_MEMORY", "true").lower() == "true"

        self.max_seq_len_query = int(os.getenv("MAX_SEQ_LEN_QUERY", 64))
        self.max_seq_len_document = int(os.getenv("MAX_SEQ_LEN_DOCUMENT", 256))
        self.use_fast_tokenizer = os.getenv("USE_FAST_TOKENIZER", "false").lower() == "true"

        self.gradient_checkpointing = os.getenv("GRADIENT_CHECKPOINTING", "false").lower() == "true"
        self.learning_rate = float(os.getenv("LEARNING_RATE", 1e-5))
        self.lr_scheduler_type = os.getenv("LR_SCHEDULER_TYPE", "cosine")
        self.weight_decay = float(os.getenv("WEIGHT_DECAY", 0.0))
        self.gradient_accumulation_steps = int(os.getenv("GRADIENT_ACCUMULATION_STEPS", 1))
        self.max_grad_norm = float(os.getenv("MAX_GRAD_NORM", 1.0))
        self.warmup_steps = int(os.getenv("WARMUP_STEPS", 100))
        self.max_steps = int(os.getenv("MAX_STEPS", -1))
        self.early_stopping = int(os.getenv("EARLY_STOPPING", 50))

        dtype_str = os.getenv("COMPUTE_DTYPE", "float").lower()
        self.compute_dtype = getattr(torch, dtype_str, torch.float)

        self.pooler_type = os.getenv("POOLER_TYPE", "avg")
        self.sim_func_type = os.getenv("SIM_FUNC_TYPE", "dot")
        self.label_smoothing = float(os.getenv("LABEL_SMOOTHING", 0.0))

        self.device = "cuda" if torch.cuda.is_available() else "cpu"


def main(args):
    set_seed(args.seed)

    tokenizer = AutoTokenizer.from_pretrained(
        "VoVanPhuc/sup-SimCSE-VietNamese-phobert-base"
    )

    if args.pretrained:
        model = DenseModel.from_pretrained(
            args.pretrained_path,
            torch_dtype=args.compute_dtype,
            device_map=args.device,
            args=args,
        )
    else:
        config = RobertaConfig.from_pretrained(
            "VoVanPhuc/sup-SimCSE-VietNamese-phobert-base",
            finetuning_task=args.token_level,
        )
        model = DenseModel.from_pretrained(
            "VoVanPhuc/sup-SimCSE-VietNamese-phobert-base",
            torch_dtype=args.compute_dtype,
            config=config,
            device_map=args.device,
            args=args,
        )

    if args.gradient_checkpointing:
        model.gradient_checkpointing_enable()

    train_dataset = OursDataset(args=args, tokenizer=tokenizer, mode="train")

    trainer = Trainer(args=args, model=model, train_dataset=train_dataset)

    if args.do_train:
        trainer.train()

        # Plotting the training loss
        plt.plot(trainer.cur_lost_lst, label="Training Loss")
        plt.xlabel("Steps")
        plt.ylabel("Loss")
        plt.title("Training Loss Over Steps")
        plt.legend()
        plt.savefig("training_loss.png")  # Save the plot as a file
        plt.show()  # Display the plot

        # Save the model
        model.save_pretrained(args.model_dir)


if __name__ == "__main__":
    config = TrainConfig()
    main(config)
