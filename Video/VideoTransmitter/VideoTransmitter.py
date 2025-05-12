#!/usr/bin/env python3
# @author: Markus Kösters

import ProjectLogging

from BusTransactions.BusInterface import BusInterface
from Video.VideoTransmitter.VideoTransmitterInterface import VideoTransmitterInterface


class VideoTransmitter(VideoTransmitterInterface):
    """
    The VideoTransmitter class is responsible for transmitting video frames over a specified bus.
    It is not implementing the Video transmission itself but wraps an existing bus with an Interface.
    """
    __logger: ProjectLogging.Logger.getLogger = ProjectLogging.Logger('VideoTransmitter',
                                                                      'VideoTransmitter.log').getLogger

    def __init__(self, bus: BusInterface):
        """
        Initializes the VideoTransmitter with a serializer and bus.
        :param bus: The bus used to transmit the serialized video frames.
        """
        # Initializing a logger. The loglevel can globally be set in ProjectLogging.Logger.
        self.__bus = bus
        self.__logger.debug(f"VideoTransmitter-bus is: {self.__bus}")

    def transmit(self, frameData: bytes) -> None:
        """
        Protocol for the image transmission. It ensures the image data is read from the file (which is already serialized)
        and then sent over the bus.
        :param frameData: Image data to be transmitted.
        """
        self.__logger.debug(f"Transmitting video frame of type: {type(frameData)}\t and size: {len(frameData)}.")
        self.__bus.writeSingleMessage(frameData)

