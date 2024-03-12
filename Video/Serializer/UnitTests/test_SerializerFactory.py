#!/usr/bin/env python3
import unittest
from Video.Serializer.SerializerFactory import SerializerFactory
from Video.Serializer import SerializerJoblib


class TestSerializerFactory(unittest.TestCase):

    def test_produce_serialization_joblib(self):
        serializer_joblib = SerializerFactory.produceSerializationJoblib()
        self.assertIsInstance(serializer_joblib, SerializerJoblib)


if __name__ == '__main__':
    unittest.main()

