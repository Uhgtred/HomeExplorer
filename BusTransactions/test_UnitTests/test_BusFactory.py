#!/usr/bin/env python3
# @author: Markus Kösters

import unittest

from BusTransactions import BusInterfaceFactory, BusInterface
from BusTransactions import SerialBusConfig
from BusTransactions import SerialBus
from BusTransactions.Buses.SerialBusModule.test_UnitTests.SerialBusMock import MockSerialBus
from BusTransactions import Encoding


class MyTestCase(unittest.TestCase):

    busFactory = BusInterfaceFactory()
    mockLibrary = MockSerialBus

    def test_produceBusTransceiver(self):
        config = SerialBusConfig('test', 123, self.mockLibrary)
        encoding = Encoding.EncodingFactory.arduinoSerialEncoding
        bus = SerialBus(config)
        transceiver = self.busFactory.produceBusTransceiver(bus, encoding)
        assert isinstance(transceiver, BusInterface)


if __name__ == '__main__':
    unittest.main()
