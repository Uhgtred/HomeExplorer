#!/usr/bin/env python3
# @author: Markus Kösters

import unittest
from dataclasses import field, dataclass

from ActorControl.ActorControlFactory import ActorControlFactory
from ActorControl.ButtonConfig import ButtonConfig


@dataclass
class ButtonData:
    # Defining the style of a button.
    ID: int
    value: int


@dataclass
class Buttons:
    ActorType: str = 'xbox_controller'
    LXAxis: ButtonData = field(default_factory=lambda: ButtonData(0, 0))  # leftmost value: ButtonData = ButtonDef(-32768 rightmost value: ButtonData = ButtonDef(32767
    LYAxis: ButtonData = field(default_factory=lambda: ButtonData(1, 0))  # upmost value: ButtonData = ButtonDef(-32768 downmost value: ButtonData = ButtonDef(32767
    LTrigger: ButtonData = field(default_factory=lambda: ButtonData(2, 0))  # max value: ButtonData = ButtonDef(255
    LBtn: ButtonData = field(default_factory=lambda: ButtonData(310, 0))
    L3: ButtonData = field(default_factory=lambda: ButtonData(317, 0))
    RXAxis: ButtonData = field(default_factory=lambda: ButtonData(3, 0))  # leftmost value: ButtonData = ButtonDef(-32768 rightmost value: ButtonData = ButtonDef(32767
    RYAxis: ButtonData = field(default_factory=lambda: ButtonData(4, 0))  # upmost value: ButtonData = ButtonDef(-32768 downmost value: ButtonData = ButtonDef(32767
    RTrigger: ButtonData = field(default_factory=lambda: ButtonData(5, 0))  # max value: ButtonData = ButtonDef(255
    RBtn: ButtonData = field(default_factory=lambda: ButtonData(311, 0))
    R3: ButtonData = field(default_factory=lambda: ButtonData(318, 0))
    StartBtn: ButtonData = field(default_factory=lambda: ButtonData(315, 0))
    SelectBtn: ButtonData = field(default_factory=lambda: ButtonData(314, 0))
    ABtn: ButtonData = field(default_factory=lambda: ButtonData(304, 0))
    BBtn: ButtonData = field(default_factory=lambda: ButtonData(305, 0))
    XBtn: ButtonData = field(default_factory=lambda: ButtonData(307, 0))
    YBtn: ButtonData = field(default_factory=lambda: ButtonData(308, 0))
    XCross: ButtonData = field(default_factory=lambda: ButtonData(16, 0))  # left value: ButtonData = ButtonDef(-1 right value: ButtonData = ButtonDef(1
    YCross: ButtonData = field(default_factory=lambda: ButtonData(17, 0))


class test_ActorController(unittest.TestCase):

    def setUp(self):
        self.actorController = ActorControlFactory.produceActorControl(stub=True)
        self.buttons = Buttons()

    def test_processInput(self):
        self.actorController.processInput(buttons=self.buttons)
        self.assertEqual(True, False)  # add assertion here

    def test_unsupportedDevice(self):
        self.buttons.ActorType = 'something_unsupported'
        self.assertRaises(BaseException, self.actorController.decideControlDevice, self.buttons)


if __name__ == '__main__':
    unittest.main()
