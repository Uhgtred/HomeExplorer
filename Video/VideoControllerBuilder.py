#!/usr/bin/env python3
# @author: Markus Kösters

from Video.VideoCamera import VideoCameraInterface
from Video.Serializer import SerializerInterface
from Video.VideoController import VideoController
from Video.VideoTransmitter import VideoTransmitterInterface
from Video.VideoController import VideoController


class VideoControllerBuilder:

    def __init__(self):
        self.videoController = VideoController()

    def addCamera(self, camera: VideoCameraInterface) -> any:
        self.videoController.setCamera(camera)
        return self

    # def addFiltering(self, filtering) -> any:
    #     self.videoController.setFiltering(filtering)
    #     return self

    def addSerialization(self, serialization: SerializerInterface) -> any:
        self.videoController.setSerialization(serialization)
        return self

    # def addCompression(self, compression) -> any:
    #     self.videoController.setCompression(compression)
    #     return self

    def addTransmission(self, transmission: VideoTransmitterInterface) -> any:
        self.videoController.setTransmission(transmission)
        return self

    def build(self) -> VideoController:
        return self.videoController
