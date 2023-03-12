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
        self.__initArduino()

    @property
    def rcvMessage(self):
        """Reading a single line from the serial-conncection to the Arduino and returning it!"""
        return self.device.readline()

    def sendMessage(self, message:bytes):
        """Writing a message <bytes> to the Arduino through the serial-connection!"""
        self.device.write(message)

    def close(self):
        """Closing the connection to the Arduino!"""
        try:
            self.device.close()
        except Exception as e:
            print(f'Could not close serial-connection to Arduino: {e}')

    def __initArduino(self):
        """
        Initialising the settings of the serial-connection.
        Settings can be changed in Configurations/Configurations.conf.
        Make sure settings on the Arduino match the settings in config-file. Arduino-settings can be changed in Arduino/MicrocontrollerCode/RobotController/RobotController.ino!
        """
        device = serial.Serial()
        device.baud = self.__baudRate
        device.port = self.__Arduino
        device.timeout = self.__delay
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
