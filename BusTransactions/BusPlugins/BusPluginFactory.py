#!/usr/bin/env python3
# @author: Markus Kösters

from .Ethernet import Tcp_Udp_sockets, SocketConfigs
from .SerialBusModule import SerialBus, SerialBusConfig
from .BusPluginInterface import BusPluginInterface


class BusPluginFactory:
    """
    Class for producing Bus-instances.
    """

    @staticmethod
    def produceSerialBusArduinoPlugin() -> BusPluginInterface:
        """
        Method for creating an instance of a SerialBus.
        :return: SerialBus-instance.
        """
        config = SerialBusConfig('/dev/ttyACM0', 115200)
        return SerialBus(config)

    @staticmethod
    def produceUdpSocketPlugin(ipAddress='127.0.0.1', messageSize=4096) -> BusPluginInterface:
        """
        Method for creating an instance of a Udp-socket connection.
        :return: Socket-instance.
        """
        config = SocketConfigs.UdpSocketConfig(IPAddress=ipAddress, messageSize=messageSize)
        return Tcp_Udp_sockets.UdpSocket(config)
