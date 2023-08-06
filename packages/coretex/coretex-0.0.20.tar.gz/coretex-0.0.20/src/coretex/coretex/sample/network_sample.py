from typing import Any, Type, TypeVar, Optional, Generic, Dict
from typing_extensions import Self

import os

from .sample import Sample
from ..space import SpaceTask
from ...codable import KeyDescriptor
from ...networking import NetworkObject, NetworkManager
from ...folder_management import FolderManager
from ...utils import guessMimeType


SampleDataType = TypeVar("SampleDataType")


class NetworkSample(Generic[SampleDataType], Sample[SampleDataType], NetworkObject):

    """
        Represents the Sample object from Coretex.ai
    """

    isLocked: bool
    spaceTask: SpaceTask

    @property
    def path(self) -> str:
        return os.path.join(FolderManager.instance().samplesFolder, str(self.id))

    @property
    def zipPath(self) -> str:
        return f"{self.path}.zip"

    @classmethod
    def _keyDescriptors(cls) -> Dict[str, KeyDescriptor]:
        descriptors = super()._keyDescriptors()
        descriptors["spaceTask"] = KeyDescriptor("project_task", SpaceTask)

        return descriptors

    @classmethod
    def _endpoint(cls) -> str:
        return "session"

    @classmethod
    def _genericSampleImport(
        cls,
        endpoint: str,
        parameters: Dict[str, Any],
        filePath: str,
        mimeType: Optional[str] = None
    ) -> Optional[Self]:

        if mimeType is None:
            mimeType = guessMimeType(filePath)

        with open(filePath, "rb") as sampleFile:
            files = [
                ("file", ("file", sampleFile, mimeType))
            ]

            response = NetworkManager.instance().genericUpload(f"items/{endpoint}", files, parameters)
            if response.hasFailed():
                return None

            return cls.decode(response.json)

    def download(self, ignoreCache: bool = False) -> bool:
        if os.path.exists(self.zipPath) and not ignoreCache:
            return True

        response = NetworkManager.instance().genericDownload(
            endpoint = f"{self.__class__._endpoint()}/export?id={self.id}",
            destination = self.zipPath
        )

        return not response.hasFailed()

    def load(self) -> SampleDataType:
        return super().load()  # type: ignore
