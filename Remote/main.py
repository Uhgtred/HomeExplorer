#!/usr/bin/env python3
# @author   Markus Kösters

import threading
import time
import cv2

from Controller.Controller import Controller
from Network.SocketClient import SocketClient
from Configuration.ConfigReader import ConfigReader


class Main:

    def __init__(self):
        """Starting the Remote-Program and configuring everything"""
        self.__conf = ConfigReader()
        self.__delay = float(self.__conf.readConfigParameter('DelayMain'))
        self.__socketDelay = float(self.__conf.readConfigParameter('SocketDelay'))
        print(self.__socketDelay)
        self.videoFPS = float(1 / float(self.__conf.readConfigParameter('VideoFPS')))
        self.__controllerValues = '00000000000000000000'
        #self.videoController = cv2
        self.__cont = Controller()
        self.__controller = self.__cont.initController()
        self.__socketClient = SocketClient()
        self.__connectToServer()
        self.__threads()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print('Program exit...')
            self.exit_handler()
        finally:
            self.exit_handler()

    def __connectToServer(self):
        """Connects Remote (client) to Robot (server)"""
        __connected = False
        retryCounter = 1
        while not __connected:
            print(f'Trying to connect to server! (Try: {retryCounter})')
            __connected = self.__socketClient.connect()
            retryCounter += 1
            time.sleep(1)
        print(f'Connection to Server established:\t{__connected}')

    def __readController(self):
        while True:
            try:
                self.__controllerValues = self.__cont.getControllerValues()
            except Exception as e:
                self.__controllerValues = '00000000000000000000'  # in case of error in communication to controller puts zeroes to stop the motors
                print(f'Error while reading controller: {e}')
            time.sleep(self.__delay)

    def __cameraStream(self):
        while True:
            vidFrame = self.__socketClient.rcvVideo()
            self.videoController.imshow('Robot Vision') # needs to go on a real GUI!!!
            time.sleep(self.videoFPS)
            
    def __socketRead(self):
        while True:
            self.socketReceivedMessage = self.__socketClient.rcvMessage()
            time.sleep(self.__socketDelay)
            
    def __socketWrite(self):
        while True:
            self.__socketClient.sendMessage(self.__controllerValues)
            time.sleep(self.__socketDelay)

    def __socketCommunication(self):
        while True:
            self.__socketClient.sendMessage(self.__controllerValues)
            time.sleep(self.__socketDelay)

    def __threads(self):
        """Any Thread that has to run goes in here!"""
        __controllerThread = threading.Thread(target=self.__readController, name='ControllerThread')
        __controllerThread.daemon = True
        __controllerThread.start()
        
        __controllerReadThread = threading.Thread(target=lambda : self.__cont.readController(self.__controller) , name='ControllerReadThread')
        __controllerReadThread.daemon = True
        __controllerReadThread.start()
#         __socketReadThread = threading.Thread(target=self.__socketRead, name='SocketReadThread')
#         __socketReadThread.daemon = True
#         __socketReadThread.start()

        __socketWriteThread = threading.Thread(target=self.__socketWrite, name='SocketWriteThread')
        __socketWriteThread.daemon = True
        __socketWriteThread.start()

#         __socketCommunicationThread = threading.Thread(target=self.__socketCommunication, name='SocketCommunicationThread')
#         __socketCommunicationThread.daemon = True
#         __socketCommunicationThread.start()

        #__cameraStreamThread = threading.Thread(target=self.__cameraStream, name='CameraStreamThread')
        #__cameraStreamThread.daemon = True
        #__cameraStreamThread.start()

        __cameraStreamThread = threading.Thread(target=self.__cameraStream, name='CameraStreamThread')
        __cameraStreamThread.daemon = True
        __cameraStreamThread.start()

    def exit_handler(self):
        """Put things that need to b done before program-exit"""
        pass


main = Main()
