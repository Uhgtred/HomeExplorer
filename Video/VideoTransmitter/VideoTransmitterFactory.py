#!/usr/bin/env python3
# @author: Markus Kösters

from BusTransactions.BusFactory import BusFactory
from Video.VideoTransmitter.VideoTransmitter import VideoTransmitter


class VideoTransmitterFactory:

    @staticmethod
    def produceDefaultVideoTransmitter(port: int, stub: bool = False) -> VideoTransmitter:
        """
        Factory method for producing an instance of a default video-transmission object.
        :return: Video-transmission instance-object.
        """
        bus = BusFactory.produceUDP_ImageDataReceiver(port=port)
        return VideoTransmitter(bus)

    @staticmethod
    def produceDefaultVideoTransmitterStub(port: int) -> VideoTransmitter:
        """
        Produce a default VideoTransmitter stub configured with a UDP ImageDataReceiver.

        This method creates a `Bus` instance by utilizing the `BusFactory` to produce
        a UDP-based ImageDataReceiver stub for the given port. Subsequently, it
        instantiates and returns a `VideoTransmitter` object that operates on the
        created Bus.

        :param port: The port number used to initialize the UDP ImageDataReceiver
            stub.
        :type port: int
        :return: A configured VideoTransmitter instance.
        :rtype: VideoTransmitter
        """
        bus = BusFactory.produceUDP_ImageDataReceiverStub(port)
        return VideoTransmitter(bus)
