#!/usr/bin/env python3
# @author: Markus Kösters

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class ButtonData:
    # Defining the attributes of a single button.
    ID: int
    value: int
    Actor: str


@dataclass
class Buttons:
    LXAxis: ButtonData
    LYAxis: ButtonData
    LTrigger: ButtonData
    LBtn: ButtonData
    L3: ButtonData
    RXAxis: ButtonData
    RYAxis: ButtonData
    RTrigger: ButtonData
    RBtn: ButtonData
    R3: ButtonData
    StartBtn: ButtonData
    SelectBtn: ButtonData
    ABtn: ButtonData
    BBtn: ButtonData
    XBtn: ButtonData
    YBtn: ButtonData
    XCross: ButtonData
    YCross: ButtonData


class ActorControlInterface(ABC):

    @abstractmethod
    def processInput(self, buttons: Buttons) -> None:
        """
        Interface-method for describing how the input can be set.
        :param buttons: Buttons-object containing information about the buttons.
        """
