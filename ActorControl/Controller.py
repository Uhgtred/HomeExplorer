#!/usr/bin/env python3
# @author: Markus Kösters
from dataclasses import dataclass

from ActorControl.ActorControlInterface import Buttons


@dataclass
class Controller:
    # buttons that negate the value of another button.
    # key is the negating button and the value is a list containing the button that will be negated [0] and the state [1].
    negationButtons: dict[str:list]


class DefaultController:
    Controller(negationButtons={Buttons.LBtn.ID: [Buttons.LTrigger.ID, 0], Buttons.RBtn.ID: [Buttons.RTrigger.ID, 0]})
