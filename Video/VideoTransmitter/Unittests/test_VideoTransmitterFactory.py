#!/usr/bin/env python3
# @author: Markus Kösters

import unittest

from Video.VideoTransmitter import VideoTransmitterFactory, VideoTransmitter


class test_VideoTransmitterFactory(unittest.TestCase):
    def test_produceDefaultVideoTransmitter(self):
        videoTransmitter = VideoTransmitterFactory.produceDefaultVideoTransmitter(2002)
        self.assertIsInstance(videoTransmitter, VideoTransmitter)

if __name__ == '__main__':
    unittest.main()
