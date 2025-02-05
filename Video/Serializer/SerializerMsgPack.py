#!/usr/bin/env python3
# @author: Markus Kösters
import cv2
import msgpack
import numpy

from Video.Serializer import SerializerInterface


class SerializerMsgPack(SerializerInterface):

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
            print('[Warning]: SerializerMsgPack does not support file-paths.')
        encoding_parameters = [int(cv2.IMWRITE_JPEG_QUALITY), 80] # 80 is the quality of the jpeg compression
        returnValue, buffer = cv2.imencode('.jpg', imageData, encoding_parameters) # returnValue is type boolean.
        serializedData: bytes = msgpack.packb({'frameData': buffer.tobytes()})
        return serializedData

    def deserialize(self, data: bytes) -> any:
        payload = msgpack.unpackb(data)
        frameData = payload.get(b'frameData')  # Access the frame
        frameData = numpy.frombuffer(frameData, dtype=numpy.uint8) # or numpy.ndarray?
        # Todo: i have no idea what cv2.imdecode is returning. The documentations are really bad for opencv.
        imageframe = cv2.imdecode(frameData, cv2.IMREAD_COLOR)
        return imageframe
