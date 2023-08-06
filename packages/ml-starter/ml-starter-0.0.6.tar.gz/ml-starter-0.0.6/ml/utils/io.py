import logging
from pathlib import Path
from typing import TypeVar, cast

from omegaconf import DictConfig, OmegaConf

from ml.core.registry import register_model, register_task
from ml.models.base import BaseModel
from ml.tasks.base import BaseTask
from ml.trainers.base import DummyBaseTrainer
from ml.trainers.mixins.device.auto import AutoDevice
from ml.utils.timer import Timer

logger = logging.getLogger(__name__)

T = TypeVar("T")


def check_built(obj: T | None, name: str) -> T:
    if obj is None:
        raise RuntimeError(f"Could not build {name}")
    return obj


def get_checkpoint_path(
    trainer: DummyBaseTrainer,
    config_path: str | Path,
    ckpt_path: str | Path | None,
) -> Path:
    if ckpt_path is not None:
        ckpt_path = Path(ckpt_path)
        if ckpt_path.exists():
            return ckpt_path
        logger.warning("Could not find the passed checkpoint at %s", ckpt_path)

    # Tries loading the checkpoint that the trainer thinks exists.
    ckpt_path = trainer.get_ckpt_path()
    if ckpt_path.exists():
        return ckpt_path
    logger.warning("Could not find trainer checkpoint at %s", ckpt_path)

    # Tries loading other checkpoints.
    ckpt_path = trainer.exp_dir / "ckpt.pt"
    if ckpt_path.exists():
        return ckpt_path
    logger.warning("Could not find checkpoint at %s", ckpt_path)

    # Searches for a checkpoint in the same directory as the config.
    config_path = Path(config_path)
    ckpt_paths = list(config_path.parent.rglob("ckpt*.pt"))
    if ckpt_paths:
        return max(ckpt_paths, key=lambda p: p.stat().st_mtime)
    logger.warning("Could not find checkpoints in config directory %s", config_path.parent)

    raise RuntimeError("Could not find a checkpoint to load")


def load_model_and_task(
    config_path: str | Path,
    ckpt_path: str | Path | None = None,
    to_device: bool = True,
) -> tuple[BaseModel, BaseTask]:
    """Loads a trained checkpoint from a config, and optional checkpoint path.

    Args:
        config_path: The path to the config file.
        ckpt_path: The path to the checkpoint file; if None, the latest
            checkpoint will be used. This defaults to first checking in an
            adjacent `checkpoints` directory for a `ckpt.pt` file, or else
            checking for the checkpoint file in the same directory as the
            config.
        to_device: Whether to move the model to the device specified in the
            config.

    Returns:
        The model and task loaded from the checkpoint
    """

    with Timer("loading checkpoint"):
        config = cast(DictConfig, OmegaConf.load(config_path))
        model = check_built(register_model.build_entry(config), "model")
        task = check_built(register_task.build_entry(config), "task")
        trainer = DummyBaseTrainer(config)

        # Uses the dummy trainer to load the checkpoint.
        ckpt_path = get_checkpoint_path(trainer, config_path, ckpt_path)
        trainer.load_checkpoint(ckpt_path, task, model)

        if to_device:
            device = AutoDevice.detect_device()
            device.module_to(model)
            device.module_to(task)

    return model, task
