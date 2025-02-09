#!/usr/bin/env python3
# @author: Markus Kösters

from abc import ABC, abstractmethod


class CompressorInterface(ABC):

    @staticmethod
    @abstractmethod
    def compress(data: any) -> any:
        """
        Interface for compressing image-data before sending it.
        :param data: Image-data that is to be compressed.
        :return: Compressed image-data.
        """

    @staticmethod
    @abstractmethod
    def decompress(compressedData: any) -> bytes:
        """
        Interface for compressing image-data before sending it.
        :param compressedData: Compressed image-data that is to be decompressed.
        :return: Decompressed image-data.
        """