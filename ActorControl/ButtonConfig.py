#!/usr/bin/env python3
# @author: Markus Kösters

from dataclasses import dataclass, field

from ActorControl import Motors


@dataclass
class ButtonData:
    # Defining the attributes of a single button.
    ID: int
    value: int


@dataclass
class ButtonConfig:
    ActorType: str
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
