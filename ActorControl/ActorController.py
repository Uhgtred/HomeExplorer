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

Maybe better use this:
"""
from abc import ABC, abstractmethod


# Define a family of algorithms (ControlDeviceProcessing)
class ControlDeviceProcessing(ABC):
    @abstractmethod
    def process(self, buttons: ButtonConfig):
        pass


# Each algorithm is encapsulated in its own class
class XboxControllerProcessing(ControlDeviceProcessing):
    def process(self, buttons: ButtonConfig):
        # logic for Xbox Controller
        pass


class KeyboardControllerProcessing(ControlDeviceProcessing):
    def process(self, buttons: ButtonConfig):
        # logic for Keyboard Controller
        pass


# The ActorController now uses composition to use the strategy
class ActorController:
The device_processing_strategy could be provided by the buttons-object
Maybe the buttons-object needs to be a normal class then, including methods that allow to process the data. 
    def __init__(self, device_processing_strategy: ControlDeviceProcessing):
        self.device_processing_strategy = device_processing_strategy

    def processInput(self, buttons: ButtonConfig) -> None:
        jsonMessage = self.device_processing_strategy.process(buttons)
        self.__transmitterMethod(self.transformValuesToJson(jsonMessage))
"""