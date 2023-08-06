from typing import Optional
from typing_extensions import Self
from pathlib import Path

from .image_sample_data import AnnotatedImageSampleData
from .local_image_sample import LocalImageSample
from .image_format import ImageFormat
from ..network_sample import NetworkSample
from ...annotation import CoretexImageAnnotation
from ....networking import NetworkManager, RequestType


class ImageSample(NetworkSample[AnnotatedImageSampleData], LocalImageSample):

    def __init__(self) -> None:
        NetworkSample.__init__(self)

    @property
    def imagePath(self) -> Path:
        path = Path(self.path)

        for format in ImageFormat:
            imagePaths = list(path.glob(f"*.{format.extension}"))
            imagePaths = [path for path in imagePaths if not "thumbnail" in str(path)]

            if len(imagePaths) > 0:
                return Path(imagePaths[0])

        raise FileNotFoundError

    @property
    def annotationPath(self) -> Path:
        return Path(self.path) / "annotations.json"

    def saveAnnotation(self, coretexAnnotation: CoretexImageAnnotation) -> bool:
        super().saveAnnotation(coretexAnnotation)

        parameters = {
            "id": self.id,
            "data": coretexAnnotation.encode()
        }

        response = NetworkManager.instance().genericJSONRequest(
            endpoint = "session/save-annotations",
            requestType = RequestType.post,
            parameters = parameters
        )

        return not response.hasFailed()

    @classmethod
    def createImageSample(cls, datasetId: int, path: str) -> Optional[Self]:
        """
            Creates a new image sample with the provided dataset and path

            Parameters:
            datasetId: int -> id of dataset in which image sample will be created
            path: str -> path to the image sample

            Returns:
            The created image sample object
        """

        parameters = {
            "dataset_id": datasetId
        }

        return cls._genericSampleImport("image-import", parameters, path)
