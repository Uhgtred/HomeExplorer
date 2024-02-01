#!/usr/bin/env python3
# @author: Markus Kösters

import unittest

from Robot.Video.Camera import CameraConfig


class CameraConfigTest(unittest.TestCase):
    def test_CameraConfigPositive(self):
        fps = 30
        port = 0
        resolution = (640, 480)
        config = CameraConfig(fps, port, resolution)
        self.assertEqual(config.Port, port)
        self.assertEqual(config.FPS, fps)
        self.assertEqual(config.Resolution, resolution)

    def test_CameraConfigNegative(self):
        port = 'hans'
        resolution = '300x200'
        fps = -1
        config = CameraConfig(fps, port, resolution)
        print(config)


if __name__ == '__main__':
    unittest.main()
