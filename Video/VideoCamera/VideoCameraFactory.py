#!/usr/bin/env python3
# @author: Markus Kösters

from .VideoCamera import VideoCamera
from .VideoCameraConfig import VideoCameraConfig
from .test_UnitTests.VideoCameraStub import VideoCameraStub


class VideoCameraFactory:

    @staticmethod
    def produceDefaultCameraInstance():
        """
        Method that produces a VideoCamera-instance with a default configuration.
        """
        camConfig = VideoCameraConfig(30, 0, (800, 480))  # standard resolution of a raspberry-pi display
        return VideoCamera(camConfig)

    @staticmethod
    def produceStubCameraInstance():
        camConfig = VideoCameraConfig(30, 0, (800, 480), VideoCameraStub)
        return VideoCamera(camConfig)

