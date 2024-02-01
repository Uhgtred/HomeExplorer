#!/usr/bin/env python3
# @author: Markus Kösters
from .Camera import Camera
from .CameraConfig import CameraConfig


class CameraFactory:

    @staticmethod
    def produceDefaultCameraInstance():
        """
        Method that produces a Camera-instance with a default configuration.
        """
        camConfig = CameraConfig(30, 0, [800, 480])  # standard resolution of a raspberry-pi display
        return Camera(camConfig)
