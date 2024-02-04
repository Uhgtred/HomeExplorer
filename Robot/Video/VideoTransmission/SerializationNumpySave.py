#!/usr/bin/env python3
# @author: Markus Kösters

import io
import numpy

from .SerializerInterface import SerializerInterface


class SerializationNumpySave(SerializerInterface):

    __memoryFile = io.BytesIO()

    def serialize(self, imageData: numpy.ndarray) -> bytes:
        """
        Method for serialization of imageData.
        :param imageData: Image data as numpy array that will be serialized.
        :return: Serialized numpy array (image data).
        """
        numpy.save(self.__memoryFile, imageData)
        return self.__memoryFile.getvalue()
