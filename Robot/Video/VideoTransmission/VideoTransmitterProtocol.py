#!/usr/bin/env python3
# @author: Markus Kösters

from typing import Protocol

from .SerializerInterface import SerializerInterface


class VideoTransmitterProtocol(Protocol):

    def serialize(self, serializer: SerializerInterface.serialize):
        """
        Protocol for the image tranmission to make sure the data is serialized before sending.
        :param serializer: Serializer instance.
        """
        raise NotImplementedError
