#!/usr/bin/env python3
# @author: Markus Kösters
from dataclasses import fields

from ActorControl.ActorControlInterface import ActorControlInterface, Buttons


class InputProcessor(ActorControlInterface):

    __inputValues = None

    def setInputValues(self, inputValues: Buttons) -> None:
        self.__inputValues = inputValues()

    def process(self) -> None:
        for button in fields(self.__inputValues):
            fieldContent = getattr(self.__inputValues, button.name)
            fieldContent.Actor
        