# train_gpt2.py
import torch
import pytorch_lightning as pl
from pytorch_lightning import Trainer
from pytorch_lightning.strategies import DeepSpeedStrategy
from pytorch_lightning.loggers import MLFlowLogger
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from datasets import load_dataset


class GPT2Finetuner(pl.LightningModule):
    def __init__(self, model_name="gpt2", lr=5e-5):
        super().__init__()
        self.save_hyperparameters()
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        #fix padding issue
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.lr = lr

        dataset = load_dataset("wikitext", "wikitext-2-raw-v1", split="train")

        def encode(examples):
            return self.tokenizer(
                examples["text"],
                truncation=True,
                padding="max_length",
                max_length=128
            )

        dataset = dataset.map(encode, batched=True)
        self.dataset = dataset.with_format("torch")

    def training_step(self, batch, batch_idx):
        outputs = self.model(input_ids=batch["input_ids"], labels=batch["input_ids"])
        loss = outputs.loss
        self.log("train_loss", loss, prog_bar=True)
        return loss

    def configure_optimizers(self):
        return torch.optim.AdamW(self.parameters(), lr=self.lr)

    def train_dataloader(self):
        return torch.utils.data.DataLoader(self.dataset, batch_size=8, shuffle=True)


def main():
    import os, socket
    '''
    # Resolve the node's IP instead of using hostname
    master_ip = socket.gethostbyname(socket.gethostname())
    os.environ["MASTER_ADDR"] = master_ip
    os.environ["MASTER_PORT"] = "29500"
    os.environ["NCCL_SOCKET_IFNAME"] = "eth0"   # or ens3 / ens5 depending on your NIC
    os.environ["NCCL_DEBUG"] = "INFO"
    '''
    os.environ.setdefault("NCCL_SOCKET_IFNAME", "eth0")   # or ens5/ens3 if that's your NIC
    os.environ.setdefault("NCCL_DEBUG", "WARN")
    os.environ.setdefault("MASTER_PORT", "29500")
    # Don't set MASTER_ADDR here; the launcher will provide rendezvous info


    # attach MLflow logger
    mlf_logger = MLFlowLogger(experiment_name="/Users/kristofer.schlachter/deepspeed_zero2")

    # point to your DeepSpeed config
    strategy = DeepSpeedStrategy(config="/dbfs/ds_config.json")
    '''
    trainer = Trainer(
        max_epochs=1,
        accelerator="gpu",
        devices=4,       # GPUs per node (g5.12xlarge has 4)
        num_nodes=4,     # 4 worker nodes
        precision="16-mixed",
        strategy=strategy,
        logger=mlf_logger
    )'''

     # IMPORTANT: when using an external launcher (TorchDistributor/torchrun),
    # each process should manage a SINGLE GPU -> devices=1.
    # Lightning infers world size/ranks from env; you don't set num_nodes here.
    trainer = Trainer(
        max_epochs=1,
        accelerator="gpu",
        devices=1,                 # one process == one GPU
        precision="16-mixed",
        strategy=strategy,
        logger=mlf
    )



    model = GPT2Finetuner()
    trainer.fit(model)


if __name__ == "__main__":
    main()