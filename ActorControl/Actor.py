#!/usr/bin/env python3
# @author: Markus Kösters
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, fields, asdict

from ActorControl.ActorControlInterface import Buttons


class Actors(ABC):

    @abstractmethod
    def setButton(self, button: Buttons) -> None:
        """
        Setter-Method for the button that will be used.
        :param button: Button that will be set.
        """

    @abstractmethod
    @classmethod
    def getValue(cls) -> int:
        """
        Abstract method to receive the value from the corresponding button.
        """


class LeftMotor(Actors):
    __button = Buttons.LTrigger
    __reverseButton = Buttons.LBtn

    @classmethod
    def setButton(cls, button: Buttons) -> None:
        cls.__button = button

    @classmethod
    def getValue(cls) -> int:
        if cls.__reverseButton.value:
            return cls.__button.value * -1
        return cls.__button.value


class ActorController:
    __actorValues: json
    __actors = {'left_motor': LeftMotor}  # , 'right_motor', 'left_motor_reverse', 'right_motor_reverse'}

    def initActorButtons(self, buttons: Buttons) -> None:
        for button, button_data in asdict(buttons).items():
            self.__actors[button_data.Actor].setButton(button)

    def updateActors(self, buttons: Buttons) -> None:
        for button, button_data in asdict(buttons).items():
            self.__actors[button_data.Actor].setButton(button)
