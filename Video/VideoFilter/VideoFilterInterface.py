#!/usr/bin/env python3
# @author: Markus Kösters

from typing import Protocol


class VideoFilterInterface(Protocol):

    @staticmethod
    def filterFrame(image, *filterArgs: list) -> any:
        """
        Interface for Method that filter video data.
        :param image: Image-object.
        :param filterArgs: Arguments passed to the filter method.
        """
        pass
