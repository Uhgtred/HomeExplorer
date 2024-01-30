#!/usr/bin/env python3
# @author: Markus Kösters

from abc import ABC, abstractmethod


class VideoFilterInterface(ABC):

    @abstractmethod
    @staticmethod
    def filter(image, *filterArgs: list) -> any:
        """
        Interface for Method that filter video data.
        :param image: Image-object.
        :param filterArgs: Arguments passed to the filter method.
        """
        pass
