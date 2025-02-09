#!/usr/bin/env python3
# @author: Markus Kösters

from abc import ABC, abstractmethod
import numpy


class SerializerInterface(ABC):

    @abstractmethod
    def serialize(self, imageData: numpy.ndarray = None, filePath: str = '') -> any:
        """
        Interface for serialization of image-arrays. Selectable whether to use the image-data or a file-path.
        Please start your implementation with super().serialize(...) to correctly handle exceptions.
        :param imageData: Array containing image-data that will be serialized.
        :param filePath: File path of the image-file that will be serialized.
        :return: Bytes containing serialized image-data.
        """
        if imageData is None and filePath == '':
            raise ValueError("Either imageData or filePath has to be provided.")

    @abstractmethod
    def deserialize(self, imageData: bytes) -> numpy.ndarray:
        """
        Interface for deserialization of image-data.
        :param imageData: Serialized image-data.
        :return: np.ndarray containing image-data.
        """
