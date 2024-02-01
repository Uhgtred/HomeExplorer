#!/usr/bin/env python3
# @author: Markus Kösters

import unittest

from Robot.Video.Camera import CameraFactory, Camera


class CameraFactoryTest(unittest.TestCase):

    def test_produceDefaultCameraInstance(self):
        myCamera = CameraFactory.produceDefaultCameraInstance()
        self.assertTrue(isinstance(myCamera, Camera))
        myCamera.stopCamera()


if __name__ == '__main__':
    unittest.main()
