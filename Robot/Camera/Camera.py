#!/usr/bin/env python3
# @author      Markus Kösters


import time
import cv2
import pickle
import struct
import imutils

from Configurations.ConfigReader import ConfigReader


class Camera:

    def __init__(self):
        self.__conf = ConfigReader()
        self.videoFPS = float(1 / self.__conf.readConfigParameter('VideoFPS)'))
        self.message = ''

    def readCamera(self, display=False):
        while True:
            vid = cv2.VideoCapture(0)
            while vid.isOpened():
                img, frame = vid.read()
                frame = imutils.resize(frame, width=320)
                a = pickle.dumps(frame)
                self.message = struct.pack("Q", len(a)) + a
                time.sleep(self.videoFPS)



if __name__ == '__main__':
    obj = Camera()
    __answer = obj.readCamera(display=True)
