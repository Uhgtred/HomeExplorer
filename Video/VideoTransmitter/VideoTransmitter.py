#!/usr/bin/env python3
# @author: Markus Kösters

import logging

from BusTransactions.BusFactory import BusFactory
from Video.VideoTransmitter.VideoTransmitterInterface import VideoTransmitterInterface


class VideoTransmitter(VideoTransmitterInterface):
    """
    The VideoTransmitter class is responsible for transmitting video frames over a specified bus.
    """

    """
    Todo:   Is this class still needed? Maybe it would be possible to use the BusTransactions module and overwrite the encoding with serialization.
            Or even use the BusTransactions module directly and set the serializer to match the encoding. But by doing this the possib
            ilities to compress the frames would be lost as well. Except I also integrate the compression into the serializer of the BusTransactions module.
            This would be a major change though and also goes against the separation of concerns. So I will leave it like this for now. 
            Best solution would probably be to integrate a compression into the BusTransactions. This would require the BusFactory to become a BusBuilder instead.
            Ontop the implementation and the concept for the compression inside the BusTransactions-package would be needed.
    """

    def __init__(self, bus: BusFactory.produceUDP_Transceiver):
        """
        Initializes the VideoTransmitter with a serializer and bus.
        :param bus: The bus used to transmit the serialized video frames.
        """
        # Initializing a logger. The loglevel can globally be set in ProjectLogging.Logger.
        self.__logger: logging.Logger = logging.getLogger(__name__)
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

