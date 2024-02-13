#!/usr/bin/env python3
# @author: Markus Kösters

from dataclasses import dataclass

import cv2


@dataclass(frozen=True)
class VideoCameraConfig:
    """
    VideoCamera configuration.
    """
    FPS: int
    Port: int
    Resolution: tuple[int, int]
    camera: cv2.VideoCapture = cv2.VideoCapture
