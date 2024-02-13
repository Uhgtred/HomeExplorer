#!/usr/bin/env python3
# @author: Markus Kösters

from dataclasses import dataclass


@dataclass(frozen=True)
class VideoCameraConfig:
    """
    VideoCamera configuration.
    """
    FPS: int
    Port: int
    Resolution: tuple[int, int]
