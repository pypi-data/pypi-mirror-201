from typing import Any, Dict, List, Tuple, Optional

import json
import logging
import traceback

from tap import Tap

from .heartbeat import Heartbeat
from .base import ProjectCallback
from ..coretex import Experiment, ExperimentStatus
from ..networking import NetworkManager


class LocalProjectCallback(ProjectCallback):

    def onStart(self) -> None:
        super().onStart()

        logging.getLogger("coretexpylib").info("Heartbeat started")

        heartbeat = Heartbeat()
        heartbeat.start()

    def onSuccess(self) -> None:
        super().onSuccess()

        self._experiment.updateStatus(ExperimentStatus.completedWithSuccess)

    def onException(self, exception: BaseException) -> None:
        super().onException(exception)

        self._experiment.updateStatus(ExperimentStatus.completedWithError)

        exceptionStackTrace = "".join(traceback.format_exception(
            type(exception),
            exception,
            exception.__traceback__
        ))

        for line in exceptionStackTrace.split("\n"):
            if len(line.strip()) == 0:
                continue

            logging.getLogger("coretexpylib").fatal(line)


class LocalArgumentParser(Tap):

    username: str
    password: str

    datasetId: int
    projectId: int
    name: Optional[str]
    description: Optional[str]

    def configure(self) -> None:
        self.add_argument("--username", type = str)
        self.add_argument("--password", type = str)

        self.add_argument("--datasetId", type = int)
        self.add_argument("--projectId", type = int)
        self.add_argument("--name", nargs = "?", type = str, default = None)
        self.add_argument("--description", nargs = "?", type = str, default = None)


def loadLocalParameters() -> List[Dict[str, Any]]:
    with open("experiment.config", "r") as configFile:
        configContent = json.load(configFile)

        if "parameters" in configContent:
            parameters: List[Dict[str, Any]] = configContent["parameters"]

    return parameters


def processLocal() -> Tuple[int, ProjectCallback]:
    parser = LocalArgumentParser().parse_args()

    response = NetworkManager.instance().authenticate(parser.username, parser.password)
    if response.hasFailed():
        raise RuntimeError(">> [Coretex] Failed to authenticate")

    parameters = loadLocalParameters()

    experiment = Experiment.startCustomExperiment(
        parser.datasetId,
        parser.projectId,
        # Dummy Local node ID, hardcoded as it is only a temporary solution,
        # backend will add a new ExperimentType (local) which does not require a specific
        # node to run
        43,
        parser.name,
        parser.description,
        parameters=parameters
    )

    if experiment is None:
        raise RuntimeError(">> [Coretex] Failed to create experiment")

    experiment.updateStatus(ExperimentStatus.preparingToStart)

    return experiment.id, LocalProjectCallback(experiment)
