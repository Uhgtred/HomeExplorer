#!/usr/bin/env python3
# @author: Markus Kösters

from Video.VideoController import VideoController


class VideoControllerBuilder:

    def __init__(self):
        self.videoController = VideoController()
        self.__camera = None
        self.__filtering = None
        self.__serialization = None
        self.__compression = None
        self.__transmission = None

    def addCamera(self, camera) -> any:
        self.videoController.setCamera(camera)
        return self

    # def addFiltering(self, filtering) -> any:
    #     self.videoController.setFiltering(filtering)
    #     return self

    def addSerialization(self, serialization) -> any:
        self.videoController.setSerialization(serialization)
        return self

    # def addCompression(self, compression) -> any:
    #     self.videoController.setCompression(compression)
    #     return self

    def addTransmission(self, transmission) -> any:
        self.videoController.setTransmission(transmission)
        return self

    def build(self) -> VideoController:
        return self.videoController
