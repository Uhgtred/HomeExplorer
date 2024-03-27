#!/usr/bin/env python3
# @author: Markus Kösters

from abc import ABC, abstractmethod

from .ButtonConfig import ButtonConfig


class ControlDevice(ABC):

    @abstractmethod
    def getButtonDict(self, buttons: ButtonConfig) -> dict:
        """
        Interface-method to process input-object containing control-information.
        """


class Controller(ControlDevice):

    def getButtonDict(self, buttons: ButtonConfig) -> dict:
        """
        Method for processing input-object.
        :return: Dictionary containing control-information.
        """
        return self.__getValuesFromObject(buttons)

    def __getValuesFromObject(self, buttons: ButtonConfig) -> dict:
        """
        Extract all the values from the buttons-object.
        :param buttons: Object that stores information about the buttons pushed on the remote-side.
        :return: Dictionary containing the id of the buttons as key and their value as value.
        """
        buttonDict: dict = {
                                str(buttons.LTrigger): buttons.LTrigger.value if buttons.LBtn.value == 0 else -buttons.LTrigger.value,
                                str(buttons.RTrigger.ID): buttons.RTrigger.value if buttons.RBtn.value == 0 else -buttons.RTrigger.value,
                                str(buttons.RXAxis.ID): buttons.RXAxis.value,
                                str(buttons.RYAxis.ID): buttons.RYAxis.value
                            }
        return buttonDict
