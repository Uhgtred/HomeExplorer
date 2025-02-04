#!/usr/bin/env python3
# @author: Markus Kösters

from BusTransactions import Bus
from BusTransactions.BusFactory import BusFactory


class VideoTransmitter:
    """
    The VideoTransmitter class is responsible for transmitting video frames over a specified bus.
    """

    """
    Todo: Is this class still needed?
    """

    def __init__(self, port: int, host: bool = False):
        """
        Initializes the VideoTransmitter with a serializer and bus.
        :param bus: The bus used to transmit the serialized video frames.
        """
        self.__bus = BusFactory.produceUDP_Transceiver(port, host, noEncoding=True)

    def transmit(self, frameData: bytes) -> None:
        """
        Protocol for the image transmission. It ensures the image data is read from the file (which is already serialized)
        and then sent over the bus.
        :param frameData: Image data to be transmitted.
        """
        print(len(frameData))
        self.__bus.writeSingleMessage(frameData)

    @staticmethod
    def __readImageFileData(imageFilePath: str) -> bytes:
        """
        Method that reads the data from the image file, which is a serialized numpy array representing a video frame.
        :param imageFilePath: str - Absolute path to the image file.
        :return: bytes - Data read from the image file.
        """
        with open(imageFilePath, 'rb') as f:
            return f.read()
