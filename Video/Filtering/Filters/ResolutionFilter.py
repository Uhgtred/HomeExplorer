#!/usr/bin/env python3
# @author: Markus Kösters

import cv2
import imutils


class ResolutionFilter:

    @staticmethod
    def filter(image: any, *filterArgs: list) -> any:
        """
        Filter method that rescales the image.
        :param image: Image that will be rescaled.
        :param filterArgs: X-axis and Y-axis resolution in a list.
        :return: Rescaled image.
        """
        x, y = filterArgs
        imutils.resize(image, width=x, height=y, inter=cv2.INTER_AREA)

