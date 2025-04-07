#!/usr/bin/env python3
# @author: Markus Kösters

import unittest

from Video.VideoCamera import VideoCameraConfig


class CameraConfigTest(unittest.TestCase):
    def test_CameraConfigPositive(self):
        fps = 30
        port = 0
        resolution = (640, 480)
        config = VideoCameraConfig(fps, port, resolution)
        self.assertEqual(config.Port, port)
        self.assertEqual(config.FPS, fps)
        self.assertEqual(config.Resolution, resolution)

    # Todo: implement negative testcase!

if __name__ == '__main__':
    unittest.main()
