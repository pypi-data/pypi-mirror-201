from pathlib import Path

from .custom_sample_data import CustomSampleData
from ..local_sample import LocalSample


class LocalCustomSample(LocalSample[CustomSampleData]):

    def load(self) -> CustomSampleData:
        return CustomSampleData(Path(self.path))
