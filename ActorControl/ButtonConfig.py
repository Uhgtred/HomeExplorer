#!/usr/bin/env python3
# @author: Markus Kösters
from dataclasses import dataclass, field


@dataclass
class ButtonConfig:
    xBox: dict[str, str] = field(default_factory=lambda: ({
        '2': 'LeftMotor',
        '5': 'RightMotor',
        '3': 'CameraXServo',
        '4': 'CameraYServo'
    }))