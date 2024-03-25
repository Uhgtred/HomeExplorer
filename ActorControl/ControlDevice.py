#!/usr/bin/env python3
# @author: Markus Kösters

from ActorControl.ActorControlInterface import Buttons


class ControlDevice(ABC):

    @abstractmethod
    def processInput(self) -> dict:
        """
        Interface-method to process input-object containing control-information.
        """


class Controller(ControlDevice):

    def getButtonDict(self, buttons: Buttons) -> dict:
        """
        Method for processing input-object.
        :return: Dictionary containing control-information.
        """
        return self.__getValuesFromObject(buttons)

    def __getValuesFromObject(self, buttons: Buttons) -> dict:
        """
        Extract all the values from the buttons-object.
        :param buttons: Object that stores information about the buttons pushed on the remote-side.
        :return: Dictionary containing the id of the buttons as key and their value as value.
        """
        buttonDict = {}
        self.__buttonDict[buttons.LTrigger.ID] = buttons.LTrigger.value if buttons.LBtn.value == 0 else -buttons.LTrigger.value
        self.__buttonDict[buttons.RTrigger.ID] = buttons.RTrigger.value if buttons.RBtn.value == 0 else -buttons.RTrigger.value
        self.__buttonDict[buttons.RXAxis.ID] = buttons.RXAxis.value
        self.__buttonDict[buttons.RYAxis.ID] = buttons.RYAxis.value
        return buttonDict
