from __future__ import annotations

from typing import TypeVar, Generic, Type, Generator, Optional
from pathlib import Path

import logging
import zipfile

from .dataset import Dataset
from ..sample import LocalSample, AnyLocalSample


SampleType = TypeVar("SampleType", bound = "LocalSample")
SampleGenerator = Generator[SampleType, None, None]


def _generateZippedSamples(path: Path, sampleClass: Type[SampleType]) -> Generator[SampleType, None, None]:
    for samplePath in path.glob("*"):
        if not zipfile.is_zipfile(samplePath):
            continue

        yield sampleClass(samplePath)


class LocalDataset(Generic[SampleType], Dataset[SampleType]):

    def __init__(self, path: Path, sampleClass: Type[SampleType], generator: Optional[SampleGenerator] = None) -> None:
        if generator is None:
            generator = _generateZippedSamples(path, sampleClass)

        self.__path = path

        self.name = path.stem
        self.samples = list(generator)

    @staticmethod
    def default(path: Path) -> LocalDataset:
        return LocalDataset(path, LocalSample)

    @staticmethod
    def custom(path: Path, generator: SampleGenerator) -> LocalDataset:
        return LocalDataset(path, AnyLocalSample, generator)

    @property
    def path(self) -> Path:
        return self.__path

    def download(self, ignoreCache: bool = False) -> None:
        logging.getLogger("coretexpylib").warning(">> [Coretex] Local dataset cannot be downloaded")
