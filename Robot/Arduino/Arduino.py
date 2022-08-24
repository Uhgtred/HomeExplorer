#!/usr/bin/env python3
# @author      Markus Kösters

import serial

from Configurations.ConfigReader import ConfigReader


class Arduino:

    def __init__(self):
        self.__conf = ConfigReader()
        self.__Arduino = self.__conf.readConfigParameter('ArduinoPort')
        self.__baudRate = int(self.__conf.readConfigParameter('ArduinoBaudRate'))
        self.__format = self.__conf.readConfigParameter('MessageFormat')
        self.__delay = float(self.__conf.readConfigParameter('SerialTimeOut'))

    def sendMessage(self, message, device):
        if message:
            message = message.encode(self.__format)
        device.write(message)

    def readMessage(self, device):
        if device.in_waiting:
            message = device.readline()
            if message:
                if type(message) is not str:
                    message = message.decode(self.__format).strip()
            return message

    def close(self, device):
        device.close()

    def initArduino(self):
        device = serial.Serial()
        device.baud = self.__baudRate
        device.port = self.__Arduino
        device.timeout = self.__delay
        device.open()
        return device


if __name__ == '__main__':
    # import /home/pi/Desktop/Robot_V1_0_2_1/Configuration/ConfigReader
    obj = Arduino()
    device = Arduino.initArduino()
    device.sendMessage('Hallo')
    print(device.readMessage())
