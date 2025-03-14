#!/usr/bin/env python3
# @author: Markus Kösters

import json
from inspect import signature

from select import select

import ProjectLogging
from .ActorControlInterface import ActorControlInterface
from .ButtonConfig import ButtonConfig
from .ButtonsInterface import ButtonsInterface
from .UnitTests.TestActorController import Buttons

enum


class ActorController(ActorControlInterface):

    __logger: ProjectLogging.Logger.getLogger = ProjectLogging.Logger('ActorController',
                                                                      'ActorController.log').getLogger

    def __init__(self, transmitterMethod: callable, inputDeviceType: str):
        """
        :param transmitterMethod: Method used to transmit data. Needs to accept one input argument.
        :param inputDeviceType: This defines which input-device is connected. For example 'xbox_controller'.
        """
        self.__inputDeviceType: str = inputDeviceType
        self.__checkInputArgs(transmitterMethod, 1)
        self.__transmitterMethod = transmitterMethod

    @staticmethod
    def __remapButtons(buttonDict: dict, configDict: dict) -> dict:
        """
        Method used to remap buttons according to config and transmitter method.
        :param buttonDict: Button dictionary to be remapped.
        :param configDict: Dictionary containing the new keys as values and old keys as keys.
        :return: Remapped dictionary.
        """
        ActorController.__logger.debug(f'Buttons that are going to be remapped: {buttonDict}, '
                                       f'with config: {configDict}')
        newButtonsDict: dict = {}
        for key in buttonDict.keys():
            newKey: str = configDict.get(str(key))
            newButtonsDict[newKey] = buttonDict.get(key)
        return newButtonsDict

    @staticmethod
    def __checkInputArgs(method: callable, numberOfArgs: int) -> None:
        """
        Method for checking number of input arguments for a given method. Raising an exception if numberOfArgs does not match the signature of the method.
        :param method: Method to check.
        """
        # raising exception if method does not accept any input-arguments.
        methodSignature = signature(method)
        if len(methodSignature.parameters) != numberOfArgs:
            raise TypeError(f'Method: {method} shall accept {numberOfArgs} argument(s), got: {len(methodSignature.parameters)}!')

    def processInput(self, buttons: Buttons) -> None:
        """
        Method to get the content of a buttons-object.
        """
        buttonDict = self._getButtonDict(buttons)
        jsonMessage = self._transformValuesToJson(buttonDict)
        self.__transmitterMethod(jsonMessage)

    def _getButtonDict(self, buttons: Buttons) -> dict:
        """
        Method for retrieving button-data from a button-object.
        :param buttons: Button-object that contains button information and state.
        :return: Dictionary containing button information and state.
        """
        buttonDict: dict = buttons.getButtonDict
        match self.__inputDeviceType.lower():
            case 'xbox_controller': return self.__remapButtons(buttonDict, ButtonConfig().xBox)

    @staticmethod
    def _transformValuesToJson(message: dict) -> json:
        """
        Method for transforming values to json.
        :param message: Dictionary containing the values to be transformed to json.
        :return: Message that will be sent to
        """
        return json.dumps(message)
