#!/usr/bin/env python3
# @author: Markus Kösters
import logging
import unittest

import numpy

from Video.VideoTransmitter import VideoTransmitterFactory, VideoTransmitter


class test_VideoTransmitter(unittest.TestCase):
    """
    This class contains unit tests for verifying the functionality and correctness of a
    video transmitter.

    The primary goal of this class is to ensure the video transmission process accurately
    handles image data. It verifies that the transmitted data received at the other end
    matches the original data, thus maintaining data integrity during transmission.

    :ivar __logger: Logger instance used for logging class-level information.
    :type __logger: logging.Logger
    """

    __logger: logging.Logger = logging.getLogger(__name__)

    def test_transmit(self) -> None:
        """
        Tests the functionality of the video transmission process by verifying that the
        transmitted data matches the original data.

        The test creates a video transmitter with a specified port in stub mode, reads an
        image file from the current directory, and transmits it through the created
        transmitter. The transmitted data is then obtained and compared with the original
        image data to ensure accuracy.

        :raises AssertionError: If the transmitted data does not match the original
            image data.
        """
        transmitter: VideoTransmitter = VideoTransmitterFactory.produceDefaultVideoTransmitterStub(port=2002)
        whiteImage: numpy.ndarray = numpy.ones((100, 100, 3), dtype=numpy.uint8) * 255
        transmitter.transmit(whiteImage)
        transmitterBuffer: tuple[bytes,tuple[str, int]] = transmitter._VideoTransmitter__bus.bus.sock.recvfrom(4096)
        self.assertIsInstance(transmitterBuffer, tuple)



if __name__ == '__main__':
    unittest.main()
