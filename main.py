#!/usr/bin/env python3
# @author   Markus Kösters

import threading
import os

import Runners
from BusTransactions.BusFactory import BusFactory
from Events import EventFactory

# from Configurations.ConfigReader import ConfigReader

os.chdir(os.path.dirname(os.getcwd()))


class Main:

    __ports: dict = {'controllerPort': 2001}

    def __init__(self):
        """Starting the Robot-Program and configuring everything"""
        self.__asyncRunner = Runners.asyncRunner.AsyncRunner()
        self.__setup()
        self.__asyncRunner.runTasks()

    def __setup(self):
        remoteControlSocket = BusFactory.produceUDP_Transceiver(host=True, port=self.__ports.get('controllerPort'))
        arduinoSerial = BusFactory.produceSerialTransceiver()
        remoteControlEvent = EventFactory.produceEvent('controllerEvent')
        remoteControlEvent.subscribe(arduinoSerial.writeSingleMessage)
        self.__asyncRunner.addTask(remoteControlSocket.readBusUntilStopFlag(remoteControlEvent.notifySubscribers))


if __name__ == '__main__':
    main = Main()