#!/usr/bin/env python3
# @author: Markus Kösters

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, fields, asdict

from ActorControl.ActorControlInterface import Buttons


class ActorController:

    def __init__(self, transmitter: BusFactory):
        self.__transmitter = transmitter.produceSerialTransceiver()
        self.__actors = {Buttons.LTrigger.ID: 0, Buttons.LBtn.ID: LeftMotor}
        self.__jsonMessage = {Buttons.LTrigger.ID: 0, Buttons.LBtn.ID: 0}
        # the key is the negator, and the value is the button-value that will be negated
        self.__negatorButtons = {Buttons.LBtn.ID: Buttons.LTrigger.ID, Buttons.RBtn.ID: Buttons.RTrigger.ID}

    def processInput(self, buttons: Buttons) -> None:
        """
        Method for processing input-object.
        :return:
        """
        self.getValuesFromObject(buttons)
        jsonMessage = self.__transformValuesToJson(self.__jsonMessage)
        self.__transmitter.writeSingleMessage(jsonMessage)


    def getValuesFromObject(self, buttons: Buttons) -> dict:
        for field in fields(buttons):
            attributes = getattr(buttons, field.name)
            # if the button is a negator, negate the value. else
            if attributes.ID in self.__negatorButtons.keys():
                self.negateActorValue(self.__negatorButtons.get(attributes.ID))
                continue
            if self.__jsonMessage.get(attributes.ID) == -1:
                self.negateActorValue(attributes.ID)
            else:
                self.__jsonMessage[attributes.ID] = attributes.value

    def negateActorValue(self, buttonID: Buttons.name.ID) -> None:
        """
        Method for negating the value of a button.
        :param buttonID: ID of the button whose value will be negated.
        """
        if self.__jsonMessage[buttonID] == 0:
            self.__jsonMessage[buttonID] = -1
        self.__jsonMessage[buttonID] = -self.__jsonMessage[buttonID]

    @staticmethod
    def __transformValuesToJson(message: dict) -> json:
        """
        Method for transforming values to json.
        :param message: Dictionary containing the values to be transformed to json.
        :return: Message that will be sent to
        """
        jsonMessage = json.dumps(message)
        return jsonMessage
