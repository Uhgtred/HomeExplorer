#!/usr/bin/env python3
# @author: Markus Kösters

import unittest

from Video.VideoTransmitter import VideoTransmitterFactory


class test_VideoTransmitter(unittest.TestCase):

    transmitter = VideoTransmitterFactory.produceVideoTransmitterStub(port=2002)

    def test_transmit(self):
        with open('testImage', 'rb') as image_file:
            image_data = image_file.read()
        self.transmitter.transmit('testImage')
        transmitterBuffer = self.transmitter._VideoTransmitter__bus.bus.sock.recvfrom(4096)[-len(image_data):]
        self.assertEqual(image_data, transmitterBuffer)  # add assertion here


if __name__ == '__main__':
    unittest.main()
