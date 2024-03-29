#!/usr/bin/env python3
# @author: Markus Kösters

import unittest
from dataclasses import field, dataclass, asdict

from ActorControl.ActorControlFactory import ActorControlFactory


@dataclass
class ButtonData:
    # Defining the style of a button.
    ID: int
    value: int


@dataclass
class Buttons:
    ActorType: str = 'test'
    LTrigger: ButtonData = field(default_factory=lambda: ButtonData(2, 20))  # max value: ButtonData = ButtonDef(255
    LBtn: ButtonData = field(default_factory=lambda: ButtonData(310, 1))
    RTrigger: ButtonData = field(default_factory=lambda: ButtonData(5, 20))  # max value: ButtonData = ButtonDef(255
    RBtn: ButtonData = field(default_factory=lambda: ButtonData(311, 0))


class test_ActorController(unittest.TestCase):

    def setUp(self):
        self.actorController = ActorControlFactory.produceActorControl(stub=True)
        self.buttons = Buttons()

    def test_processInput(self):
        self.actorController.processInput(buttons=self.buttons)
        dictionary = {self.buttons.LTrigger.ID: -self.buttons.LTrigger.value, self.buttons.RTrigger.ID: self.buttons.RTrigger.value}
        self.assertDictEqual(dictionary, self.actorController._ActorController__devices.get('test').value)

    def test_unsupportedDevice(self):
        self.buttons.ActorType = 'something_unsupported'
        self.assertRaises(BaseException, self.actorController.decideControlDevice, self.buttons)


if __name__ == '__main__':
    unittest.main()
