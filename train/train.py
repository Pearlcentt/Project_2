import torch
import argparse
from transformers import set_seed, AutoTokenizer, RobertaConfig
import matplotlib.pyplot as plt

from train.trainer import Trainer
from dataset.dataset import OursDataset
from dense.dense_model import DenseModel


def main(args):
    set_seed(42)

    args.device = "cuda" if torch.cuda.is_available() else "cpu"

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
    # Set up argument parser
    parser = argparse.ArgumentParser()

    # Model and data related arguments
    parser.add_argument(
        "--model_dir",
        default=None,
        required=True,
        type=str,
        help="Path to save or load model",
    )
    parser.add_argument(
        "--data_dir",
        default=None,
        type=str,
        help="The input data directory",
    )
    parser.add_argument(
        "--token_level",
        type=str,
        default="word-level",
        help="Tokenization level (word-level or syllable-level for Vietnamese)",
    )
    parser.add_argument(
        "--model_type",
        default="phobert",
        type=str,
        help="Model type to use",
    )
    parser.add_argument(
        "--do_train",
        action="store_true",
        help="Flag to run the training process",
    )
    parser.add_argument(
        "--pretrained",
        action="store_true",
        help="Whether to use a pretrained base model",
    )
    parser.add_argument(
        "--pretrained_path",
        default=None,
        type=str,
        help="Path to pretrained model",
    )

    # Training hyperparameters
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for initialization",
    )
    parser.add_argument(
        "--num_train_epochs",
        default=2.0,
        type=float,
        help="Total number of training epochs",
    )
    parser.add_argument(
        "--batch_size",
        default=32,
        type=int,
        help="Batch size for training",
    )
    parser.add_argument(
        "--dataloader_drop_last",
        type=bool,
        default=True,
        help="Whether to drop the last incomplete batch in dataloader",
    )
    parser.add_argument(
        "--dataloader_num_workers",
        type=int,
        default=0,
        help="Number of workers for dataloader",
    )
    parser.add_argument(
        "--dataloader_pin_memory",
        type=bool,
        default=True,
        help="Whether to use pinned memory in dataloader",
    )

    # Tokenizer configuration
    parser.add_argument(
        "--max_seq_len_query",
        default=64,
        type=int,
        help="Maximum sequence length for query after tokenization",
    )
    parser.add_argument(
        "--max_seq_len_document",
        default=256,
        type=int,
        help="Maximum sequence length for document after tokenization",
    )
    parser.add_argument(
        "--use_fast_tokenizer",
        default=False,
        type=bool,
        help="Whether to use the fast tokenizer",
    )

    # Optimizer configuration
    parser.add_argument(
        "--gradient_checkpointing",
        action="store_true",
        help="Enable gradient checkpointing to reduce memory usage",
    )
    parser.add_argument(
        "--learning_rate",
        default=1e-5,
        type=float,
        help="Initial learning rate for Adam optimizer",
    )
    parser.add_argument(
        "--lr_scheduler_type",
        default="cosine",
        type=str,
        help="Type of learning rate scheduler to use",
    )
    parser.add_argument(
        "--weight_decay",
        default=0.0,
        type=float,
        help="Weight decay for optimizer",
    )
    parser.add_argument(
        "--gradient_accumulation_steps",
        type=int,
        default=1,
        help="Number of steps to accumulate gradients before updating",
    )
    parser.add_argument(
        "--max_grad_norm",
        default=1.0,
        type=float,
        help="Maximum gradient norm for clipping",
    )
    parser.add_argument(
        "--warmup_steps",
        default=100,
        type=int,
        help="Number of warmup steps for learning rate scheduler",
    )
    parser.add_argument(
        "--max_steps",
        default=-1,
        type=int,
        help="Maximum number of training steps (-1 for no limit)",
    )
    parser.add_argument(
        "--early_stopping",
        type=int,
        default=50,
        help="Number of epochs without improvement for early stopping",
    )

    # Model configuration
    parser.add_argument(
        "--compute_dtype",
        type=torch.dtype,
        default=torch.float,
        help="Computation data type for the model",
    )
    parser.add_argument(
        "--pooler_type",
        default="avg",
        type=str,
        help="Type of pooler to use for the model",
    )
    parser.add_argument(
        "--sim_func_type",
        default="dot",
        type=str,
        help="Similarity function to use for calculations",
    )
    parser.add_argument(
        "--label_smoothing",
        default=0.00,
        type=float,
        help="Amount of label smoothing to apply",
    )

    # Parse arguments and set model path
    args = parser.parse_args()

    # Run main function
    main(args)
