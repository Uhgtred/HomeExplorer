#!/usr/bin/env python3
# @author: Markus Kösters

from Video.Serializer.SerializerMsgPack import SerializerMsgPack


class SerializerFactory:

    @staticmethod
    def produceSerializationMsgPack():
        """ Produces a Serializer MsgPack"""
        return SerializerMsgPack()
