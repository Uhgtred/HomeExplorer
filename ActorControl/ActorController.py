#!/usr/bin/env python3
# @author: Markus Kösters

import json

from BusTransactions import Bus
from . import ControlDevice
from .ActorControlInterface import ButtonConfig, ActorControlInterface
from .ControlDevice import Controller, mockController


class ActorController(ActorControlInterface):

    def __init__(self, transmitterMethod: Bus.writeSingleMessage):
        """
        Todo: let devices be a dictionary that is being provided by the factory.
        :param transmitterMethod:
        """
        self.__transmitterMethod = transmitterMethod
        self.__devices = {'xbox_controller': Controller(), 'test': mockController(), 'keyboard_controller': mockController()}

    def processInput(self, buttons: ButtonConfig) -> None:
        """
        Method to decide over which device will handle the control-values.
        :param buttons: Object containing information about the control device and the values of the readings.
        """
        buttonProcessingClass = self.decideControlDevice(buttons)
        jsonMessage = buttonProcessingClass.getButtonDict(buttons)
        self.__transmitterMethod(self.transformValuesToJson(jsonMessage))

    def decideControlDevice(self, buttons: ButtonConfig) -> ControlDevice.ControlDevice:
        """
        Method for determining the device that the Buttons-object is connected to.
        :param buttons: Buttons-object containing information about the buttons.
        :return: ControlDevice-object containing information about the way that the button-inputs will be processed.
        """
        match buttons.ActorType:
            case 'xbox_controller':
                return self.__devices.get('xbox_controller')
            case 'test':
                return self.__devices.get('test')
            case 'keyboard_controller':
                return self.__devices.get('keyboard_controller')
            case other:
                raise BaseException(f'Unsupported device type: {buttons.ActorType}, please choose from: {self.__devices.keys()}')

    @staticmethod
    def transformValuesToJson(message: dict) -> json:
        """
        Method for transforming values to json.
        :param message: Dictionary containing the values to be transformed to json.
        :return: Message that will be sent to
        """
        return json.dumps(message)
