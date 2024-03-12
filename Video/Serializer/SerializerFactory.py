#!/usr/bin/env python3
# @author: Markus Kösters

from Video.Serializer import SerializerJoblib
from Video.Serializer.SerializerConfig import SerializerConfig


class SerializerFactory:

    @staticmethod
    def produceSerializationJoblib():
        """ Produces a Serializer Joblib"""
        file = './tmpVideoData/imageFile.pkl'
        config = SerializerConfig(file)
        return SerializerJoblib(config)
