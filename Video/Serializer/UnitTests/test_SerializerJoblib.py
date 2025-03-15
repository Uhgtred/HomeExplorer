#!/usr/bin/env python3

import unittest

import numpy
import os

from Video.Serializer.SerializerMsgPack import SerializerMsgPack

class TestSerializerJoblib(unittest.TestCase):

    def setUp(self):
        self.serializer = SerializerMsgPack()
        self.data: numpy.ndarray = numpy.random.randint(0, 256, (100, 100, 3), dtype=numpy.uint8)


    def test_serialize(self):
        """
        Tests the serialization method to ensure it outputs data in byte format.

        This test checks if the `serialize` method of the `self.serializer`
        correctly converts the input `self.data` into a serialized byte object.

        :raises AssertionError: If the `serializedData` is not an
            instance of `bytes`.
        """
        serializedData: bytes = self.serializer.serialize(self.data)
        self.assertIsInstance(serializedData, bytes)

    def test_deserialize(self):
        """
        Tests the deserialization process of the data after it has been serialized. The
        test ensures that the serialized data can be successfully converted back to the
        expected data format and type. It verifies that the deserialized result is of
        type `numpy.ndarray`.

        :param serializedData: The serialized form of the test data.
        :type serializedData: bytes
        :param deserialized_data: The deserialized output data.
        :type deserialized_data: numpy.array

        :return: None
        """
        serializedData: bytes = self.serializer.serialize(self.data)
        deserialized_data: numpy.array = self.serializer.deserialize(serializedData)
        self.assertIsInstance(deserialized_data, numpy.ndarray)



if __name__ == '__main__':
    unittest.main()