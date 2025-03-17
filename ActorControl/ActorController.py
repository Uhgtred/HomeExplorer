#!/usr/bin/env python3
# @author: Markus Kösters

import json
from inspect import signature

import logging

from .ButtonsInterface import ButtonsInterface
from .ActorControlInterface import ActorControlInterface
from .ButtonConfig import ButtonConfig

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
    __logger: logging.getLogger = logging.getLogger(__name__)

    def __init__(self, transmitterMethod: callable, inputDeviceType: str):
        """
        :param transmitterMethod: Method used to transmit data. Needs to accept one input argument.
        :param inputDeviceType: This defines which input-device is connected. For example 'xbox_controller'.
        """
        self.__inputDeviceType: str = inputDeviceType
        print(f'transmitterMethod: {transmitterMethod}, {signature(transmitterMethod)}')
        self.__logger.debug(f'Input Device Type: {self.__inputDeviceType}')
        self.__checkInputArgs(transmitterMethod, 2)
        self.__transmitterMethod = transmitterMethod

    @staticmethod
    def __remapButtons(buttonDict: dict, configDict: dict) -> dict:
        """
        Remaps the keys of a given dictionary that represents buttons using a configuration
        dictionary mapping old keys to new keys. This functionality is typically used
        to adjust configurations dynamically based on user preferences or system specifications.

        .. note::
           This method performs logging for debugging purposes before the remapping process begins.

        :param buttonDict: A dictionary where keys represent current buttons and values
           represent associated data or actions bound to those buttons.
        :param configDict: A dictionary that defines the mapping of old button keys
           to new button keys. The keys are existing buttons, and the values are the
           new keys to replace them.
        :return: A new dictionary where keys of `buttonDict` have been remapped using
           `configDict`. If a key in `buttonDict` does not have a corresponding key in
           `configDict`, it will not appear in the resulting dictionary.
        :rtype: dict
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
        methodSignature: signature = signature(method)
        if len(methodSignature.parameters) > numberOfArgs:
            raise TypeError(f'Method: {method} shall accept {numberOfArgs} argument(s), got: {len(methodSignature.parameters)}!')

    def processInput(self, buttons: ButtonsInterface) -> None:
        """
        Processes input buttons by converting their data into a JSON message and transmitting it.

        This function performs the following steps:
        1. Extracts button data into a dictionary by calling an internal method.
        2. Converts the dictionary values into a JSON-formatted string.
        3. Sends the resultant JSON message using a private transmitter method.

        :param buttons: The Buttons object containing input data to be processed.
        :return: None
        """
        buttonDict = self._getButtonDict(buttons)
        jsonMessage = self._transformValuesToJson(buttonDict)
        self.__transmitterMethod(jsonMessage)

    def _getButtonDict(self, buttons: ButtonsInterface) -> dict:
        """
        Converts button configuration into a dictionary remapped to the specific input device
        type's button configuration. Supports handling various device types for consistent
        button mapping across different input devices.

        :param buttons: Buttons instance containing the button configuration to be converted.
        :type buttons: Buttons
        :return: Dictionary of button mappings remapped for the corresponding input device
            type defined by the instance's configuration.
        :rtype: dict
        """
        buttonDict: dict = buttons.getButtonDict
        match self.__inputDeviceType.lower():
            case 'xbox_controller': return self.__remapButtons(buttonDict, ButtonConfig().xBox)
            case default: return self.__remapButtons(buttonDict, ButtonConfig().default)

    @staticmethod
    def _transformValuesToJson(message: dict) -> json:
        """
        Transforms a given dictionary message into a JSON formatted string.

        :param message: The dictionary object to be converted to a JSON string.
        :type message: dict
        :return: JSON formatted string representation of the dictionary.
        :rtype: json
        """
        return json.dumps(message)
