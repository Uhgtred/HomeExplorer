#!/usr/bin/env python3
# @author: Markus Kösters

from .BusPlugins import BusPluginInterface
from .Encoding.BusEncodings import EncodingProtocol


class Bus:
    """
    Class for communication with a variety of bus-systems.
    """

    def __init__(self, bus: BusPluginInterface, encoding: EncodingProtocol):
        """
        :param bus: Bus that shall be communicated with. Needs to follow the protocol Bus.
        :param encoding: Encoding that will be used to make the messages compliant to the bus.
        """
        self.__stopFlag: bool = False
        self.encoding = encoding
        self.bus = bus

    def readSingleMessage(self) -> EncodingProtocol.decode:
        """
        Read and decode a single message from the bus.
        :return: Decoded message in string format.
        """
        return self.encoding.decode(self.bus.readBus())

    def readBusUntilStopFlag(self, callbackMethod: callable, stopFlag: bool = False) -> None:
        """
        Reads and decodes messages from a bus in a loop until stopFlag is True.
        :param callbackMethod: Method that the received messages shall be sent to.
                                Needs to accept one argument which is the message read from the bus.
        :param stopFlag: When true reading-loop stops.
        """
        while not stopFlag:
            callbackMethod(self.readSingleMessage())

    def writeSingleMessage(self, message: any) -> None:
        """
        Sending an encoded message to the bus.
        :param message: Message that will be sent to the bus.
        """
        encodedMessage = self.encoding.encode(message)
        self.bus.writeBus(encodedMessage)

    @property
    def stopFlag(self) -> bool:
        """
        Getter-Method for the stop-flag.
        :return: Stop-flag.
        """
        return self.__stopFlag

    @stopFlag.setter
    def stopFlag(self, state: bool) -> None:
        """
        Setter-method for the stop-flag.
        :param state: Stop-flag state that will be set.
        """
        self.__stopFlag = state
