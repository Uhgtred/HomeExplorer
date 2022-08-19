#!/usr/bin/env python3
# @author   Markus Kösters

import threading
import time

from Controller.Controller import Controller
from Network.SocketClient import SocketClient
from Configuration.ConfigReader import ConfigReader


class Main:
    
    def __init__(self):
        self.__conf = ConfigReader()
        self.__cont = Controller()
        self.__socketClient = SocketClient()
        self.connectToServer()
        self.__delay = float(self.__conf.readConfigParameter('DelayMain'))

        __controller = self.__cont.initController()
        self.__controllerValues = ''

        __controllerThread = threading.Thread(target=lambda: self.__cont.readController(__controller), name='ControllerThread')  # has to be lambda-function! arguments won't work because of obj-like parameter
        __controllerThread.daemon = True
        __controllerThread.start()

        __socketThread = threading.Thread(target=self.__socketCommunication, name='ControllerValueThread')
        __socketThread.daemon = True
        __socketThread.start()

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
        retryCounter = 1
        while not __connected:
            print(f'Trying to connect to server! (Try: {retryCounter})')
            __connected = self.__socketClient.connect()
            retryCounter += 1
            time.sleep(1)
        print(f'Connection to Server established:\t{__connected}')

    def __socketCommunication(self):
        while True:
            self.__controllerValues = self.__cont.getControllerValues()
            self.__socketClient.sendMessage(self.__controllerValues)
            self.__socketClient.rcvVideo()
            time.sleep(self.__delay)

    def exit_handler(self):
        self.__socketClient.disconnect()
    
    def __del__(self):
        self.exit_handler()


main = Main()
