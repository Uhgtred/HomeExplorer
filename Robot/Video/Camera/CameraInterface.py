#!/usr/bin/env python3
# @author: Markus Kösters

from abc import ABC, abstractmethod


class CameraInterface(ABC):

    @abstractmethod
    @property
    def FPS(self) -> float:
        """
        Getter-Method for getting the current camera FPS.
        :return: Float representing the camera-FPS.
        """
        pass

    @abstractmethod
    @FPS.setter
    def FPS(self, fps: int) -> None:
        """
        Setter-Method for setting the camera-FPS.
        :param fps: Integer representing the camera-FPS.
        """
        pass

    @abstractmethod
    def readCameraInLoop(self, callbackMethod: any) -> None:
        """
        Method for reading the camera.
        :param callbackMethod: Method that the output-image shall be passed to for further processing.
        """
        pass

    @abstractmethod
    def readSingleFrame(self) -> object:
        """
        Method for reading a single frame from the camera.
        :return:
        """
        pass

    @abstractmethod
    def stopCamera(self) -> None:
        """
        Method for closing the camera.
        """

