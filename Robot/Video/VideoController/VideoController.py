#!/usr/bin/env python3
# @author: Markus Kösters
from Robot.Video.Camera import CameraInterface


class VideoController:

    def __init__(self):
        self.__camera = None
        self.__filtering = None
        self.__compression = None
        self.__transmission = None

    def setCamera(self, camera: CameraInterface) -> None:
        self.__camera = camera

    def setFiltering(self, filtering) -> None:
        self.__filtering = filtering

    def setCompression(self, compression) -> None:
        self.__compression = compression

    def setTransmission(self, transmission) -> None:
        self.__transmission = transmission
