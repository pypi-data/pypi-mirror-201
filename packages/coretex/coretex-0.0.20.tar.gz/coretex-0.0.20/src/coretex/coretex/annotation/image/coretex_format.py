from typing_extensions import Self
from uuid import UUID
from typing import List, Dict, Tuple
from math import fsum, cos, sin, radians

from PIL import Image, ImageDraw
from PIL.Image import Image as ImageType
from shapely.geometry import Polygon, Point

import numpy as np

from .bbox import BBox
from .classes_format import ImageDatasetClasses
from ....codable import Codable, KeyDescriptor


SegmentationType = List[float]


def toPoly(segmentation: List[float]) -> List[Tuple[float, float]]:
    points: List[Tuple[float, float]] = []

    for index in range(0, len(segmentation) - 1, 2):
        points.append((segmentation[index], segmentation[index + 1]))

    return points


class CoretexSegmentationInstance(Codable):

    classId: UUID
    bbox: BBox
    segmentations: List[SegmentationType]

    @classmethod
    def _keyDescriptors(cls) -> Dict[str, KeyDescriptor]:
        descriptors = super()._keyDescriptors()

        descriptors["classId"] = KeyDescriptor("class_id", UUID)
        descriptors["bbox"] = KeyDescriptor("bbox", BBox)
        descriptors["segmentations"] = KeyDescriptor("annotations")

        return descriptors

    @classmethod
    def create(cls, classId: UUID, bbox: BBox, segmentations: List[SegmentationType]) -> Self:
        obj = cls()

        obj.classId = classId
        obj.bbox = bbox
        obj.segmentations = segmentations

        return obj

    def extractSegmentationMask(self, width: int, height: int) -> np.ndarray:
        image = Image.new("L", (width, height))

        for segmentation in self.segmentations:
            draw = ImageDraw.Draw(image)
            draw.polygon(toPoly(segmentation), fill = 1)

        return np.asarray(image)

    def extractBinaryMask(self, width: int, height: int) -> np.ndarray:
        binaryMask = self.extractSegmentationMask(width, height)
        binaryMask[binaryMask > 0] = 1

        return binaryMask

    def centroid(self) -> Tuple[float, float]:
        flattenedSegmentations = [element for sublist in self.segmentations for element in sublist]

        listCX = [value for index, value in enumerate(flattenedSegmentations) if index % 2 == 0]
        centerX = fsum(listCX) / len(listCX)

        listCY = [value for index, value in enumerate(flattenedSegmentations) if index % 2 != 0]
        centerY = fsum(listCY) / len(listCY)

        return centerX, centerY

    def centerSegmentations(self, newCentroid: Tuple[float, float]) -> None:
        newCenterX, newCenterY = newCentroid
        oldCenterX, oldCenterY = self.centroid()

        modifiedSegmentations: List[List[float]] = []

        for segmentation in self.segmentations:
            modifiedSegmentation: List[float] = []

            for i in range(0, len(segmentation), 2):
                x = segmentation[i] + (newCenterX - oldCenterX)
                y = segmentation[i+1] + (newCenterY - oldCenterY)

                modifiedSegmentation.append(x)
                modifiedSegmentation.append(y)

            modifiedSegmentations.append(modifiedSegmentation)

        self.segmentations = modifiedSegmentations

    def rotateSegmentations(self, degrees: int) -> None:
        rotatedSegmentations: List[List[float]] = []
        centerX, centerY = self.centroid()

        # because rotations with image and segmentations doesn't go in same direction
        # one of the rotations has to be inverted so they go in same direction
        theta = radians(-degrees) 
        cosang, sinang = cos(theta), sin(theta) 

        for segmentation in self.segmentations:
            rotatedSegmentation: List[float] = []

            for i in range(0, len(segmentation), 2):
                x = segmentation[i] - centerX
                y = segmentation[i + 1] - centerY

                newX = (x * cosang - y * sinang) + centerX
                newY = (x * sinang + y * cosang) + centerY

                rotatedSegmentation.append(newX)
                rotatedSegmentation.append(newY)

            rotatedSegmentations.append(rotatedSegmentation)

        self.segmentations = rotatedSegmentations


class CoretexImageAnnotation(Codable):

    name: str
    width: float
    height: float
    instances: List[CoretexSegmentationInstance]

    @classmethod
    def _keyDescriptors(cls) -> Dict[str, KeyDescriptor]:
        descriptors = super()._keyDescriptors()
        descriptors["instances"] = KeyDescriptor("instances", CoretexSegmentationInstance, list)

        return descriptors

    @classmethod
    def create(
        cls,
        name: str,
        width: float,
        height: float,
        instances: List[CoretexSegmentationInstance]
    ) -> Self:
        obj = cls()

        obj.name = name
        obj.width = width
        obj.height = height
        obj.instances = instances

        return obj

    def extractSegmentationMask(self, classes: ImageDatasetClasses) -> np.ndarray:
        image = Image.new("L", (self.width, self.height))

        for instance in self.instances:
            labelId = classes.labelIdForClassId(instance.classId)
            if labelId is None:
                continue

            for segmentation in instance.segmentations:
                if len(segmentation) == 0:
                    raise ValueError(f">> [Coretex] Empty segmentation")

                draw = ImageDraw.Draw(image)
                draw.polygon(toPoly(segmentation), fill = labelId + 1)

        return np.asarray(image)
