from typing import Final, Type
from typing_extensions import Self

import sys
import logging

from ..coretex import Experiment
from ..folder_management import FolderManager
from ..logging import LogHandler


class ProjectCallback:

    def __init__(self, experiment: Experiment) -> None:
        self._experiment: Final = experiment

    @classmethod
    def create(cls, experimentId: int) -> Self:
        experiment = Experiment.fetchById(experimentId)
        if experiment is None:
            raise ValueError

        return cls(experiment)

    def onStart(self) -> None:
        pass

    def onSuccess(self) -> None:
        pass

    def onException(self, exception: BaseException) -> None:
        pass

    def onNetworkConnectionLost(self) -> None:
        FolderManager.instance().clearTempFiles()

        sys.exit()

    def onCleanUp(self) -> None:
        logging.getLogger("coretexpylib").info("Experiment execution finished")
        LogHandler.instance().flushLogs()
        LogHandler.instance().reset()

        FolderManager.instance().clearTempFiles()
