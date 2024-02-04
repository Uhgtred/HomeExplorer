#!/usr/bin/env python3
# @author: Markus Kösters

from abc import ABC, abstractmethod
import numpy


class SerializerInterface(ABC):

    @abstractmethod
    def serialize(self, imageData: numpy.ndarray) -> bytes:
        """
        Interface for serialization of image-arrays.
        :param imageData: Array containing image-data that will be serialized.
        """
        pass

