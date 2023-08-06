from typing import TypeVar, Generic, Union
from abc import ABC, abstractmethod
from zipfile import BadZipFile, ZipFile
from pathlib import Path

import os
import shutil


SampleDataType = TypeVar("SampleDataType")


class Sample(ABC, Generic[SampleDataType]):

    """
        Represents the Sample object from Coretex.ai
    """

    name: str

    @property
    @abstractmethod
    def path(self) -> str:
        pass

    @property
    @abstractmethod
    def zipPath(self) -> str:
        pass

    @abstractmethod
    def download(self, ignoreCache: bool = False) -> bool:
        """
            Downloads the Sample if it is an instance or a subclass of NetworkSample\n
            Ignored for instances and subclasses of LocalSample

            Returns:\n
            True if Sample has been downloaded successfully, False if something went wrong\n
            In LocalSample case True is always returned
        """
        pass

    def __unzipSample(self) -> None:
        if os.path.exists(self.path):
            shutil.rmtree(self.path)

        with ZipFile(self.zipPath) as zipFile:
            zipFile.extractall(self.path)

    def unzip(self, ignoreCache: bool = False) -> None:
        if os.path.exists(self.path) and not ignoreCache:
            return

        try:
            self.__unzipSample()
        except BadZipFile:
            # Delete invalid zip file
            os.unlink(self.zipPath)

            # Re-download
            self.download()

            # Try to unzip - if it fails again it should crash
            self.__unzipSample()

    @abstractmethod
    def load(self) -> SampleDataType:
        pass

    def joinPath(self, other: Union[Path, str]) -> Path:
        if isinstance(other, str):
            other = Path(other)

        return Path(self.path) / other
