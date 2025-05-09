import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from transformers.trainer_pt_utils import get_parameter_names
from transformers.optimization import get_scheduler
from lion_pytorch import Lion
from tqdm import tqdm, trange


class Trainer:
    def __init__(self, args, model, train_dataset):
        self.args = args

        self.model = model.to(args.device)
        self.train_dataset = train_dataset

    def train(self):

        dataloader = DataLoader(
            self.train_dataset, batch_size=self.args.batch_size, shuffle=True
        )

        if self.args.max_steps > 0:
            total = self.args.max_steps
            self.args.num_train_epochs = (
                self.args.max_steps
                // (len(dataloader) // self.args.gradient_accumulation_steps)
                + 1
            )
        else:
            total = (
                len(dataloader)
                // self.args.gradient_accumulation_steps
                * self.args.num_train_epochs
            )

        optimizer = self.get_optimizer()
        scheduler = get_scheduler(
            self.args.lr_scheduler_type,
            optimizer=optimizer,
            num_warmup_steps=self.args.warmup_steps,
            num_training_steps=total,
        )

        print(
            f"Training with {len(dataloader)} steps, {self.args.num_train_epochs} epochs, {total} total steps"
        )

        global_step = 0

        self.model.zero_grad()
        train_iterator = trange(
            int(self.args.num_train_epochs),
            desc="Epoch",
            disable=False,
            dynamic_ncols=True,
        )

        scaler = torch.amp.grad_scaler.GradScaler()

        for _ in train_iterator:
            epoch_iterator = tqdm(
                dataloader, desc="Iteration", disable=False, dynamic_ncols=True
            )

            loss_lst = []

            for step, batch in enumerate(epoch_iterator):
                self.model.train()
                batch = tuple(t.to(self.args.device) for t in batch)

                inputs = {
                    "input_ids": batch[0],
                    "attention_mask": batch[1],
                    "input_ids_positive": batch[2],
                    "attention_mask_positive": batch[3],
                    "is_train": True,
                }

                with torch.amp.autocast("cuda"):
                    loss = self.model(**inputs)

                if self.args.gradient_accumulation_steps > 1:
                    loss = loss / self.args.gradient_accumulation_steps

                scaler.scale(loss).backward()

                if (step + 1) % self.args.gradient_accumulation_steps == 0:
                    torch.nn.utils.clip_grad_norm_(
                        self.model.parameters(), self.args.max_grad_norm
                    )

                    scaler.step(optimizer)
                    scheduler.step()
                    scaler.update()

                    self.model.zero_grad()
                    global_step += 1

                loss_lst.append(loss.item())

                if 0 < self.args.max_steps < global_step:
                    epoch_iterator.close()
                    break

            if 0 < self.args.max_steps < global_step:
                train_iterator.close()
                break
        self.cur_lost_lst = loss_lst

    def get_optimizer(self):
        decay_parameters = get_parameter_names(self.model, [torch.nn.LayerNorm])
        decay_parameters = [name for name in decay_parameters if "bias" not in name]
        optimizer_grouped_parameters = [
            {
                "params": [
                    p for n, p in self.model.named_parameters() if n in decay_parameters
                ],
                "weight_decay": self.args.weight_decay,
            },
            {
                "params": [
                    p
                    for n, p in self.model.named_parameters()
                    if n not in decay_parameters
                ],
                "weight_decay": 0.0,
            },
        ]
        optimizer = Lion(optimizer_grouped_parameters, lr=self.args.learning_rate)
        return optimizer
