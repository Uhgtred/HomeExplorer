#!/usr/bin/env python3
# @author: Markus Kösters

from abc import ABC, abstractmethod
import numpy


class SerializerInterface(ABC):

    @abstractmethod
    def serialize(self, imageData: numpy.ndarray) -> str:
        """
        Interface for serialization of image-arrays.
        :param imageData: Array containing image-data that will be serialized.
        :return: File-path of serialized image.
        """

    @abstractmethod
    def deserialize(self, imageData: bytes) -> numpy.ndarray:
        """
        Interface for deserialization of image-data.
        :param imageData: Serialized image-data.
        :return: np.ndarray containing image-data.
        """

