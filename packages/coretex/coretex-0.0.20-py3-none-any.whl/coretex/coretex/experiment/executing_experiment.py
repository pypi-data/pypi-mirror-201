from __future__ import annotations

from typing import Final, Optional, Type, TypeVar, Generic

import os
import json
import logging

from .experiment import Experiment
from ..space import SpaceTask
from ..dataset import NetworkDataset, CustomDataset, ImageSegmentationDataset, ObjectDetectionDataset


class ExperimentBuilder:

    def __init__(self, experimentId: int) -> None:
        self.experimentId: Final = experimentId

        self.__datasetType: Optional[Type[NetworkDataset]] = None

    def setDatasetType(self, datasetType: Optional[Type[NetworkDataset]]) -> ExperimentBuilder:
        self.__datasetType = datasetType
        return self

    def __getDatasetType(self, experiment: ExecutingExperiment) -> Type[NetworkDataset]:
        if self.__datasetType is not None:
            return self.__datasetType

        if experiment.spaceTask == SpaceTask.other:
            return CustomDataset

        if experiment.spaceTask == SpaceTask.imageSegmentation:
            return ImageSegmentationDataset

        if experiment.spaceTask == SpaceTask.objectDetection:
            return ObjectDetectionDataset

        logging.getLogger("coretexpylib").error(f">> [Coretex] SpaceTask ({experiment.spaceTask}) not supported")
        return NetworkDataset

    def build(self) -> ExecutingExperiment:
        experiment: Optional[ExecutingExperiment[NetworkDataset]] = ExecutingExperiment.fetchById(self.experimentId)
        if experiment is None:
            raise Exception(f">> [Coretex] Experiment (ID: {self.experimentId}) not found")

        if not os.path.exists("experiment.config"):
            raise FileNotFoundError(">> [Coretex] (experiment.config) file not found")

        with open("experiment.config", "r") as configFile:
            configContent = json.load(configFile)
            parameters = configContent["parameters"]

            if not isinstance(parameters, list):
                raise ValueError(">> [Coretex] Invalid experiment.config file. Property 'parameters' must be an array")

            for parameter in parameters:
                if parameter["data_type"] != "dataset":
                    continue

                experiment.parameters[parameter["name"]] = self.__getDatasetType(experiment).fetchById(parameter["value"])

        return experiment


DatasetType = TypeVar("DatasetType", bound = "NetworkDataset")


class ExecutingExperiment(Experiment, Generic[DatasetType]):

    __currentExperiment: Optional[ExecutingExperiment] = None

    @staticmethod
    def current() -> ExecutingExperiment:
        if ExecutingExperiment.__currentExperiment is None:
            raise ValueError(">> [Coretex] Tried to access current experiment, but no experiment is executing")

        return ExecutingExperiment.__currentExperiment

    @staticmethod
    def startExecuting(experimentId: int, datasetType: Optional[Type[NetworkDataset]] = None) -> ExecutingExperiment:
        if ExecutingExperiment.__currentExperiment is not None:
            raise ValueError(">> [Coretex] Tried to set current experiment, but current experiment is already set")

        ExecutingExperiment.__currentExperiment = ExperimentBuilder(experimentId).setDatasetType(datasetType).build()
        return ExecutingExperiment.current()

    @staticmethod
    def stopExecuting() -> None:
        if ExecutingExperiment.__currentExperiment is None:
            raise ValueError(">> [Coretex] Tried to deallocate current experiment, but current experiment is already deallocated")

        ExecutingExperiment.__currentExperiment = None

    @property
    def dataset(self) -> Type[DatasetType]:
        """
            If there is no parameter with name "dataset" calling this will raise an exception

            Returns:
            Dataset object if there was a parameter with name "dataset" entered when the experiment was started
        """
        return self.parameters["dataset"]  # type: ignore
