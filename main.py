#!/usr/bin/env python3
# @author   Markus Kösters

import os

import Runners
from BusTransactions.BusFactory import BusFactory
from Events import EventFactory

# changing working-directory to parent of this file
os.chdir(os.path.dirname(os.getcwd()))


class Main:
    __ports: dict = {'controllerPort': 2001}

    def __init__(self):
        """Starting the Robot-Program and configuring everything"""
        self.__asyncRunner = Runners.asyncRunner.AsyncRunner()
        self.__setup()
        self.__asyncRunner.runTasks()

    def __setup(self) -> None:
        try:
            remoteControlSocket = BusFactory.produceUDP_Transceiver(host=True, port=self.__ports.get('controllerPort'))
            arduinoSerial = BusFactory.produceSerialTransceiver()
            remoteControlEvent = EventFactory.produceEvent('controllerEvent')
            remoteControlEvent.subscribe(arduinoSerial.writeSingleMessage)
            self.__asyncRunner.addTask(remoteControlSocket.readBusUntilStopFlag(remoteControlEvent.notifySubscribers))
        except Exception as e:
            raise BaseException(f'An error occurred during setup: {e}')


if __name__ == '__main__':
    main = Main()
