#!/usr/bin/env python3
# @author: Markus Kösters

from Video.Serialization import SerializationJoblib
from Video.Serialization.SerializerConfig import SerializerConfig


class SerializerFactory:

    @staticmethod
    def produceSerializationJoblib():
        """ Produces a Serialization Joblib"""
        file = './tmp/imageFile.pkl'
        config = SerializerConfig(file)
        return SerializationJoblib(config)
