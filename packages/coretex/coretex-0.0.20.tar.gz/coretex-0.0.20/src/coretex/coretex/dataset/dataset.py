from typing import Optional, TypeVar, Generic, List
from abc import ABC, abstractmethod
from pathlib import Path

from ..sample import Sample


SampleType = TypeVar("SampleType", bound = "Sample")


class Dataset(ABC, Generic[SampleType]):

    name: str
    samples: List[SampleType]

    @property
    def count(self) -> int:
        """
            Returns:
            Number of samples in this dataset
        """

        return len(self.samples)

    @property
    @abstractmethod
    def path(self) -> Path:
        pass

    @abstractmethod
    def download(self, ignoreCache: bool = False) -> None:
        pass

    def add(self, sample: SampleType) -> bool:
        """
            Adds the specified sample into the dataset, only
            if the dataset is not locked or deleted and if the sample
            is not deleted

            Parameters:
            sample: SampleType -> sample which should be added into the dataset

            Returns:
            True if sample was added, False if sample was not added
        """

        self.samples.append(sample)
        return True

    def rename(self, name: str) -> bool:
        """
            Renames the dataset, only if the dataset
            is not locked, or if the provided name is
            different from the current name

            Parameters:
            name: str -> new dataset name

            Returns:
            True if dataset was renamed, False if dataset was not renamed
        """

        if self.name == name:
            return False

        self.name = name
        return True

    def getSample(self, name: str) -> Optional[SampleType]:
        for sample in self.samples:
            # startswith must be used since if we import sample
            # with the same name twice, the second one will have
            # suffix with it's serial number
            if sample.name.startswith(name):
                return sample

        return None
