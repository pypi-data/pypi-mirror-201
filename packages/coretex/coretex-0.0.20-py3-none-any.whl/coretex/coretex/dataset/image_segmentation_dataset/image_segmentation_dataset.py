from typing import Dict

from ..image_dataset import ImageDataset
from ...sample import ImageSegmentationSample
from ....codable import KeyDescriptor


class ImageSegmentationDataset(ImageDataset[ImageSegmentationSample]):

    @classmethod
    def _keyDescriptors(cls) -> Dict[str, KeyDescriptor]:
        descriptors = super()._keyDescriptors()
        descriptors["samples"] = KeyDescriptor("sessions", ImageSegmentationSample, list)

        return descriptors
