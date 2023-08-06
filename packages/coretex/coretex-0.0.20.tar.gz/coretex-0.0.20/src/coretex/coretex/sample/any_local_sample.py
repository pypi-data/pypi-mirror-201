from typing import TypeVar

from .local_sample import LocalSample


SampleDataType = TypeVar("SampleDataType")


class AnyLocalSample(LocalSample[SampleDataType]):

    @property
    def path(self) -> str:
        return str(self._path)

    @property
    def zipPath(self) -> str:
        return str(self._path)
