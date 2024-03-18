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
        if stub:
            bus = BusFactory.produceUDP_Transceiver(host=True, port=port, stub=True)
        else:
            bus = BusFactory.produceUDP_Transceiver(host=True, port=port)
        return VideoTransmitter(bus)
