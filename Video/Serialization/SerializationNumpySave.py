#!/usr/bin/env python3
# @author: Markus Kösters

import numpy

from .SerializerConfig import SerializerConfig
from .SerializerInterface import SerializerInterface


class SerializationNumpySave(SerializerInterface):
    """
    Class for serializing numpy array before sending it through socket.
    """

    def __init__(self, config: SerializerConfig):
        self.__imageFile = config.storageFile

    def serialize(self, imageData: numpy.ndarray) -> bytes:
        """
        Method for serialization of imageData.
        :param imageData: Image data as numpy array that will be serialized.
        :return: Serialized numpy array (image data).
        Todo: implement this! Maybe this needs to be done in c++ for better performance.
        """
        numpy.save(self.__imageFile, imageData)

        return pass
