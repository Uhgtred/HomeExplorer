#!/usr/bin/env python3
# @author: Markus Kösters

import unittest

from Video.VideoCamera import VideoCameraFactory, VideoCamera


class CameraFactoryTest(unittest.TestCase):

    def test_produceDefaultCameraInstance(self):
        myCamera = VideoCameraFactory.produceDefaultCameraInstance()
        self.assertTrue(isinstance(myCamera, VideoCamera))
        myCamera.stopCamera()


if __name__ == '__main__':
    unittest.main()
