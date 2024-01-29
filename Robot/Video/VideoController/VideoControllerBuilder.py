#!/usr/bin/env python3
# @author: Markus Kösters

from Robot.BusTransactions import BusPluginInterface
from Robot.Video.VideoController.VideoController import VideoController


class VideoControllerBuilder:

    def __init__(self):
        self.videoController = VideoController()
        self.__camera = None
        self.__filtering: Filtering = None
        self.__compression: VideoCompression = None
        self.__transmission: BusPluginInterface | FileStorage = None

    def addCamera(self, camera):
        self.videoController.setCamera(camera)
        return self

    def addFiltering(self, filtering):
        self.videoController.setFiltering(filtering)
        return self

    def addCompression(self, compression):
        self.videoController.setCompression(compression)
        return self

    def addTransmission(self, transmission) -> VideoControllerBuilder:
        self.videoController.setTransmission(transmission)
        return self

    def build(self) -> VideoController:
        return self.videoController
