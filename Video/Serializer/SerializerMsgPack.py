#!/usr/bin/env python3
# @author: Markus Kösters

import logging

import cv2
import msgpack
import numpy

from ProjectLogging import Logger
from Video.Serializer import SerializerInterface


class SerializerMsgPack(SerializerInterface):

    def __init__(self):
        self.__logger: logging.Logger = logging.getLogger(__name__)

    def serialize(self, imageData: numpy.ndarray = None, filePath: str = '') -> bytes:
        """
        Serialize raw image data into a compressed byte format.

        This function takes a NumPy ndarray representing image data, compresses it
        using JPEG encoding, and serializes it into a compact byte format using msgpack.
        The result includes the compressed image data in encoded byte array format,
        suitable for network transmission or storage.

        :param imageData: A NumPy ndarray containing raw image data to be serialized.
        :type imageData: numpy.ndarray
        :param filePath: A file path to an image file to be serialized (not valid for this implementation).
        :type filePath: str
        :return: A serialized byte object containing the compressed image data in
            msgpack format.
        :rtype: bytes
        """
        # This makes the code use the abstract method at the beginning, which includes a little bit of error-handling.
        super().serialize(imageData)
        if filePath:
            self.__logger.warning('SerializerMsgPack does not support file-paths.')
        self.__logger.debug(f'Serializing image data of type {type(imageData)} ...')
        encodingParameters = [int(cv2.IMWRITE_JPEG_QUALITY), 80] # 80 is the quality of the jpeg compression
        returnValue, buffer = cv2.imencode('.jpg', imageData, encodingParameters) # returnValue is type boolean.
        serializedData: bytes = msgpack.packb({'frameData': buffer.tobytes()})
        return serializedData

    def deserialize(self, data: bytes) -> any:
        """
        Deserializes a given byte array into an image frame object.

        This method takes a serialized byte array in the MessagePack format,
        extracts the frame data, decodes it into an image format using OpenCV,
        and returns the corresponding image frame.

        :param data: A byte array representing the serialized payload in
                     MessagePack format.
        :type data: bytes
        :return: Decoded image frame extracted from the serialized data.
        :rtype: any
        # Todo: Check if this code could be more modular (i am serializing and decoding image-data, which makes it only usable for image-data).
                If i split the code into two functions, it would be more modular and could potentially also be used for other data types.
        """
        payload: dict = msgpack.unpackb(data)
        frameData: numpy.ndarray = payload.get('frameData')  # Access the frame-data
        frameData: numpy.ndarray = numpy.frombuffer(frameData, dtype=numpy.uint8)
        imageframe = cv2.imdecode(frameData, cv2.IMREAD_COLOR)
        return imageframe
