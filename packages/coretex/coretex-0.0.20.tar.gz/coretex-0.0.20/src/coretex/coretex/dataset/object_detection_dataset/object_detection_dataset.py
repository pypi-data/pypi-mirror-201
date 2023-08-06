from typing import Dict

from ..image_dataset import ImageDataset
from ...sample import ObjectDetectionSample
from ....codable import KeyDescriptor


class ObjectDetectionDataset(ImageDataset[ObjectDetectionSample]):

    @classmethod
    def _keyDescriptors(cls) -> Dict[str, KeyDescriptor]:
        descriptors = super()._keyDescriptors()
        descriptors["samples"] = KeyDescriptor("sessions", ObjectDetectionSample, list)

        return descriptors
