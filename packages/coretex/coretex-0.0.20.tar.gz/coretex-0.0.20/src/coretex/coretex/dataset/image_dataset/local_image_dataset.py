from typing import TypeVar, Type
from pathlib import Path

import json

from .base import BaseImageDataset
from ..local_dataset import LocalDataset
from ...sample import LocalImageSample
from ...annotation import ImageDatasetClass, ImageDatasetClasses


SampleType = TypeVar("SampleType", bound = "LocalImageSample")


class LocalImageDataset(BaseImageDataset[SampleType], LocalDataset[SampleType]):  # type: ignore

    def __init__(self, path: Path, sampleClass: Type[SampleType]) -> None:
        super().__init__(path, sampleClass)

        self.classes = ImageDatasetClasses()

        if self.classesPath.exists():
            with open(path / "classes.json") as file:
                value = json.load(file)
                self.classes = ImageDatasetClasses(
                    [ImageDatasetClass.decode(element) for element in value]
                )
