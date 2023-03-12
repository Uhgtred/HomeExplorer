#!/usr/bin/env python3
# @author   Markus Kösters

from evdev import InputDevice
import subprocess

from Configurations.ConfigReader import ConfigReader
from Network.SocketController import SocketController


class Controller:

    def __init__(self):
        self.__conf = ConfigReader()
        self.__deviceVendor = int(self.__conf.readConfigParameter('DeviceVendorID'))
        self.defineButtonConfig()
        self.__controller = None
        self.__initController()

    def defineButtonConfig(self):
        """Button configuration can be done in the config"""
        """Left side Trigger and Analog-stick"""
        self.__LXAxis = int(self.__conf.readConfigParameter('LXAxis'))
        self.__LYAxis = int(self.__conf.readConfigParameter('LYAxis'))
        self.__LTrigger = int(self.__conf.readConfigParameter('LTrigger'))
        self.__LBtn = int(self.__conf.readConfigParameter('LBtn'))
        self.__L3 = int(self.__conf.readConfigParameter('L3'))
        """Right side Trigger and Analog-stick"""
        self.__RXAxis = int(self.__conf.readConfigParameter('RXAxis'))
        self.__RYAxis = int(self.__conf.readConfigParameter('RYAxis'))
        self.__RTrigger = int(self.__conf.readConfigParameter('RTrigger'))
        self.__RBtn = int(self.__conf.readConfigParameter('RBtn'))
        self.__R3 = int(self.__conf.readConfigParameter('R3'))
        """Menu-Buttons"""
        self.__StartBtn = int(self.__conf.readConfigParameter('StartBtn'))
        self.__SelectBtn = int(self.__conf.readConfigParameter('SelectBtn'))
        """ABXY-Buttons"""
        self.__ABtn = int(self.__conf.readConfigParameter('ABtn'))
        self.__BBtn = int(self.__conf.readConfigParameter('BBtn'))
        self.__XBtn = int(self.__conf.readConfigParameter('XBtn'))
        self.__YBtn = int(self.__conf.readConfigParameter('YBtn'))
        """Cross-Buttons"""
        self.__XCross = int(self.__conf.readConfigParameter('XCross'))
        self.__YCross = int(self.__conf.readConfigParameter('YCross'))
        """Defining the values of the buttons. Button-IDs can be changed in the config-file"""
        """ORDER OF THE DICTIONARY DOES MATTER FOR RobotController.ino ON ROBOT!!!"""
        self.__buttonDict = {self.__RTrigger: 0,
                             self.__RBtn: 0,
                             self.__LTrigger: 0,
                             self.__LBtn: 0,
                             self.__RXAxis: [0, 0],
                             self.__RYAxis: [0, 0],
                             self.__LXAxis: [0, 0],
                             self.__LYAxis: [0, 0],
                             self.__L3: 0,
                             self.__R3: 0,
                             self.__StartBtn: 0,
                             self.__SelectBtn: 0,
                             self.__ABtn: 0,
                             self.__BBtn: 0,
                             self.__XBtn: 0,
                             self.__YBtn: 0,
                             self.__XCross: [0, 0],
                             self.__YCross: [0, 0]
                             }

    def __initController(self):
        """Automatically detects, connects and returns (object) the controller with the vendor-ID specified in Configurations.conf! Only works on linux!"""
        """Searching for any devices in /dev/..."""
        path = self.__conf.readConfigParameter('ControllerPath')
        temp = subprocess.Popen(['ls', path], stdout=subprocess.PIPE)
        temp = temp.communicate()
        deviceList = (temp[0]).decode()
        deviceList = deviceList.split('\n')
        """Checking if device meets the preset vendor-id. If so setting it as the controller."""
        for element in deviceList:
            element = f'{path}{element}'
            if 'event' in element:
                if InputDevice(element).info.vendor == self.__deviceVendor:
                    self.__controller = InputDevice(element)

    def readController(self):
        """Reads controller-output in a loop! Controller-object needed, this is being set by initController!"""
        """ToDo: hex-values instead of decimal"""
        self.__controller.grab()  # makes the controller only listen to this Code
        for event in self.__controller.read_loop():
            if event.code == self.__LBtn or event.code == self.__RBtn:
                self.__buttonDict[event.code] = (0 if not event.value else 1)
            else:
                if event.value < 0:
                    self.__buttonDict[event.code][1] = -1 * event.value
                if type(self.__buttonDict.get(event.code)) is list:
                    self.__buttonDict[event.code][0] = event.value
                else:
                    self.__buttonDict[event.code] = event.value

    @property
    def getControllerValues(self):
        """Sending the values for Track-Control to the robot"""
        tempList = []
        """Running through the dictionary, reading all the values and adding them to a csv-string"""
        for key in self.__buttonDict:
            keyValue = self.__buttonDict.get(key)
            """Values could be array (1D from AnalogStick)"""
            if type(keyValue) is list:
                tempList.append(round(keyValue[0] / 128.5) if keyValue[0] != 0 else 0)  # making sure the value is not greater than 255
                tempList.append(round(keyValue[1] / 128.5) if keyValue[1] != 0 else 0)  # making sure the value is not greater than 255
            else:
                tempList.append(keyValue)
        for counter, element in enumerate(tempList):
            tempList[counter] = str(element)
        contValues = ','.join(tempList)
        """returning controller-output to calling methhod/function"""
        return contValues
        # self.socketController.sendMessage(contValues, 'controller')
