#!/usr/bin/env python3
# @author: Markus Kösters

import time
import unittest

import cv2
import numpy

from Video.VideoCamera import VideoCameraFactory


class CameraTest(unittest.TestCase):

    frame = None
    camera = None
    frameCounter = 0

    def helper(self, frame):
        self.frame = frame
        if frame is not None:
            self.frameCounter += 1
        # print(f'Frame read:\n{frame}')

    def test_cameraTest(self):
        runTime = 3
        self.camera = VideoCameraFactory.produceDefaultCameraInstance()
        self.camera.readCameraInLoop(self.helper)
        # waiting the defined amount of time until closing the camera.
        time.sleep(runTime)
        self.assertIs(type(self.frame), numpy.ndarray)
        self.camera.stopCamera()
        print(f'[UnitTest][Video]: {self.frameCounter} frames recorded in {runTime} seconds!')
        self.frameCounter = 0

    def test_cameraSingleFrame(self):
        camera = VideoCameraFactory.produceStubCameraInstance()
        frame = camera.readSingleFrame()
        self.assertIs(type(frame), type(numpy.ndarray([])))
        camera.stopCamera()

    def test_stopCamera(self):
        camera = VideoCameraFactory.produceStubCameraInstance()
        camera.stopCamera()
        self.assertFalse(camera._VideoCamera__cam.isOpened())

if __name__ == '__main__':
    unittest.main()
