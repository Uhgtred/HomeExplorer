#!/usr/bin/env python3
# @author Markus Kösters

import unittest

from BusTransactions import BusPluginFactory
from ..SerialBusConfig import SerialBusConfig
from ..SerialBus import SerialBus
from .SerialBusMock import MockSerialBus


class test_SerialBus(unittest.TestCase):

    def setUp(self) -> None:
        self.testString = b'Hello World'
        self.path = 'test'
        self.baudRate = 115200

    def test_write(self):
        bus = BusPluginFactory.produceSerialBusPlugin(self.path, self.baudRate, stub=True)
        bus.writeBus(self.testString)
        message = bus.bus.buffer.pop(0)
        self.assertEqual(message, self.testString)

    def test_read(self):
        bus = BusPluginFactory.produceSerialBusPlugin(self.path, self.baudRate, stub=True)
        bus.writeBus(self.testString)
        message = bus.readBus()
        self.assertEqual(message, self.testString)


if __name__ == '__main__':
    unittest.main()
