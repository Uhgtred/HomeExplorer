#!/usr/bin/env python3
# @author: Markus Kösters

from .Bus import Bus
from .BusPlugins import BusPluginInterface
from .BusPlugins import BusPluginFactory
from .Encoding import EncodingFactory
from .Encoding.BusEncodings import EncodingProtocol


class BusFactory:
    """
    Factory for creating an instance of a bus-transceiver.
    """

    @staticmethod
    def produceBusTransceiver(bus: type(BusPluginFactory), encoding: type(EncodingFactory)) -> Bus:
        """
        Method for producing an instance of a bus-transceiver.
        :param bus: Bus-Class that will be communicated with, produced by Factory-class in BusPlugins-Module.
        :param encoding: Encoding that decides the format of the messages.
        """
        # check if encoding has already been instanced
        if callable(encoding):
            encoding: EncodingProtocol = encoding()
        transceiver = Bus(bus, encoding)
        return transceiver

    @staticmethod
    def produceSerialTransceiver(path: str = '/dev/ttyACM0', baudRate: int = 115200, stub: bool = False) -> Bus:
        """
        Method for creating an instance of a serial-bus transceiver that connects to arduino.
        """
        encoding: EncodingProtocol = EncodingFactory.arduinoSerialEncoding()
        busPlugin: BusPluginInterface = BusPluginFactory.produceSerialBusPlugin(path, baudRate, stub=stub)
        return Bus(busPlugin, encoding)

    @staticmethod
    def produceUDP_Transceiver(port: int, host: bool, pickle: bool = True, stub: bool = False, noEncoding: bool = False) -> Bus:
        """
        Method for creating an instance of an udp-socket.
        :return: Bus-object.
        Todo: don't use pickle anymore, it is not safe to use.
        Todo: integrate noEncoding if needed.
        """
        if noEncoding:
            busPlugin: BusPluginInterface = BusPluginFactory.produceUdpSocketPlugin(host=host, port=port, stub=stub)
            return Bus(busPlugin)
        encoding: EncodingProtocol = EncodingFactory.socketEncoding(pickle)
        busPlugin: BusPluginInterface = BusPluginFactory.produceUdpSocketPlugin(host=host, port=port, stub=stub)
        return Bus(busPlugin, encoding)
