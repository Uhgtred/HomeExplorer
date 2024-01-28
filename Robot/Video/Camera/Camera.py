#!/usr/bin/env python3
# @author      Markus Kösters

import time
import cv2

from .CameraConfig import CameraConfig
from .CameraInterface import CameraInterface


class Camera(CameraInterface):

    __cam = None

    def __init__(self, config: CameraConfig):
        self.__videoFPS = float(1 / config.FPS)
        self.__videoPort = config.Port
        # Todo: Not sure if this is a good way to do this here. But don't want an extra class for one line of code.
        self.__setupCamera()

    def __setupCamera(self) -> None:
        """
        Method for setting up the camera.
        """
        if not self.__cam:
            self.__cam = cv2.VideoCapture(self.__videoPort)

    @property
    def FPS(self) -> float:
        """
        Getter-Method for getting the current camera FPS.
        :return: Float representing the camera-FPS.
        """
        return self.__videoFPS

    @FPS.setter
    def FPS(self, fps: int) -> None:
        """
        Setter-Method for setting the camera-FPS.
        :param fps: Integer representing the camera-FPS.
        """
        self.__videoFPS = float(1 / fps)

    def readCameraInLoop(self, callbackMethod: any) -> None:
        """
        Method for reading the camera.
        :param callbackMethod: Method that the output-image shall be passed to for further processing.
        """
        while self.__cam.isOpened():
            # state returns false if the frame could not be read, else returns true.
            state, frame = self.__cam.read()
            if not state:
                # Todo: make a log-entry when a frame could not be read correctly.
                #       maybe a warning would also be a good idea, depending on the frequency of this happening
                pass
            callbackMethod(frame)
            time.sleep(self.__videoFPS)

    def stopCamera(self) -> None:
        """
        Method for releasing the camera.
        """
        self.__cam.release()
        self.__cam = None

    def readSingleFrame(self) -> object:
        """
        Read single frame from the camera if camera is open and no error occurs while reading.
        :return: Frame read from the camera. Or None if the camera is not open or an error occurs.
        """
        if self.__cam.isOpened():
            state, frame = self.__cam.read()
            if state:
                return frame
        return None
