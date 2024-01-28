#!/usr/bin/env python3
# @author: Markus Kösters
from .Camera import Camera
from .CameraConfig import CameraConfig


class CameraFactory:

    @staticmethod
    def produceCameraInstance():
        """
        Method that produces a Camera-instance with a default configuration.
        """
        camConfig = CameraConfig(30, 0)
        return Camera(camConfig)
