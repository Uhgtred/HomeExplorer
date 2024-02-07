#!/usr/bin/env python3
# @author: Markus Kösters
import time
import unittest

from BusTransactions import BusInterfaceFactory, SerialBus, SerialBusConfig
from BusTransactions.Buses.SerialBusModule.test_UnitTests.SerialBusMock import MockSerialBus
from BusTransactions import Encoding


class MyTestCase(unittest.TestCase):
    transceiver = BusInterfaceFactory()
    config = SerialBusConfig('test', 123, MockSerialBus)
    bus = SerialBus(config)
    transceiver = transceiver.produceBusTransceiver(bus, Encoding.EncodingFactory.arduinoSerialEncoding)
    testString = 'Test from BusTransceiver'
    messages = []

    def test_BusTransceiver_writeSingleMessage(self):
        self.transceiver.writeSingleMessage(self.testString)
        message = self.transceiver.bus.bus.buffer.pop(0)
        self.assertEqual(message[:-1], self.testString.encode())

    def test_BusTransceiver_readSingleMessage(self):
        self.transceiver.writeSingleMessage(self.testString)
        message = self.transceiver.readSingleMessage()
        self.assertEqual(message, self.testString)


if __name__ == '__main__':
    unittest.main()
