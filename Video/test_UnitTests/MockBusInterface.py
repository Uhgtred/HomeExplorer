#!/usr/bin/env python3
# Mock for BusTransactions modules

import sys
import logging
from unittest.mock import MagicMock

# Create a mock BusInterface class
class BusInterface:
    def __init__(self):
        self.writeSingleMessage = MagicMock()

    def writeSingleMessage(self, data):
        pass

# Create a mock Bus class
class Bus:
    def __init__(self):
        self.writeSingleMessage = MagicMock()

    def writeSingleMessage(self, data):
        pass

# Create a mock BusFactory class with the methods used in VideoTransmitterFactory
class BusFactoryMock:
    @staticmethod
    def produceUDP_ImageDataTransceiver(port):
        return Bus()

    @staticmethod
    def produceUDP_ImageDataTransceiverWithStub(port):
        return Bus()

    @staticmethod
    def produceUDP_TransceiverNoEncoding(port):
        return Bus()

# Create a mock module for BusTransactions.BusInterface
sys.modules['BusTransactions.BusInterface'] = MagicMock()
sys.modules['BusTransactions.BusInterface'].BusInterface = BusInterface

# Mock the BusFactory module
sys.modules['BusTransactions.BusFactory'] = MagicMock()
sys.modules['BusTransactions.BusFactory'].BusFactory = BusFactoryMock

# Mock the Bus module
sys.modules['BusTransactions.Bus'] = MagicMock()
sys.modules['BusTransactions.Bus'].Bus = Bus

# Mock the BusTransactions module itself
sys.modules['BusTransactions'] = MagicMock()
sys.modules['BusTransactions'].Bus = Bus

# Mock the logging module for VideoTransmitter
sys.modules['P'] = MagicMock()
