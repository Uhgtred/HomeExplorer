#!/usr/bin/env python3
# @author: Markus Kösters
import inspect
import pickle
import unittest

from BusTransactions import EncodingFactory


class test_BusEncodings(unittest.TestCase):

    encoding = EncodingFactory
    testString = "Hello World"

    def test_SocketDecodeEncode(self):
        """
        Testing any decodings in Encodinginterface, that follow the protocol:
        EncodingProtocol
        """
        message = self.encoding.socketEncoding().encode(self.testString)
        self.assertEqual(message, pickle.dumps(self.testString))
        message = self.encoding.socketEncoding().decode(message)
        self.assertEqual(message, self.testString)

    def test_ArduinoDecodeEncode(self):
        """
        Testing any encodings in Encodinginterface, that follow the protocol:
        EncodingProtocol
        """
        message = self.encoding.arduinoSerialEncoding().encode(self.testString)
        self.assertEqual(message, f'{self.testString}&'.encode())
        message = self.encoding.arduinoSerialEncoding().decode(message)
        self.assertEqual(message, self.testString)


if __name__ == '__main__':
    unittest.main()
