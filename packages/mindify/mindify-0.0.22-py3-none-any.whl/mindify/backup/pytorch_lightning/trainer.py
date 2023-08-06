import os
import uuid

import wandb
import pytorch_lightning as pl
from pytorch_lightning import Trainer
from pytorch_lightning.callbacks import ModelCheckpoint
from pytorch_lightning.loggers import WandbLogger

from mindify.backup.helpers import DateHelper, FileHelper


class WandbTrainer(object):
    def __init__(self, project: str = 'test', name: str = 'test', wandb_enabled: bool = True,
                 checkpoint_monitor: str = None, checkpoint_monitor_mode: str = 'min', **kwargs):

        self.wandb_enabled = wandb_enabled

        os.environ["WANDB_NOTEBOOK_NAME"] = project
        uname = name + "_" + DateHelper.format_date(DateHelper.now(), '%m%d%H%M%S')

        wandb_logger_dir = FileHelper.get_home_path("wandb")
        print("name=", uname, "wandb_logger_dir = ", wandb_logger_dir)

        loggers = kwargs.pop('loggers') if 'loggers' in kwargs else []
        if loggers is None:
            loggers = []

        if wandb_enabled:
            loggers.append(WandbLogger(project=project, name=uname, id=uuid.uuid4().hex, dir=wandb_logger_dir,
                                       settings=wandb.Settings(start_method='thread', _disable_stats=True),
                                       reinit=True))

        callbacks = kwargs.pop('callbacks') if 'callbacks' in kwargs else []
        if callbacks is None:
            callbacks = []

        if checkpoint_monitor is not None:
            checkpoint_callback = ModelCheckpoint(
                monitor=checkpoint_monitor,
                mode=checkpoint_monitor_mode,
                dirpath=FileHelper.get_home_path("checkpoints/checkpoints-" + project),
                filename=project + '-' + name + '-epoch{epoch:02d}-val_loss{' + checkpoint_monitor + ':.4f}',
                save_top_k=5,
                auto_insert_metric_name=False
            )
            callbacks.append(checkpoint_callback)
            kwargs['enable_checkpointing'] = True

        kwargs = {
            'num_sanity_val_steps': 0,
            'enable_model_summary': False,
            'accelerator': 'gpu',
            'enable_checkpointing': False,
            **kwargs
        }
        self.trainer = Trainer(logger=loggers, callbacks=callbacks, **kwargs)

        self.module = None
        self.datamodule = None

    def fit(self, module: 'pl.LightningModule', datamodule: 'pl.LightningDataModule', ckpt_path: str = None):
        self.module = module
        self.datamodule = datamodule

        for logger in self.trainer.loggers:
            logger.log_hyperparams(self.module.hparams)

        self.trainer.fit(module, datamodule, ckpt_path=ckpt_path)

        if self.wandb_enabled:
            wandb.finish(quiet=True)
