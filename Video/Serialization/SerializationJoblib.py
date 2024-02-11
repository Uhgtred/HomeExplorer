#!/usr/bin/env python3
# @author: Markus Kösters

import fileinput
import joblib
import numpy

from .SerializerConfig import SerializerConfig
from .SerializerInterface import SerializerInterface


class SerializationJoblib(SerializerInterface):
    """
    Class for serializing numpy array before sending it through socket.
    """

    def __init__(self, config: SerializerConfig):
        self.__imageFile = config.storageFile

    def serialize(self, imageFrame: numpy.ndarray) -> fileinput:
        """
        Method for serialization of imageData.
        :param imageFrame: Image data as numpy array that will be serialized.
        :return: Serialized numpy array (image data).
        Todo: implement this! Maybe this needs to be done in c++ for better performance.
        """
        frameFile = self.__imageFile
        joblib.dump(imageFrame, frameFile)
        return frameFile
