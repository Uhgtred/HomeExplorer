#!/usr/bin/env python3
# @author: Markus Kösters

import json
from inspect import signature, Signature
import typing

import ProjectLogging
from .ActorControlInterface import ActorControlInterface


class ActorController(ActorControlInterface):
    """
    This class is responsible for controlling an actor using inputs from various
    devices, mapping inputs appropriately, and transmitting the data in a
    standardized format.

    The ActorController interfaces with inputs from devices such as game controllers,
    remaps button configurations based on predefined settings, and processes the
    input data into a format that can be transmitted to perform specific actions.

    :ivar __logger: Logger instance for debugging and tracking activities in the
        ActorController.
    :type __logger: ProjectLogging.Logger.getLogger
    :ivar __inputDeviceType: Specifies the type of input device connected, such as
        'xbox_controller'.
    :type __inputDeviceType: str
    :ivar __transmitterMethod: Callable method used to transmit the processed
        input data.
    :type __transmitterMethod: callable
    """
    __logger: ProjectLogging.Logger.getLogger = ProjectLogging.Logger('ActorController',
                                                                      'ActorController.log').getLogger

    def __init__(self, transmitterMethod: typing.Callable):
        """
        :param transmitterMethod: Method used to transmit data. Needs to accept one input argument.
        :param inputDeviceType: This defines which input-device is connected. For example 'xbox_controller'.
        """
        self.__checkInputArgs(transmitterMethod, 2)
        self.__transmitterMethod = transmitterMethod

    @staticmethod
    def __checkInputArgs(method: typing.Callable, numberOfArgs: int) -> None:
        """
        Method for checking number of input arguments for a given method. Raising an exception if numberOfArgs does not match the signature of the method.
        :param method: Method to check.
        """
        # raising exception if method does not accept any input-arguments.
        methodSignature: Signature = signature(method)
        if len(methodSignature.parameters) > numberOfArgs:
            raise TypeError(f'Method: {method} shall accept {numberOfArgs} argument(s), got: {len(methodSignature.parameters)}!')

    def processInput(self, buttonJson: str) -> None:
        """
        Processes input buttons by converting their data into a JSON message and transmitting it.

        This function performs the following steps:
        1. Extracts button data into a dictionary by calling an internal method.
        2. Converts the dictionary values into a JSON-formatted string.
        3. Sends the resultant JSON message using a private transmitter method.

        :param buttons: The Buttons object containing input data to be processed.
        :return: None
        """
        # jsonMessage = self._transformValuesToJson(buttonDict)
        self.__transmitterMethod(buttonJson)

    @staticmethod
    def _transformValuesToJson(message: dict) -> str:
        """
        Transforms a given dictionary message into a JSON formatted string.

        :param message: The dictionary object to be converted to a JSON string.
        :type message: dict
        :return: JSON formatted string representation of the dictionary.
        :rtype: json
        """
        return json.dumps(message)
