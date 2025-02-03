#!/usr/bin/env python3
# @author: Markus Kösters
import os

from Video.Serializer import SerializerJoblib
from Video.Serializer.SerializerConfig import SerializerConfig
from Video.Serializer.SerializerMsgPack import SerializerMsgPack


class SerializerFactory:


    """
    This method is not compatible with the current state of the project.
    """
    # @staticmethod
    # def produceSerializationJoblib():
    #     """ Produces a Serializer Joblib"""
    #     print('Creating Filepath for Video Data...')
    #     filePath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../tmpVideoData'))
    #     os.makedirs(filePath, exist_ok=True)
    #     print(f'Filepath: {filePath} successfully created!')
    #     file = f'{filePath}/imageFile.pkl'
    #     file.strip('\x00')
    #     config = SerializerConfig(file)
    #     return SerializerJoblib(config)

    @staticmethod
    def produceSerializationMsgPack():
        """ Produces a Serializer MsgPack"""
        return SerializerMsgPack()
