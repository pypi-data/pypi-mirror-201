from typing import Final, Optional, Any, List, Dict, Union
from typing_extensions import Self
from threading import Lock
from zipfile import ZipFile
from pathlib import Path

import os
import logging
import zipfile

from .status import ExperimentStatus
from .artifact import Artifact
from ..space import SpaceTask
from ...codable import KeyDescriptor
from ...networking import NetworkManager, NetworkObject, RequestType
from ...folder_management import FolderManager


class Experiment(NetworkObject):

    """
        Represents the Experiment object from Coretex.ai
    """

    __statusUpdateLock: Final = Lock()

    datasetId: int
    name: str
    description: str
    meta: Dict[str, Any]
    status: ExperimentStatus
    spaceId: int
    spaceName: str
    spaceTask: SpaceTask
    projectId: int
    projectName: str
    createdById: str
    useCachedEnv: bool

    def __init__(self) -> None:
        super(Experiment, self).__init__()

        self.__lastStatusMessage: Optional[str] = None
        self.__parameters: Dict[str, Any] = {}

    @property
    def parameters(self) -> Dict[str, Any]:
        return self.__parameters

    @property
    def projectPath(self) -> str:
        return FolderManager.instance().getTempFolder(str(self.id))

    # Codable overrides

    @classmethod
    def _keyDescriptors(cls) -> Dict[str, KeyDescriptor]:
        descriptors = super()._keyDescriptors()

        descriptors["status"] = KeyDescriptor("status", ExperimentStatus)
        descriptors["spaceId"] = KeyDescriptor("project_id")
        descriptors["spaceName"] = KeyDescriptor("project_name")
        descriptors["spaceTask"] = KeyDescriptor("project_task", SpaceTask)
        descriptors["projectId"] = KeyDescriptor("sub_project_id")
        descriptors["projectName"] = KeyDescriptor("sub_project_name")

        # private properties of the object should not be encoded
        descriptors["__lastStatusMessage"] = KeyDescriptor(isEncodable = False)
        descriptors["__parameters"] = KeyDescriptor(isEncodable = False)

        return descriptors

    # NetworkObject overrides

    @classmethod
    def _endpoint(cls) -> str:
        return "model-queue"

    def onDecode(self) -> None:
        super().onDecode()

        if self.meta["parameters"] is None:
            self.meta["parameters"] = []

        parameters = self.meta["parameters"]

        if not isinstance(parameters, list):
            raise ValueError

        for p in parameters:
            self.__parameters[p["name"]] = p["value"]

    # Experiment methods

    def updateStatus(self, status: ExperimentStatus, message: Optional[str] = None, notifyServer: bool = True) -> bool:
        """
            Updates Experiment status

            Parameters:
            status: ExperimentStatus -> ExperimentStatus type
            message: Optional[str] -> Descriptive message for experiment status
        """

        with Experiment.__statusUpdateLock:
            if message is None:
                message = status.defaultMessage

            assert(len(message) > 10)  # Some information needs to be sent to Coretex.ai
            self.status = status
            self.__lastStatusMessage = message

            parameters: Dict[str, Any] = {
                "id": self.id,
                "status": status.value,
                "status_message": message
            }

            if notifyServer:
                # TODO: Should API rename this too?
                endpoint = "model-queue/job-status-update"
                response = NetworkManager.instance().genericJSONRequest(
                    endpoint = endpoint,
                    requestType = RequestType.post,
                    parameters = parameters
                )

                if response.hasFailed():
                    logging.getLogger("coretexpylib").error(">> [Coretex] Error while updating experiment status")

                return not response.hasFailed()

            return True

    def getLastStatusMessage(self) -> Optional[str]:
        return self.__lastStatusMessage

    def downloadProject(self) -> bool:
        """
            Download project

            Returns:
            True if project downloaded successfully, False if project download has failed
        """

        zipFilePath = f"{self.projectPath}.zip"

        response = NetworkManager.instance().genericDownload(
            endpoint=f"workspace/download?model_queue_id={self.id}",
            destination=zipFilePath
        )

        with ZipFile(zipFilePath) as zipFile:
            zipFile.extractall(self.projectPath)

        # remove zip file after extract
        os.unlink(zipFilePath)

        if response.hasFailed():
            logging.getLogger("coretexpylib").info(">> [MLService] Project download has failed")

        return not response.hasFailed()

    def createArtifact(self, localFilePath: str, remoteFilePath: str, mimeType: Optional[str] = None) -> Optional[Artifact]:
        return Artifact.create(self.id, localFilePath, remoteFilePath, mimeType)

    def createQiimeArtifact(self, rootArtifactFolderName: str, qiimeArtifactPath: Path) -> None:
        if not zipfile.is_zipfile(qiimeArtifactPath):
            raise ValueError(">> [Coretex] Not an archive")

        localFilePath = str(qiimeArtifactPath)
        remoteFilePath = f"{rootArtifactFolderName}/{qiimeArtifactPath.name}"

        mimeType: Optional[str] = None
        if qiimeArtifactPath.suffix in [".qza", ".qzv"]:
            mimeType = "application/zip"

        artifact = self.createArtifact(localFilePath, remoteFilePath, mimeType)
        if artifact is None:
            logging.getLogger("coretexpylib").warning(f">> [Coretex] Failed to upload {localFilePath} to {remoteFilePath}")

        # TODO: Enable when uploading file by file is not slow anymore
        # tempDir = Path(FolderManager.instance().createTempFolder(rootArtifactFolderName))
        # fileUtils.recursiveUnzip(qiimeArtifactPath, tempDir, remove = False)

        # for path in fileUtils.walk(tempDir):
        #     relative = path.relative_to(tempDir)

        #     localFilePath = str(path)
        #     remoteFilePath = f"{rootArtifactFolderName}/{str(relative)}"

        #     logging.getLogger("coretexpylib").debug(f">> [Coretex] Uploading {localFilePath} to {remoteFilePath}")

        #     artifact = self.createArtifact(localFilePath, remoteFilePath)
        #     if artifact is None:
        #         logging.getLogger("coretexpylib").warning(f">> [Coretex] Failed to upload {localFilePath} to {remoteFilePath}")

    @classmethod
    def startCustomExperiment(
        cls,
        datasetId: int,
        projectId: int,
        nodeId: Union[int, str],
        name: Optional[str],
        description: Optional[str] = None,
        parameters: Optional[List[Dict[str, Any]]] = None
    ) -> Optional[Self]:

        if isinstance(nodeId, int):
            nodeId = str(nodeId)

        if parameters is None:
            parameters = []

        response = NetworkManager.instance().genericJSONRequest(
            f"{cls._endpoint()}/custom",
            RequestType.post,
            parameters={
                "dataset_id": datasetId,
                "sub_project_id": projectId,
                "service_id": nodeId,
                "name": name,
                "description": description,
                "parameters": parameters
            }
        )

        if response.hasFailed():
            return None

        return cls.decode(response.json[0])
