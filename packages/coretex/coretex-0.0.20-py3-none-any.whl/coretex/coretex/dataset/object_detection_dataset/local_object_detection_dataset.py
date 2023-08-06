from pathlib import Path

from ..image_dataset import LocalImageDataset
from ...sample import LocalObjectDetectionSample


class LocalObjectDetectionDataset(LocalImageDataset[LocalObjectDetectionSample]):

    def __init__(self, path: Path) -> None:
        super().__init__(path, LocalObjectDetectionSample)
