#!/usr/bin/env python3
# @author: Markus Kösters

import unittest

from BusTransactions import SerialBusConfig, BusPluginInterface
from BusTransactions import SerialBus
from BusTransactions.BusPlugins.SerialBusPlugin.test_UnitTests.SerialBusMock import MockSerialBus
from BusTransactions import Encoding
from BusTransactions.BusFactory import BusFactory


class MyTestCase(unittest.TestCase):

    busFactory = BusFactory()
    mockLibrary = MockSerialBus

    def test_produceBusTransceiver(self):
        config = SerialBusConfig('test', 123, self.mockLibrary)
        encoding = Encoding.EncodingFactory.arduinoSerialEncoding
        bus = SerialBus(config)
        transceiver = self.busFactory.produceBusTransceiver(bus, encoding)
        print(transceiver)
        assert isinstance(transceiver, BusPluginInterface)


if __name__ == '__main__':
    unittest.main()
