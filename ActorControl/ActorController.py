#!/usr/bin/env python3
# @author: Markus Kösters

import json
from dataclasses import fields

from .ActorControlInterface import Buttons, ActorControlInterface
from .ControlDevice import Controller, ControlDevice
from BusTransactions import Bus


class ActorController(ActorControlInterface):

    def __init__(self, transmitterMethod: Bus.writeSingleMessage):
        self.__transmitterMethod = transmitterMethod

    def processInput(self, buttons: Buttons) -> None:
        """
        Method to decide over which device will handle the control-values.
        :param buttons: Object containing information about the control device and the values of the readings.
        """
        buttonProcessingClass = self.__decideControlDevice(buttons)
        jsonMessage = buttonProcessingClass.processInput()
        self.__transmitter(self.__transformValuesToJson(jsonMessage))

    def __decideControlDevice(self, buttons: Buttons) -> ControlDevice:
        """
        Method for determining the device that the Buttons-object is connected to.
        :param buttons: Buttons-object containing information about the buttons.
        :return: ControlDevice-object containing information about the way that the button-inputs will be processed.
        """
        match buttons.ActorType:
            case 'xbox_controller':
                buttonProcessingClass = Controller(buttons)
            case 'keyboard':
                pass
            case other:
                raise BaseException(f'No supported controller! {buttons.ActorType}')
        return buttonProcessingClass

    @staticmethod
    def __transformValuesToJson(message: dict) -> json:
        """
        Method for transforming values to json.
        :param message: Dictionary containing the values to be transformed to json.
        :return: Message that will be sent to
        """
        jsonMessage = json.dumps(message)
        return jsonMessage
