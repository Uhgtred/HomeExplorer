#!/usr/bin/env python3
# @author: Markus Kösters

import zlib

from Video.Compressor.CompressorInterface import CompressorInterface


class CompressorZlib(CompressorInterface):

    @staticmethod
    def compress(data: any) -> any:
        """
        Method for compressing video-data before sending it to the remote-side.
        :param data: Image-data that is to be compressed.
        :return: Compressed image-data.
        """
        return zlib.compress(data)

    @staticmethod
    def decompress(compressedData: any) -> any:
        """
        Method for decompressing video-data after receiving it.
        :param compressedData: Compressed image-data that is to be decompressed.
        :return: Decompressed image-data.
        """
        return zlib.decompress(compressedData)