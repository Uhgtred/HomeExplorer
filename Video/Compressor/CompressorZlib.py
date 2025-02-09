#!/usr/bin/env python3
# @author: Markus Kösters

import zlib

from ProjectLogging import Logger
from Video.Compressor.CompressorInterface import CompressorInterface


class CompressorZlib(CompressorInterface):

    def __init__(self):
        self.__logger: Logger.getLogger = Logger('CompressorZlib', 'VideoCompressor').getLogger

    def compress(self, data: any) -> any:
        """
        Method for compressing video-data before sending it to the remote-side.
        :param data: Image-data that is to be compressed.
        :return: Compressed image-data.
        """
        self.__logger.debug(f'Datasize before compression: {len(data)}')
        compressedData = zlib.compress(data)
        self.__logger.debug(f'Datasize after compression: {len(compressedData)}')
        return compressedData

    def decompress(self, compressedData: any) -> any:
        """
        Method for decompressing video-data after receiving it.
        :param compressedData: Compressed image-data that is to be decompressed.
        :return: Decompressed image-data.
        """
        self.__logger.debug(f'Datasize before decompression: {len(compressedData)}')
        return zlib.decompress(compressedData)