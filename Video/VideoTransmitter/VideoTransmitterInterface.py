#!/usr/bin/env python3
# @author: Markus Kösters

from abc import abstractmethod, ABC


class VideoTransmitterInterface(ABC):

    @abstractmethod
    def transmit(self, imageData: bytes) -> None:
        """
        Interface-Method for transmitting an image-file to a client.
        :param imageData: Filepath of the image-file that will be transmitted.
        """
