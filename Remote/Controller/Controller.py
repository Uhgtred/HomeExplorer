#!/usr/bin/env python3
# @author   Markus Kösters

from evdev import InputDevice
import subprocess
from Configuration.ConfigReader import ConfigReader


class Controller:

    def __init__(self):
        self.__conf = ConfigReader()
        self.__deviceVendor = int(self.__conf.readConfigParameter('DeviceVendorID'))
        self.__lValue = 0
        self.__rValue = 0
        self.__rBack = 0
        self.__lBack = 0
        self.__rStickXValue = 0
        self.__rStickYValue = 0

        self.__LXAxis = int(self.__conf.readConfigParameter('LXAxis'))
        self.__LYAxis = int(self.__conf.readConfigParameter('LYAxis'))
        self.__LTrigger = int(self.__conf.readConfigParameter('LTrigger'))
        self.__LBtn = int(self.__conf.readConfigParameter('LBtn'))
        self.__L3 = int(self.__conf.readConfigParameter('L3'))

        self.__RXAxis = int(self.__conf.readConfigParameter('RXAxis'))
        self.__RYAxis = int(self.__conf.readConfigParameter('RYAxis'))
        self.__RTrigger = int(self.__conf.readConfigParameter('RTrigger'))
        self.__RBtn = int(self.__conf.readConfigParameter('RBtn'))
        self.__R3 = int(self.__conf.readConfigParameter('R3'))

        self.__StartBtn = int(self.__conf.readConfigParameter('StartBtn'))
        self.__SelectBtn = int(self.__conf.readConfigParameter('SelectBtn'))

        self.__ABtn = int(self.__conf.readConfigParameter('ABtn'))
        self.__BBtn = int(self.__conf.readConfigParameter('BBtn'))
        self.__XBtn = int(self.__conf.readConfigParameter('XBtn'))
        self.__YBtn = int(self.__conf.readConfigParameter('YBtn'))

        self.__XCross = int(self.__conf.readConfigParameter('XCross'))
        self.__YCross = int(self.__conf.readConfigParameter('YCross'))

    def initController(self):
        """Automatically detects, connects and returns (object) the controller with the vendor-ID specified in Configurations.conf! Only works on linux!"""
        __path = self.__conf.readConfigParameter('ControllerPath')
        __temp = subprocess.Popen(['ls', __path], stdout=subprocess.PIPE)
        __controller = None

        __temp = __temp.communicate()
        deviceList = (__temp[0]).decode()
        deviceList = deviceList.split('\n')

        for element in deviceList:
            element = f'{__path}{element}'
            if 'event' in element:
                if InputDevice(element).info.vendor == self.__deviceVendor:
                    __controller = InputDevice(element)
        return __controller

    def readController(self, controller):
        """Reads controller-output in a loop! Controller-object needed, this is being returned by initController!"""
        try:
            __controller = controller
            __controller.grab()  # makes the controller only listen to this Code
            for event in __controller.read_loop():  # better with dictionary?
                if event.code == self.__LBtn:
                    self.__reverse(event, 'left')
                elif event.code == self.__LTrigger:
                    self.__lValue = event.value
                elif event.code == self.__RBtn:
                    self.__reverse(event, 'right')
                elif event.code == self.__RTrigger:
                    self.__rValue = event.value
                elif event.code == self.__RXAxis:
                    self.__rStickXValue = event.value
                elif event.code == self.__RYAxis:
                    self.__rStickYValue = event.value
                # elif event.code == self.__StartBtn and event.value:
                #     __start = time.time()
                # elif event.code == self.__StartBtn and not event.value: # for remote only makes sense if send to robot
                #     if time.time() - __start >= 5:
                #         os.system('sudo shutdown now')
        except Exception as e:
            print(f'Error while trying to read Controller output! {e}')

    def __reverse(self, event, side):
        __event = event
        __side = side
        if event.value:
            if __side == 'left':
                self.__lBack = 1
            elif __side == 'right':
                self.__rBack = 1
        elif not event.value:
            if __side == 'left':
                self.__lBack = 0
            elif __side == 'right':
                self.__rBack = 0

    def getControllerValues(self):
        """Returning the values for Track-Control"""
        __rStickXValue = 0  
        __rStickYValue = 0  
        __rStickXValueNeg = 0
        __rStickYValueNeg = 0
        __rStickXValuePos = 0
        __rStickYValuePos = 0
        __lValue = 0  
        __lValue = self.__lValue
        __lBack = self.__lBack
        __rValue = 0  
        __rValue = self.__rValue
        __rBack = self.__rBack
        if self.__rStickXValue > 0:
            __rStickXValuePos = self.__rStickXValue / 128.5
            __rStickXValuePos = round(__rStickXValuePos)
        elif self.__rStickXValue < 0:
            __rStickXValueNeg = self.__rStickXValue * (-1)
            __rStickXValueNeg = __rStickXValueNeg / 128.5
            __rStickXValueNeg = round(__rStickXValueNeg)
        else:
            __rStickXValueNeg = 0
            __rStickXValuePos = 0
        if self.__rStickYValue > 0:
            __rStickYValuePos = self.__rStickYValue / 128.5
            __rStickYValuePos = round(__rStickYValuePos)
        elif self.__rStickYValue < 0:
            __rStickYValueNeg = self.__rStickYValue * (-1)
            __rStickYValueNeg = __rStickYValueNeg / 128.5
            __rStickYValueNeg = round(__rStickYValueNeg)
        else:
            __rStickYValueNeg = 0
            __rStickYValuePos = 0
        __contValues = f'{str(__rValue).zfill(3)}{__rBack}{str(__lValue).zfill(3)}{__lBack}{str(__rStickXValuePos).zfill(3)}{str(__rStickXValueNeg).zfill(3)}{str(__rStickYValuePos).zfill(3)}{str(__rStickYValueNeg).zfill(3)}'
        return __contValues
