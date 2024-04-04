#!/usr/bin/env python3
# @author: Markus Kösters
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ButtonData(ABC):
    # Defining the attributes of a single button.
    ID: int
    value: int

@dataclass
class ButtonsInterface(ABC):
    buttonData: ButtonData

    @property
    @abstractmethod
    def getButtonDict(self) -> dict:
        """
        Interface-Method for the process-method of a Buttons-object.
        :return:
        """

