#!/usr/bin/env python3
# @author: Markus Kösters

from BusTransactions import Bus
from Video.Camera import CameraInterface


class VideoController:

    def __init__(self):
        self.__camera = None
        self.__filtering = None
        self.__compression = None
        self.__transmission = None

    def setCamera(self, camera: CameraInterface) -> None:
        """
        Setter-Method for the camera interface.
        :param camera: Camera interface that will be used to read video data.
        """
        self.__camera = camera

    def setFiltering(self, filtering: VideoFiltering) -> None:
        """
        Setter-Method for the filtering of video data.
        :param filtering: Filter that will be applied to the video data.
        """
        self.__filtering = filtering

    def setCompression(self, compression: Compression) -> None:
        """
        Setter-Method for the compression of video data.
        :param compression: Compression that will be used to compress video data.
        """
        self.__compression = compression

    def setTransmission(self, transmission: Bus) -> None:
        """
        Setter-Method for the transmission or storage of video data.
        :param transmission: Can be a transmitting or storage object.
        """
        self.__transmission = transmission
