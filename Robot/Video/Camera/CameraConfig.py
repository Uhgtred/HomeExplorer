#!/usr/bin/env python3
# @author: Markus Kösters

from dataclasses import dataclass


@dataclass(frozen=True)
class CameraConfig:
    """
    Camera configuration.
    """
    FPS: int
    Port: int
    Resolution: list[int, int]
