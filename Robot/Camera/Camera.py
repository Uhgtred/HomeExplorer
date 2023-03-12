#!/usr/bin/env python3
# @author      Markus Kösters


import cv2
import pickle
import imutils

from Configurations import ConfigReader
from Network import SocketController


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
            frame = imutils.resize(frame, width=120, height=80)
            self.socketController.sendMessage(pickle.dumps(frame), 'video')
            # time.sleep(self.videoFPS)


if __name__ == '__main__':
    obj = Camera()
    obj.readCamera()
