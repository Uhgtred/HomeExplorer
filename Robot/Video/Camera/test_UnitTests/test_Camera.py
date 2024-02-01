#!/usr/bin/env python3
# @author: Markus Kösters

import unittest
import numpy

from Robot.Video.Camera import Camera, CameraFactory


class CameraTest(unittest.TestCase):

    frame = None
    camera = None

    def helper(self, frame):
        self.frame = frame
        self.camera.stopCamera()

    def test_cameraTest(self):
        self.camera = CameraFactory.produceDefaultCameraInstance()
        self.camera.readCameraInLoop(self.helper)
        self.assertIs(type(self.frame), numpy.ndarray)

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
