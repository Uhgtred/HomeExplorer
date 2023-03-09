#!/usr/bin/env python3
# @author      Markus Kösters

import serial

from Configurations import ConfigReader


class Arduino:

    def __init__(self):
        self.__conf = ConfigReader()
        self.__Arduino = self.__conf.readConfigParameter('ArduinoPort')
        self.__baudRate = int(self.__conf.readConfigParameter('ArduinoBaudRate'))
        self.__format = self.__conf.readConfigParameter('MessageFormat')
        self.__delay = float(self.__conf.readConfigParameter('SerialTimeOut'))

    @property
    def rcvMessage(self):
        return self.device.readline()

    def sendMessage(self, message):
        self.device.write(message)

    def close(self):
        self.device.close()

    def initArduino(self):
        device = serial.Serial()
        device.baud = self.__baudRate
        device.port = self.__Arduino
        device.timeout = self.__delay
        device.open()
        self.device = device
        #return device


if __name__ == '__main__':
    import time
    # import /home/pi/Desktop/Robot_V1_0_2_1/Configurations/ConfigReader
    obj = Arduino()
    device = obj.initArduino()
    while True:
        obj.sendMessage(('Test'), device)
        print(obj.readMessage(device))
        time.sleep(0.05)
