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
        self.Arduino = Arduino()
        self.__serial = self.Arduino.initArduino()
        self.__conf = ConfigReader()
        self.__delay = float(self.__conf.readConfigParameter('DelayMain'))

        #self.__camera = Camera()
        
        self.__socket = Server()
        self.conn = self.__socket.start()        
        __socketCommunicationThread = threading.Thread(target=self.__socketCommunication, name='SocketCommunicationThread')
        __socketCommunicationThread.daemon = True
        __socketCommunicationThread.start()

        try:
            while True:
                time.sleep(1)  # sleep is for reducing CPU-load
        except KeyboardInterrupt:
            print('Program exit, resetting GPIO-Pins...')
        finally:
            self.__exit_handler()

    def __socketCommunication(self):
        while True:
            try:
                dataLine = self.__socket.getData()
                #vid = self.__camera.readCamera()
                #self.__socket.sendData(vid)
                if dataLine:
                    self.Arduino.sendMessage(dataLine, self.__serial)
                time.sleep(self.__delay)
            except Exception as e:
                print('Error occurred during communication to external device!', e)

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
