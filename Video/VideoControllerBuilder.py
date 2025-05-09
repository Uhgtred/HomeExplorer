#!/usr/bin/env python3
# @author: Markus Kösters
import typing

from Video.Compressor.CompressorInterface import CompressorInterface
from Video.VideoCamera import VideoCameraInterface
from Video.Serializer import SerializerInterface
from Video.VideoTransmitter import VideoTransmitterInterface
from Video.VideoController import VideoController


class VideoControllerBuilder:

    def __init__(self):
        self.videoController = VideoController()

    def addCamera(self, camera: VideoCameraInterface) -> typing.Self:
        self.videoController.setCamera(camera)
        return self

    def addFiltering(self, filtering) -> typing.Self:
        self.videoController.setFiltering(filtering)
        return self

    def addSerialization(self, serialization: SerializerInterface) -> typing.Self:
        self.videoController.setSerialization(serialization)
        return self

    def addCompression(self, compression: CompressorInterface) -> typing.Self:
        self.videoController.setCompression(compression)
        return self

    def addTransmission(self, transmission: VideoTransmitterInterface) -> typing.Self:
        self.videoController.setTransmission(transmission)
        return self

    def build(self) -> VideoController:
        return self.videoController
