#!/usr/bin/env python3
# @author: Markus Kösters

from Robot.BusTransactions.BusFactory import BusFactory
from Robot.Video.VideoTransmission.SerializationNumpySave import SerializationNumpySave
from Robot.Video.VideoTransmission.VideoTransmitter import VideoTransmitter


class VideoTransmitterFactory:

    @staticmethod
    def produceDefaultVideoTransmitter() -> VideoTransmitter:
        """
        Factory method for producing an instance of a default video-transmission object.
        :return: Video-transmission instance-object.
        """
        bus = BusFactory.produceUDP_Transceiver()
        serializer = SerializationNumpySave()
        return VideoTransmitter(serializer, bus)
