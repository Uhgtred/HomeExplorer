#!/usr/bin/env python3
# @author: Markus Kösters

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, fields, asdict

from ActorControl.ActorControlInterface import Buttons


class ActorController:

    def __init__(self, transmitter: BusFactory):
        self.__transmitter = transmitter.produceSerialTransceiver()
        self.__jsonMessage = {Buttons.LTrigger.ID: 0}
        # the key is the negator, and the value is the button-value that will be negated
        self.__negatorButtons = {Buttons.LBtn.ID: [Buttons.LTrigger.ID, False], Buttons.RBtn.ID: [Buttons.RTrigger.ID, False]}

    def processInput(self, buttons: Buttons) -> None:
        """
        Method for processing input-object.
        :return:
        """
        self.__getValuesFromObject(buttons)
        jsonMessage = self.__transformValuesToJson(self.__jsonMessage)
        self.__transmitter.writeSingleMessage(jsonMessage)


    def __getValuesFromObject(self, buttons: Buttons) -> dict:
        """
        Extract all the values from the buttons-object.
        :param buttons: Object that stores information about the buttons pushed on the remote-side.
        :return: Dictionary containing the id of the buttons as key and their value as value.
        """
        for field in fields(buttons):
            attributes = getattr(buttons, field.name)
            # if the button is a negator, negate the assigned value if its own value is 1.
            if attributes.ID in self.__negatorButtons.keys():
                self.__negatorButtons.get(attributes.ID)[1] = attributes.value
                continue
            self.__jsonMessage[attributes.ID] = attributes.value
        self.__negateActorValues()

    def __negateActorValues(self) -> None:
        """
        Method for negating the value of a button.
        """
        # if buttonNegator is true setting the value in the message to negativ!
        for buttonNegator in self.__negatorButtons:
            if buttonNegator[1]:
                self.__jsonMessage[buttonNegator[0]] = -self.__jsonMessage[buttonNegator[0]]

    @staticmethod
    def __transformValuesToJson(message: dict) -> json:
        """
        Method for transforming values to json.
        :param message: Dictionary containing the values to be transformed to json.
        :return: Message that will be sent to
        """
        jsonMessage = json.dumps(message)
        return jsonMessage
