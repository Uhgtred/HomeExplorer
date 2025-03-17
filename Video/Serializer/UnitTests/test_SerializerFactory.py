#!/usr/bin/env python3
import unittest

from Video.Serializer.SerializerFactory import SerializerFactory
from Video.Serializer.SerializerMsgPack import SerializerMsgPack


class TestSerializerFactory(unittest.TestCase):

    def test_produceSerializerMsgPack(self):
        serializerMsgPack = SerializerFactory.produceSerializationMsgPack()
        self.assertIsInstance(serializerMsgPack, SerializerMsgPack)

if __name__ == '__main__':
    unittest.main()

