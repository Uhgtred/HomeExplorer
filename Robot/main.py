#!/usr/bin/env python3
# @author   Markus Kösters

import threading
import time
import os

from Arduino.Arduino import Arduino
# from Controller.Controller import Controller
from Network.SocketServer import Server
from HardwareConfiguration.ConfigReader import ConfigReader

os.chdir(os.path.dirname(os.getcwd()))


class Main:

    def __init__(self):
        self.Arduino = Arduino()
        self.__serial = self.Arduino.initArduino()
        self.__conf = ConfigReader()
        # self.__cont = Controller()
        self.__delay = float(self.__conf.readConfigParameter('DelayMain'))
        
        self.__socket = Server()
        self.__socket.start()
        socketThread = threading.Thread(target=self.__socketRead, name='SocketReadThread')
        socketThread.daemon = True
        socketThread.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print('Program exit, resetting GPIO-Pins...')
        finally:
            self.__exit_handler()

    def __socketRead(self):
        while True:
            try:
                dataLine = self.__socket.getData()
                #print(f'fata : {dataLine}')
                self.Arduino.sendMessage(dataLine, self.__serial)
                time.sleep(self.__delay)
            except Exception as e:
                print('Error occurred during reading from socket-server!', e)

    def __exit_handler(self):
        self.Arduino.close(self.__serial)

if __name__ == '__main__':
    main = Main()
    #((0-255),(0/1),(0-255),(0/1),(-32768-32767),y)
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
    
    
    
