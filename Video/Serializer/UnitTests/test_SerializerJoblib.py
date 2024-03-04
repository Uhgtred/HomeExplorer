#!/usr/bin/env python3

import unittest
import numpy as np
import os

from Video.Serializer import SerializerJoblib


class SerializerConfig:
    def __init__(self, storage_file):
        self.storageFile = storage_file


class TestSerializerJoblib(unittest.TestCase):

    def setUp(self):
        self.config = SerializerConfig('temp.joblib')
        self.serializer = SerializerJoblib(self.config)
        self.data = np.array([1, 2, 3, 4, 5])

    def test_serialize(self):
        file_path = self.serializer.serialize(self.data)
        self.assertTrue(os.path.isfile(file_path))
        os.remove(file_path)

    def test_deserialize(self):
        self.serializer.serialize(self.data)
        deserialized_data = self.serializer.deserialize(self.config.storageFile)
        np.testing.assert_array_equal(deserialized_data, self.data)
        os.remove(self.config.storageFile)


if __name__ == '__main__':
    unittest.main()