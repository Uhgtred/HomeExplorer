#!/usr/bin/env python3
# @author      Markus Kösters

import cv2
import pickle
import struct
import imutils


class Camera:

    def __init__(self):
        pass

    def readCamera(self, display=False):
        camStream = cv2.VideoCapture(0)
        msg = ''
        if camStream.isOpened():
            img, frame = camStream.read()
            if display:
                cv2.imshow('RobotStream', frame)
                key = cv2.waitKey(1)
            frame = imutils.resize(frame, width=320)
            temp = pickle.dumps(frame)
            msg = struct.pack('Q', len(temp)) + temp
        return msg

if __name__ == '__main__':
    obj = Camera()
    __answer = obj.readCamera(display=True)