from typing import Any, Dict
from typing_extensions import Self
from datetime import datetime
from zipfile import ZipFile

import os
import shutil
import json
import logging

from ...networking import NetworkManager, NetworkObject
from ...folder_management import FolderManager
from ...codable import KeyDescriptor


class Model(NetworkObject):

    name: str
    createdById: str
    createdOn: datetime
    datasetId: int
    spaceId: int
    projectId: int
    isTrained: bool
    isDeleted: bool
    accuracy: float
    experimentId: int
    meta: Dict[str, Any]

    @classmethod
    def modelDescriptorFileName(cls) -> str:
        return "model_descriptor.json"

    @classmethod
    def _keyDescriptors(cls) -> Dict[str, KeyDescriptor]:
        descriptors = super()._keyDescriptors()
        descriptors["experimentId"] = KeyDescriptor("model_queue_id")

        return descriptors

    @classmethod
    def createModel(cls, name: str, experimentId: int, accuracy: float, meta: Dict[str, Any]) -> Self:
        model = cls.create(parameters = {
            "name": name,
            "model_queue_id": experimentId,
            "accuracy": accuracy,
            "meta": meta
        })

        if model is None:
            raise ValueError(">> [Coretex] Failed to create Model entity")

        return model

    @classmethod
    def saveModelDescriptor(cls, path: str, contents: Dict[str, Any]) -> None:
        modelDescriptorPath = os.path.join(path, cls.modelDescriptorFileName())

        with open(modelDescriptorPath, "w", encoding = "utf-8") as file:
            json.dump(contents, file, ensure_ascii = False, indent = 4)

    def download(self) -> None:
        """
            Downloads and extracts the model zip file from Coretex.ai
        """

        if self.isDeleted or not self.isTrained:
            return

        modelZipDestination = os.path.join(FolderManager.instance().modelsFolder, f"{self.id}.zip")

        modelFolderDestination = os.path.join(FolderManager.instance().modelsFolder, f"{self.id}")
        if os.path.exists(modelFolderDestination):
            return

        os.mkdir(modelFolderDestination)

        response = NetworkManager.instance().genericDownload(
            endpoint=f"model/download?id={self.id}",
            destination=modelZipDestination
        )

        if response.hasFailed():
            logging.getLogger("coretexpylib").info(">> [Coretex] Failed to download the model")

        zipFile = ZipFile(modelZipDestination)
        zipFile.extractall(modelFolderDestination)
        zipFile.close()

    def upload(self, path: str) -> bool:
        """
            Uploads the model zip file to Coretex.ai

            Parameters:
            path: str -> Path to the saved model dir

            Returns:
            True if model data uploaded successfully, False if model data upload has failed
        """

        if self.isDeleted:
            return False

        logging.getLogger("coretexpylib").info(">> [Coretex] Uploading model file...")

        shutil.make_archive(path, "zip", path)

        files = {
            ("file", open(f"{path}.zip", "rb"))
        }

        parameters = {
            "id": self.id
        }

        response = NetworkManager.instance().genericUpload("model/upload", files, parameters)
        if response.hasFailed():
            logging.getLogger("coretexpylib").info(">> [Coretex] Failed to upload model file")
        else:
            logging.getLogger("coretexpylib").info(">> [Coretex] Uploaded model file")

        return not response.hasFailed()
