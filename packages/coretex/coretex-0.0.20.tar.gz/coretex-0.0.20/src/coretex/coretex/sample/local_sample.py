from typing import TypeVar, Generic, Final
from pathlib import Path

import logging

from .sample import Sample


SampleDataType = TypeVar("SampleDataType")


class LocalSample(Generic[SampleDataType], Sample[SampleDataType]):

    def __init__(self, path: Path) -> None:
        super().__init__()

        self.name: Final = path.stem
        self._path: Final = path

    @property
    def path(self) -> str:
        return str(self._path.parent / self._path.stem)

    @property
    def zipPath(self) -> str:
        return str(self._path)

    def download(self, ignoreCache: bool = False) -> bool:
        logging.getLogger("coretexpylib").warning(">> [Coretex] Local sample cannot be downloaded")
        return True

    def load(self) -> SampleDataType:
        return super().load()  # type: ignore
