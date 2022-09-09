#!/usr/bin/env python3
# @author   Markus Kösters

import threading
import time
import os

from Arduino.Arduino import Arduino
from Network.SocketServer import Server
from Configurations.ConfigReader import ConfigReader
#from Camera.Camera import Camera

os.chdir(os.path.dirname(os.getcwd()))


class Main:

    def __init__(self):
        """Starting the Robot-Program and configuring everything"""
        self.socketReceivedMessage = '00000000000000000000'
        self.__conf = ConfigReader()
        self.__delay = float(self.__conf.readConfigParameter('DelayMain'))
        self.__socketDelay = float(self.__conf.readConfigParameter('SocketDelay'))
        self.Arduino = Arduino()
        self.__serial = self.Arduino.initArduino()
        #self.__camera = Camera()
        self.__socket = Server()
        self.conn = self.__socket.start()
        self.__threads()

        try:
            while True:
                time.sleep(1)  # sleep is for reducing CPU-load
        except KeyboardInterrupt:
            print('Program exit, resetting GPIO-Pins...')
        finally:
            self.__exit_handler()

    def __serialCommunication(self):
        while True:
            self.Arduino.sendMessage(self.socketReceivedMessage, self.__serial)
            receivedMessage = self.Arduino.readMessage(self.__serial)
            time.sleep(self.__delay)  # sleep is for reducing CPU-load
    
    def __socketRead(self):
        while True:
            self.socketReceivedMessage = self.__socket.rcvMessage()
#             if not self.socketReceivedMessage:
#                 self.socketReceivedMessage = '00000000000000000000'
            time.sleep(self.__socketDelay)
            
    def __socketWrite(self):
        while True:
            self.__socket.sendMessage(self.socketSendMessage)
            time.sleep(self.__socketDelay)

    def __socketCommunication(self):
        """This method is handling the communication between Robot and Remote"""
        while True:
            try:
                self.__serialDataLine = self.socketReceivedMessage
                #vid = self.__camera.readCamera()
                #self.__socket.sendMessage(vid)
                time.sleep(self.__socketDelay)  # sleep is for reducing CPU-load
            except Exception as e:
                self.__serialDataLine = '00000000000000000000'  # in case of error in communication to remote puts zeroes to stop the motors
                print('Error occurred during communication to external device!', e)

    def __threads(self):
        """Any Thread that has to run goes in here!"""
        __socketReadThread = threading.Thread(target=self.__socketRead, name='SocketReadThread')
        __socketReadThread.daemon = True
        __socketReadThread.start()

#         __socketWriteThread = threading.Thread(target=self.__socketWrite, name='SocketWriteThread')
#         __socketWriteThread.daemon = True
#         __socketWriteThread.start()

        #__cameraStreamThread = threading.Thread(target=self.__camera.readCamera(), name='CameraStreamThread')
        #__cameraStreamThread.daemon = True
        #__cameraStreamThread.start()

#         __socketCommunicationThread = threading.Thread(target=self.__socketCommunication, name='SocketCommunicationThread')
#         __socketCommunicationThread.daemon = True
#         __socketCommunicationThread.start()

        __serialCommunicationThread = threading.Thread(target=self.__serialCommunication, name='SerialCommunicationThread')
        __serialCommunicationThread.daemon = True
        __serialCommunicationThread.start()

    def __exit_handler(self):
        self.Arduino.close(self.__serial)


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
