#!/usr/bin/env python3
# @author      Markus Kösters

import cv2
import pickle
import struct


class Camera:

    def __init__(self):
        pass

    def readCamera(self):
        camStream = cv2.VideoCapture(0)
        msg = ''
        while camStream.isOpened():
            img, frame = camStream.read()
            temp = pickle.dumps(frame)
            msg = struct.pack('Q', len(temp)) + temp
        return msg
