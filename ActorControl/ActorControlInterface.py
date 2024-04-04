#!/usr/bin/env python3
# @author: Markus Kösters

import json
from abc import ABC, abstractmethod

from ActorControl.ButtonsInterface import ButtonsInterface


class ActorControlInterface(ABC):

    @abstractmethod
    def processInput(self, buttons: ButtonsInterface) -> None:
        """
        Interface-method for describing how the input can be set.
        :param buttons: Buttons-object containing information about the buttons.
        """

    @staticmethod
    @abstractmethod
    def _transformValuesToJson(message: dict) -> json:
        """
        Interface-method for transforming the message into json-format.
        :param message: Dictionary containing information about the buttons pressed and their value.
        :return: Json-formatted message.
        """

    @staticmethod
    @abstractmethod
    def _getButtonDict(buttons: ButtonsInterface) -> dict:
        """
        Interface-Method for retrieving button-data from a button-object.
        :param buttons: Button-object that contains button information and state.
        :return: Dictionary containing button information and state.
        """