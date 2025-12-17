#!/usr/bin/env python3
# @author: Markus Kösters
from BusTransactions import Bus
from BusTransactions.BusFactory import BusFactory

from Video.VideoTransmitter import VideoTransmitterInterface
from Video.VideoTransmitter.VideoTransmitter import VideoTransmitter


class VideoTransmitterFactory:

    @staticmethod
    def produceDefaultVideoTransmitter(port: int) -> VideoTransmitterInterface:
        """
        Factory method for producing an instance of a default video-transmission object.
        :return: Video-transmission instance-object.
        """
        bus = BusFactory.produceUDP_ImageDataTransceiver(port=port)
        return VideoTransmitter(bus)

    @staticmethod
    def produceDefaultVideoTransmitterStub(port: int) -> VideoTransmitterInterface:
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
        bus = BusFactory.produceUDP_ImageDataTransceiverWithStub(port)
        return VideoTransmitter(bus)

    @staticmethod
    def produceVideoTransmitterNoEncoding(port: int) -> VideoTransmitterInterface:
        """
        Generates a VideoTransmitter instance configured with a UDP Transceiver that
        has no encoding.

        This static method creates a Bus instance using the UDP_TransceiverNoEncoding
        factory method on the provided port and associates it with a
        VideoTransmitter instance. It ensures compatibility with systems or
        applications that do not require encoding for video transmission.

        :param port: The port number to be used for the UDP Transceiver. Must be an
                     integer within the permissible port range.
        :type port: int
        :return: A VideoTransmitter configured with a UDP Transceiver with no encoding.
        :rtype: VideoTransmitter
        """
        bus: Bus = BusFactory.produceUDP_TransceiverNoEncoding(port=port)
        return VideoTransmitter(bus)
