#!/usr/bin/env python3
# @author   Markus Kösters

import threading
import time
import os

from Arduino.Arduino import Arduino
from Network.SocketServer import Server
from Configurations.ConfigReader import ConfigReader
from Camera.Camera import Camera

os.chdir(os.path.dirname(os.getcwd()))


class Main:

    def __init__(self):
        """Starting the Robot-Program and configuring everything"""
        self.Arduino = Arduino()
        self.__serial = self.Arduino.initArduino()
        self.__conf = ConfigReader()
        self.__delay = float(self.__conf.readConfigParameter('DelayMain'))
        self.__socketDelay = float(self.__conf.readConfigParameter('SocketDelay'))

        self.__camera = Camera()
        
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
        if self.__serialDataLine:
            self.Arduino.sendMessage(self.__serialDataLine, self.__serial)
            time.sleep(self.__delay)  # sleep is for reducing CPU-load

    def __socketCommunication(self):
        """This method is handling the communication between Robot and Remote"""
        while True:
            try:
                self.__serialDataLine = self.__socket.getData()
                vid = self.__camera.readCamera()
                self.__socket.sendData(vid)
                time.sleep(self.__socketDelay)  # sleep is for reducing CPU-load
            except Exception as e:
                self.__serialDataLine = '00000000000000000000'  # in case of error in communication to remote puts zeroes to stop the motors
                print('Error occurred during communication to external device!', e)

    def __threads(self):
        """Any Thread that has to run goes in here!"""
        __socketReadThread = threading.Thread(target=self.__socket.rcvMessage, name='SocketReadThread')
        __socketReadThread.daemon = True
        __socketReadThread.start()

        __socketWriteThread = threading.Thread(target=self.__socket.sendMessage, name='SocketWriteThread')
        __socketWriteThread.daemon = True
        __socketWriteThread.start()

        __socketCommunicationThread = threading.Thread(target=self.__socketCommunication,
                                                       name='SocketCommunicationThread')
        __socketCommunicationThread.daemon = True
        __socketCommunicationThread.start()

        __serialCommunicationThread = threading.Thread(target=self.__serialCommunication,
                                                       name='SerialCommunicationThread')
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
