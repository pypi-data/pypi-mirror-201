from pathlib import Path

from .base import BaseCustomDataset
from ..local_dataset import LocalDataset
from ...sample import LocalCustomSample


class LocalCustomDataset(BaseCustomDataset, LocalDataset[LocalCustomSample]):

    def __init__(self, path: Path) -> None:
        super().__init__(path, LocalCustomSample)
