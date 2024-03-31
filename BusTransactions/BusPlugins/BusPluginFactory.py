#!/usr/bin/env python3
# @author: Markus Kösters

from .EthernetBusPlugin import Tcp_Udp_sockets, SocketConfigs
from .EthernetBusPlugin.test_UnitTests import MockSocket
from .SerialBusPlugin import SerialBus, SerialBusConfig
from .SerialBusPlugin.test_UnitTests.SerialBusMock import MockSerialBus


class BusPluginFactory:
    """
    Class for producing Bus-instances.
    """

    @staticmethod
    def produceSerialBusPlugin(path: str, baudRate: int, stub: bool = False) -> SerialBus:
        """
        Method for creating an instance of a SerialBus.
        :return: SerialBus-instance.
        """
        if stub:
            config = SerialBusConfig(path, baudRate, MockSerialBus)
        else:
            config = SerialBusConfig(path, baudRate)
        return SerialBus(config)

    @staticmethod
    def produceUdpSocketPlugin(port: int, host: bool, ipAddress: str = '127.0.0.1', messageSize: int = 4096, stub: bool = False) -> Tcp_Udp_sockets.UdpSocket:
        """
        Method for creating an instance of an Udp-socket connection.
        :return: Socket-instance.
        """
        if stub:
            config = SocketConfigs.UdpSocketConfig(host=host, IPAddress=ipAddress, messageSize=messageSize, port=port, busLibrary=MockSocket)
        else:
            config = SocketConfigs.UdpSocketConfig(IPAddress=ipAddress, messageSize=messageSize, port=port, host=host)
        return Tcp_Udp_sockets.UdpSocket(config)
