from typing import Optional, Type, TypeVar, Generic, List, Dict
from typing_extensions import Self
from datetime import datetime
from pathlib import Path

import os

from .dataset import Dataset
from ..sample import NetworkSample
from ...codable import KeyDescriptor
from ...networking import NetworkObject, DEFAULT_PAGE_SIZE
from ...threading import MultithreadedDataProcessor
from ...folder_management import FolderManager


SampleType = TypeVar("SampleType", bound = "NetworkSample")


class NetworkDataset(Generic[SampleType], Dataset[SampleType], NetworkObject):
    """
        Represents the Dataset object from Coretex.ai
    """

    createdOn: datetime
    createdById: str
    isLocked: bool

    def __init__(self) -> None:
        pass

    @property
    def path(self) -> Path:
        return FolderManager.instance().datasetsFolder / str(self.id)

    # Codable overrides

    @classmethod
    def _keyDescriptors(cls) -> Dict[str, KeyDescriptor]:
        descriptors = super()._keyDescriptors()
        descriptors["samples"] = KeyDescriptor("sessions", NetworkSample, list)

        return descriptors

    # NetworkObject overrides

    @classmethod
    def _endpoint(cls) -> str:
        return "dataset"

    @classmethod
    def fetchById(cls, objectId: int, queryParameters: Optional[List[str]] = None) -> Optional[Self]:
        if queryParameters is None:
            queryParameters = ["include_sessions=1"]

        return super().fetchById(objectId, queryParameters)

    @classmethod
    def fetchAll(cls, queryParameters: Optional[List[str]] = None, pageSize: int = DEFAULT_PAGE_SIZE) -> List[Self]:
        if queryParameters is None:
            queryParameters = ["include_sessions=1"]

        return super().fetchAll(queryParameters, pageSize)

    # Dataset methods

    @classmethod
    def createDataset(cls, name: str, spaceId: int, sampleIds: Optional[List[int]] = None) -> Optional[Self]:
        """
            Creates a new dataset with the provided name, type
            and samples (if present, samples are not required)

            Parameters:
            name: str -> dataset name
            spaceId: int -> space for which the dataset will be created
            samplesIds: List[int] -> samples which should be added to dataset (if present)

            Returns:
            The created dataset object or None if creation failed
        """

        if sampleIds is None:
            sampleIds = []

        return cls.create({
            "name": name,
            "project_id": spaceId,
            "sessions": sampleIds
        })

    def download(self, ignoreCache: bool = False) -> None:
        self.path.mkdir(exist_ok = True)

        def sampleDownloader(sample: SampleType) -> None:
            downloadSuccess = sample.download(ignoreCache)
            if not downloadSuccess:
                return

            symlinkPath = self.path / f"{sample.id}.zip"
            if not symlinkPath.exists():
                os.symlink(sample.zipPath, symlinkPath)

        processor = MultithreadedDataProcessor(
            self.samples,
            sampleDownloader,
            title = "Downloading dataset"
        )

        processor.process()

    def add(self, sample: SampleType) -> bool:
        if self.isLocked or sample.isDeleted:
            return False

        success = self.update({
            "sessions": [sample.id]
        })

        if success:
            return super().add(sample)

        return success

    def rename(self, name: str) -> bool:
        success = self.update({
            "name": name
        })

        if success:
            return super().rename(name)

        return success
