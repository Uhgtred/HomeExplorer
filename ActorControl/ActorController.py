#!/usr/bin/env python3
# @author: Markus Kösters

import json
from inspect import signature

from .ActorControlInterface import ActorControlInterface
from .ButtonsInterface import ButtonsInterface


class ActorController(ActorControlInterface):

    def __init__(self, transmitterMethod: callable):
        """
        :param transmitterMethod:
        """
        transmitterSignature = signature(transmitterMethod)
        if len(transmitterSignature.parameters) != 1:
            raise TypeError(f'Transmitter method shall expect 1 argument, got {len(transmitterSignature.parameters)}!')
        self.__transmitterMethod = transmitterMethod

    def processInput(self, buttons: ButtonsInterface) -> None:
        """
        Method to get the content of a buttons-object.
        """
        jsonMessage = self._transformValuesToJson(self._getButtonDict(buttons))
        self.__transmitterMethod(jsonMessage)

    @staticmethod
    def _getButtonDict(buttons: ButtonsInterface) -> dict:
        """
        Method for retrieving button-data from a button-object.
        :param buttons: Button-object that contains button information and state.
        :return: Dictionary containing button information and state.
        """
        if callable(buttons):
            buttons = buttons()
        buttonDict: dict = buttons.getButtonDict
        return buttonDict

    @staticmethod
    def _transformValuesToJson(message: dict) -> json:
        """
        Method for transforming values to json.
        :param message: Dictionary containing the values to be transformed to json.
        :return: Message that will be sent to
        """
        return json.dumps(message)
