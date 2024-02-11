#!/usr/bin/env python3
# @author: Markus Kösters

from BusTransactions import Bus
from Video.Camera import CameraInterface
from Video.Serialization import SerializerInterface
from Video.VideoTransmission import VideoTransmitter


class VideoController:

    def __init__(self):
        self.__camera = None
        self.__filtering = None
        self.__serialization = None
        self.__compression = None
        self.__transmission = None

    def setCamera(self, camera: CameraInterface) -> None:
        """
        Setter-Method for the camera interface.
        :param camera: Camera interface that will be used to read video data.
        """
        self.__camera = camera

    def setSerialization(self, serialization: SerializerInterface) -> None:
        """
        Sets the serialization strategy for the VideoController.

        The method sets the SerializerInterface (serialization strategy) object,
        which will be used by the VideoController to serialize data.

        :param serialization: The serialization object to be used by the VideoController.
        """
        self.__serialization = serialization

    # def setFiltering(self, filtering: VideoFiltering) -> None:
    #     """
    #     Setter-Method for the filtering of video data.
    #     :param filtering: Filter that will be applied to the video data.
    #     """
    #     self.__filtering = filtering
    #
    # def setCompression(self, compression: Compression) -> None:
    #     """
    #     Setter-Method for the compression of video data.
    #     :param compression: Compression that will be used to compress video data.
    #     """
    #     self.__compression = compression

    def setTransmission(self, transmission: VideoTransmitter) -> None:
        """
        Setter-Method for the transmission or storage of video data.
        :param transmission: Can be a transmitting or storage object.
        """
        self.__transmission = transmission
