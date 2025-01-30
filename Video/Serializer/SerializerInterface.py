#!/usr/bin/env python3
# @author: Markus Kösters

from abc import ABC, abstractmethod
import numpy


class SerializerInterface(ABC):

    """
    Todo: this interface obviously does not make that much sense, when I have to adapt it for every class. I shoult think about keeping it or throwing it away.
            Maybe make SerializerFacade that handles the serialization of all data-types. Or is that overcomplicated?
    """

    @abstractmethod
    def serializeFile(self, imageData: numpy.ndarray) -> str:
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

def __init_subclass__(cls):
    super().__init_subclass__()
    if cls.methodA is SerializerInterface.methodA and cls.methodB is SerializerInterface.methodB:
        raise TypeError(
            f"{cls.__name__} must override at least one of 'methodA' or 'methodB'"
        )