#!/usr/bin/env python3
# @author: Markus Kösters
import time
import unittest
from pathlib import Path

from Video.VideoTransmitter import VideoTransmitterFactory


class test_VideoTransmitter(unittest.TestCase):
    transmitter = VideoTransmitterFactory.produceDefaultVideoTransmitter(port=2002, stub=True)

    def test_transmit(self):
        path = str(Path(__file__).parent) + '/testImage'
        with open(path, 'rb') as image_file:
            image_data = image_file.read()
        self.transmitter.transmit(path)
        time.sleep(0.01)
        transmitterBuffer = self.transmitter._VideoTransmitter__bus.bus.sock.recvfrom(4096)
        self.assertIn(image_data, transmitterBuffer)  # add assertion here


if __name__ == '__main__':
    unittest.main()
