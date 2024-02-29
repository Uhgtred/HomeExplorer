#!/usr/bin/env python3
# @author      Markus Kösters

import time
import cv2

import Runners.threadRunner
from .VideoCameraConfig import VideoCameraConfig
from .VideoCameraInterface import VideoCameraInterface


class VideoCamera(VideoCameraInterface):

    def __init__(self, config: VideoCameraConfig):
        self.__cam: callable = config.camera
        self.__isRunning: bool = False
        self.__videoFPS: float = float(1 / config.FPS)
        self.__videoPort: int = config.Port
        self.__resolution: tuple[int, int] = config.Resolution
        self.__runner = Runners.threadRunner.ThreadRunner()
        # Todo: Not sure if this is a good way to do this here. But don't want an extra class for one line of code.
        self.__setupCamera()

    def __setupCamera(self) -> None:
        """
        Method for setting up the camera.
        """
        # opening camera if the object is callable (not instanced yet).
        if callable(self.__cam):
            self.__cam = self.__cam(self.__videoPort)
        self.__setResolution()

    @property
    def resolution(self) -> tuple[int, int]:
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
    def FPS(self) -> int:
        """
        Getter-Method for getting the current camera FPS.
        :return: Float representing the camera-FPS.
        """
        return int(1/self.__videoFPS)

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
        # Todo: check if this could be a process instead of a thread (pipes would be needed in that case)!
        #       Or check if Python 3.13 would give this a performance-boost by deactivating GIL.
        self.__runner.addTask(self.__readCameraInLoopThread, (callbackMethod,))
        self.__runner.runTasks()

    def __readCameraInLoopThread(self, *args) -> None:
        """
        Method for reading the camera in loop and new thread.
        :param callbackMethod: Method that the output-image shall be passed to for further processing.
        """
        callbackMethod = args[0]
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
            if time.time() - __startTime >= self.__videoFPS:
                # calling the defined callback-method and passing it the frame recorded.
                callbackMethod(frame)
                __startTime = time.time()

    def stopCamera(self) -> None:
        """
        Method for releasing the camera.
        """
        self.__cam.release()

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

    def __setResolution(self) -> None:
        """
        Method for setting the resolution of the camera.
        """
        self.__cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.__resolution[0])
        self.__cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.__resolution[1])
