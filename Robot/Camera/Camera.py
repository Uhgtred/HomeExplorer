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
        self.videoFPS = float(1 / float(self.__conf.readConfigParameter('VideoFPS')))  # waiting time is the reciprocal of frames per second
        self.resolution = self.__conf.readConfigParameter('CameraResolution')
        self.videoPort = int(self.__conf.readConfigParameter('Video_Port'))
        self.socketController = SocketController()

    def readCamera(self):
        """Reading a frame from the default-camera and senfing it via socket"""
        vid = cv2.VideoCapture(0)  # starting video-recording
        self.socketController.startServer('video')  # starting the socket-server
        while vid.isOpened():
            img, frame = vid.read()
            frame = imutils.resize(frame, width=120, height=80)  # resizing image for optimizing the transfer-rate
            self.socketController.sendMessage(pickle.dumps(frame), 'video')  # Sending the frame to the socket-client


if __name__ == '__main__':
    obj = Camera()
    obj.readCamera()
