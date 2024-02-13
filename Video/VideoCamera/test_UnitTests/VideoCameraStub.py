#!/usr/bin/env python3
# @author: Markus Kösters

import numpy as np


class VideoCameraStub:
    # Typical shape for a 480p video frame
    height = 480
    width = 640

    # OpenCV uses BGR color space by default
    channels = 3

    isOpen: bool = False

    def __init__(self, source):
        self.args = None
        self.source = source
        self.isOpen: bool = True

    def isOpened(self):
        return self.isOpen
    
    def set(self, *args):
        self.args = args

    def read(self):
        """
        Stub method for cv2.VideoCapture.read().
        :return: numpy array with random data and shape of (height, width, channels).
        """
        frame = np.random.randint(0, 255, (self.height, self.width, self.channels), dtype=np.uint8)
        return frame

    def release(self):
        self.isOpen = False
