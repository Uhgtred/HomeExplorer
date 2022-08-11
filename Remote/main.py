#!/usr/bin/env python3
# @author   Markus Kösters

import threading
import time
from Controller.Controller import Controller
from Network.SocketClient import SocketClient
from Camera.IPCamera import IPCamera
from Remote.Configuration.ConfigReader import ConfigReader


class Main:
    
    def __init__(self):
        self.__conf = ConfigReader()
        self.__cont = Controller()
        self.__socketClient = SocketClient()
        self.connectToServer()
        self.__delay = float(self.__conf.readConfigParameter('DelayMain'))
        self.__cameraDelay = float(self.__conf.readConfigParameter('CameraDelay'))

        __controller = self.__cont.initController()
        print(__controller)
        self.__controllerValues = ''
        
        __controllerThread = threading.Thread(target=lambda: self.__cont.readController(__controller), name='ControllerThread')  # has to be lambda-function! arguments won't work because of obj-like parameter
        __controllerThread.daemon = True
        __controllerThread.start()
        
        __cameraThread = threading.Thread(target=self.__camReadContinuously, name='CameraThread')
        __cameraThread.daemon = True
        __cameraThread.start()

        __trackThread = threading.Thread(target=self.__sendControllerData, name='ControllerValueThread')
        __trackThread.daemon = True
        __trackThread.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print('Program exit...')
            self.exit_handler()
        finally:
            self.exit_handler()
            
    def connectToServer(self):
        __connected = False
        while not __connected:
            print('trying to connect')
            __connected = self.__socketClient.connect()
            time.sleep(1)
        print(f'Connection to Server:\t{__connected}')
    
    def __camReadContinuously(self):
        self.__socketClient.rcvVideo()
        # self.__camera = IPCamera()
        # while True:
        #     try:
        #         #self.__camera = IPCamera() # better performance if out of the loop?
        #         self.__camera.readCamera()
        #     except:
        #         pass

    def __sendControllerData(self):
        while True:
            self.__controllerValues = self.__cont.getControllerValues()
            self.__socketClient.sendMessage(self.__controllerValues)
            time.sleep(self.__delay)

    def exit_handler(self):
        self.__camera.cleanCamera()
        self.__socketClient.disconnect()
    
    def __del__(self):
        self.exit_handler()


main = Main()
