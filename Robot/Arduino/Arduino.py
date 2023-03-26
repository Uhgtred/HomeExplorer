#!/usr/bin/env python3
# @author      Markus Kösters

import serial
import time

from Configurations.ConfigReader import ConfigReader


class Arduino:

    def __init__(self):
        self.__conf = ConfigReader()
        self.__Arduino = self.__conf.readConfigParameter('ArduinoPort')
        self.__baudRate = int(self.__conf.readConfigParameter('ArduinoBaudRate'))
        self.__format = self.__conf.readConfigParameter('MessageFormat')
        self.__delay = float(self.__conf.readConfigParameter('SerialTimeOut'))
        self.device = None

    @property
    def rcvMessage(self):
        if self.device is None:
            self.initArduino()
        return self.device.readline()

    def sendMessage(self, message):
        if self.device is None:
            self.initArduino()
        message += b'&'
        # print(f'sending: {message} length: {len(message)}')# to: {self.device}')  # debugging-line
        self.device.reset_output_buffer()
        self.device.write(message)
        time.sleep(self.__delay)

    def close(self):
        if self.device is not None:
            self.device.close()

    def initArduino(self):
        device = serial.Serial()
        device.baud = self.__baudRate
        device.port = self.__Arduino
        # device.timeout = self.__delay  # not sure if this is needed anymore
        device.open()
        self.device = device


if __name__ == '__main__':
    import time
    # import /home/pi/Desktop/Robot_V1_0_2_1/Configurations/ConfigReader
    obj = Arduino()
    device = obj.initArduino()
    while True:
        obj.sendMessage(('Test'), device)
        print(obj.readMessage(device))
        time.sleep(0.05)
