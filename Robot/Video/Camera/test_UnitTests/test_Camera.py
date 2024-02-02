#!/usr/bin/env python3
# @author: Markus Kösters
import time
import unittest
import numpy

from Robot.Video.Camera import Camera, CameraFactory


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
        self.camera = CameraFactory.produceDefaultCameraInstance()
        self.camera.readCameraInLoop(self.helper)
        time.sleep(runTime)
        self.assertIs(type(self.frame), numpy.ndarray)
        print(self.frameCounter)
        self.camera.stopCamera()
        self.frameCounter = 0

    def test_cameraSingleFrame(self):
        camera = CameraFactory.produceDefaultCameraInstance()
        frame = camera.readSingleFrame()
        self.assertIs(type(frame), numpy.ndarray)
        camera.stopCamera()

    def test_stopCamera(self):
        camera = CameraFactory.produceDefaultCameraInstance()
        camera.stopCamera()
        self.assertIs(camera._Camera__cam, None)

if __name__ == '__main__':
    unittest.main()
