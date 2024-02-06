#!/usr/bin/env python3
# @author: Markus Kösters

import numpy

from Robot.Video.VideoTransmission.Serialization.SerializerInterface import SerializerInterface
from ...BusTransactions import Bus


class VideoTransmitter:

    def __init__(self, serializer: SerializerInterface, bus: Bus):
        self.__serializer = serializer
        self.__bus = bus

    def transmit(self, image: numpy.ndarray) -> None:
        """
        Protocol for the image transmission to make sure the data is serialized before sending.
        :param image: Image that will be transmitted. Needs to be serialized before.
        """
        self.__bus.writeSingleMessage(self.__serializer.serialize(image))

