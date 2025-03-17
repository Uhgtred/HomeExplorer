#!/usr/bin/env python3
# @author: Markus Kösters

import json
import unittest
from dataclasses import field, dataclass

from ..ActorControlFactory import ActorControlFactory

@dataclass
class ButtonData:
    # Defining the style of a button.
    ID: int
    value: int

@dataclass
class Buttons:
    LTrigger: ButtonData = field(default_factory=lambda: ButtonData(2, 20))  # max value: ButtonData = ButtonDef(255
    LBtn: ButtonData = field(default_factory=lambda: ButtonData(310, 1))
    RTrigger: ButtonData = field(default_factory=lambda: ButtonData(5, 20))  # max value: ButtonData = ButtonDef(255
    RBtn: ButtonData = field(default_factory=lambda: ButtonData(311, 0))

    @property
    def getButtonDict(self) -> dict:
        buttonDict = {
            self.LTrigger.ID: self.LTrigger.value if self.LBtn.value == 0 else -self.LTrigger.value,
            self.RTrigger.ID: self.RTrigger.value if self.RBtn.value == 0 else -self.RTrigger.value
        }
        return buttonDict


class TestActorController(unittest.TestCase):

    def setUp(self):
        self.buttons = Buttons
        self.message = None

    def test_transmitterWrongNumberOfArguments(self):
        self.assertRaises(TypeError, ActorControlFactory.produceActorControlXbox, transmitterMethod=self.transmitterHelperMethod2Arguments)

    def test_processInput(self):
        actorController = ActorControlFactory.produceActorControlXbox(transmitterMethod=self.transmitterHelperMethod)
        actorController.processInput(buttons=self.buttons.getButtonDict)
        # creating the json-string manually
        buttonData = actorController._getButtonDict(self.buttons)
        self.assertEqual(json.dumps(buttonData), self.message)

    def transmitterHelperMethod(self, message: json):
        self.message = message

    def transmitterHelperMethod2Arguments(self, message: json, buttons: dict):
        pass


if __name__ == '__main__':
    unittest.main()
