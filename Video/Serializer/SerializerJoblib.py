#!/usr/bin/env python3
# @author: Markus Kösters

import fileinput
import os

import joblib
import numpy

from .SerializerConfig import SerializerConfig
from .SerializerInterface import SerializerInterface


class SerializerJoblib(SerializerInterface):
    """
    Class for serializing numpy array before sending it through socket.
    """

    def __init__(self, config: SerializerConfig):
        self.__imageFile = config.storageFile

    def serialize(self, imageFrame: numpy.ndarray) -> str:
        """
        Method for serialization of imageData.
        :param imageFrame: Image data as numpy array that will be serialized.
        :return: Serialized numpy array (image data).
        """
        joblib.dump(imageFrame, self.__imageFile)
        # returning absolute filepath of the image-file
        return os.path.abspath(self.__imageFile)

    def deserialize(self, filePath: str) -> numpy.ndarray:
        """
            Method to load a numpy array from a file
            :param filePath: The path of the file to load the numpy array from.
            :return: The loaded numpy array.
            """
        return joblib.load(filePath)

