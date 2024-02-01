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
        self.__resolution = config.Resolution
        # Todo: Not sure if this is a good way to do this here. But don't want an extra class for one line of code.
        self.__setupCamera()

    def __setupCamera(self) -> None:
        """
        Method for setting up the camera.
        """
        if not self.__cam:
            # Creating an instance of a camera-object.
            self.__cam = cv2.VideoCapture(self.__videoPort)
        self.__setResolution()

    @property
    def resolution(self) -> list:
        """
        Getter-Method for getting the current resolution of the camera.
        :return: List containing the X and the Y-Value of the current resolution [x, y].
        """
        return self.__resolution

    @resolution.setter
    def resolution(self, resolution: list[int, int]) -> None:
        """
        Setter-Method for the camera-resolution.
        :param resolution: Resolution that will be set [X, Y]
        """
        self.__resolution = [0, 0]  # make sure that the list exists with 2 values
        self.__resolution[0] = max(resolution)
        self.__resolution[1] = min(resolution)
        # Setting resolution on camera-instance when setting the values of the variables
        self.__setResolution()

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
        __startTime = time.time()
        while self.__cam is not None and self.__cam.isOpened():
            # state returns false if the frame could not be read, else returns true.
            state, frame = self.__cam.read()
            if not state:
                # Todo: make a log-entry when a frame could not be read correctly.
                #       maybe a warning would also be a good idea, depending on the frequency of this happening
                pass
            # executing any 1s/fps so for 1s/30fps it will execute any 0.0333seconds
            # sleeping the program is no option because the buffer of the camera will then cause lag
            if time.time() - __startTime == self.__videoFPS:
                # calling the defined callback-method and passing it the frame recorded.
                callbackMethod(frame)

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

    def __setResolution(self):
        """
        Method for setting the resolution of the camera.
        """
        self.__cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.__resolution[0])
        self.__cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.__resolution[1])