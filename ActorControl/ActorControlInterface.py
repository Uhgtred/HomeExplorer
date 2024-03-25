#!/usr/bin/env python3
# @author: Markus Kösters
import json
from abc import ABC, abstractmethod

from .ButtonConfig import ButtonConfig
from .ControlDevice import ControlDevice


class ActorControlInterface(ABC):

    @abstractmethod
    def processInput(self, buttons: ButtonConfig) -> None:
        """
        Interface-method for describing how the input can be set.
        :param buttons: Buttons-object containing information about the buttons.
        """

    @staticmethod
    @abstractmethod
    def __transformValuesToJson(message: dict) -> json:
        """
        Interface-method for transforming the message into json-format.
        :param message: Dictionary containing information about the buttons pressed and their value.
        :return: Json-formatted message.
        """

    @abstractmethod
    def __decideControlDevice(self, buttons: ButtonConfig) -> ControlDevice:
        """
        Interface-method for determining the device that the Buttons-object is connected to.
        :param buttons: Buttons-object containing information about the buttons.
        :return: ControlDevice-object containing information about the way that the button-inputs will be processed.
        """