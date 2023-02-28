#!/usr/bin/env python3
# @author      Markus Kösters


import time
import cv2
import pickle

import imutils
from Configurations.ConfigReader import ConfigReader
from Network.SocketController import SocketController


class Camera:

    def __init__(self):
        self.__conf = ConfigReader()
        self.videoFPS = float(1 / float(self.__conf.readConfigParameter('VideoFPS')))
        self.resolution = self.__conf.readConfigParameter('CameraResolution')
        self.videoPort = int(self.__conf.readConfigParameter('Video_Port'))
        self.socketController = SocketController()

    def readCamera(self):
        vid = cv2.VideoCapture(0)
        # __socket = Server()
        self.socketController.startServer('video')
        while vid.isOpened():
            img, frame = vid.read()
            frame = imutils.resize(frame, width=640, height=480)
            self.socketController.sendMessage(pickle.dumps(frame), 'video')
            time.sleep(self.videoFPS)


if __name__ == '__main__':
    obj = Camera()
    obj.readCamera()
