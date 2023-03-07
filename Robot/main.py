#!/usr/bin/env python3
# @author   Markus Kösters

import threading
import time
import os

from Arduino.Arduino import Arduino
from Camera.Camera import Camera
from Configurations.ConfigReader import ConfigReader
from Network.SocketController import SocketController

os.chdir(os.path.dirname(os.getcwd()))


class Main:

    def __init__(self):
        """Starting the Robot-Program and configuring everything"""
        self.__conf = ConfigReader()
        self.__delay = float(self.__conf.readConfigParameter('DelayMain'))
        self.socketController = SocketController()
        # self.socketController.startServer('controller')
        self.Arduino = Arduino()
        self.Arduino.initArduino()
        self.__camera = Camera()
        self.__threads()

    def __serialCommunication(self):
        while True:
            message = self.socketController.receiveMessage('controller')
            self.Arduino.sendMessage(message)
            time.sleep(self.__delay)  # sleep is for reducing CPU-load

    def __threads(self):
        """Any Thread that has to run goes in here!"""
        __cameraStreamThread = threading.Thread(target=self.__camera.readCamera, name='CameraReadThread', daemon=True)
        __cameraStreamThread.start()

        # __serialCommunicationThread = threading.Thread(target=self.__serialCommunication, name='SerialCommunicationThread', daemon=True)
        # __serialCommunicationThread.start()

        __cameraStreamThread.join()
        # __serialCommunicationThread.join()

    # def __exit_handler(self):
    #     self.Arduino.close(self.__serial)

if __name__ == '__main__':
    main = Main()
    # ((0-255),(0/1),(0-255),(0/1),(-32768-32767),y)
#     import serial
#     device = serial.Serial()
#     device.baud = 9600
#     device.port = '/dev/ttyACM0'
#     device.timeout = 0.05
#     device.open()
#     
#     answer = ''
#     while True:
#         device.write('bla'.encode())
#         time.sleep(0.05)
#         answer = device.readline().decode()
#         print(answer.rstrip())
#     try:
#         answer = answer.decode('utf-8')
#     except:
#         pass
#     print(answer)
#     device.close()
