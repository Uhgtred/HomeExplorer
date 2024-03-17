#!/usr/bin/env python3
# @author: Markus Kösters
import os.path
import unittest
from pathlib import Path

from Video.VideoTransmitter import VideoTransmitterFactory


class test_VideoTransmitter(unittest.TestCase):
    transmitter = VideoTransmitterFactory.produceVideoTransmitterStub(port=2002)

    def test_transmit(self):
        path = str(Path(__file__).parent) + '/testImage'
        with open(path, 'rb') as image_file:
            image_data = image_file.read()
        self.transmitter.transmit(path)
        transmitterBuffer = self.transmitter._VideoTransmitter__bus.bus.sock.recvfrom(4096)
        print(transmitterBuffer)
        print(image_data)
        self.assertEqual(image_data, transmitterBuffer)  # add assertion here


if __name__ == '__main__':
    unittest.main()
