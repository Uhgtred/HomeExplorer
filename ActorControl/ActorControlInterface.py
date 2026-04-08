#!/usr/bin/env python3
# @author: Markus Kösters

import json
from abc import ABC, abstractmethod


class ActorControlInterface(ABC):

    @abstractmethod
    def processInput(self, buttons: dict) -> None:
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