from pathlib import Path
from zipfile import ZipFile

import json
import os

from .image_sample_data import AnnotatedImageSampleData
from ..local_sample import LocalSample
from ...annotation import CoretexImageAnnotation


class LocalImageSample(LocalSample[AnnotatedImageSampleData]):

    def load(self) -> AnnotatedImageSampleData:
        return AnnotatedImageSampleData(Path(self.path))

    def saveAnnotation(self, coretexAnnotation: CoretexImageAnnotation) -> bool:
        with open(Path(self.path) / "annotations.json", "w") as file:
            json.dump(coretexAnnotation.encode(), file)

        zipPath = Path(self.zipPath)

        oldZipPath = zipPath.parent / f"{zipPath.stem}-old.zip"
        zipPath.rename(oldZipPath)

        with ZipFile(zipPath, "w") as zipFile:
            path = Path(self.path)
            for element in os.listdir(path):
                zipFile.write(path / element, arcname = element)

        oldZipPath.unlink()
        return True
