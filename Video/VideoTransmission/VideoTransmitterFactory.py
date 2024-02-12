#!/usr/bin/env python3
# @author: Markus Kösters

from BusTransactions.BusFactory import BusFactory
from Video.VideoTransmission.VideoTransmitter import VideoTransmitter


class VideoTransmitterFactory:

    @staticmethod
    def produceDefaultVideoTransmitter() -> VideoTransmitter:
        """
        Factory method for producing an instance of a default video-transmission object.
        :return: Video-transmission instance-object.
        """
        bus = BusFactory.produceUDP_Transceiver()
        return VideoTransmitter(bus)
