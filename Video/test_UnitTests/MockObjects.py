#!/usr/bin/env python3
# Mock objects for testing VideoController

import numpy
from unittest.mock import MagicMock

from Video.Compressor.CompressorInterface import CompressorInterface
from Video.VideoCamera.VideoCameraInterface import VideoCameraInterface
from Video.VideoFilter.VideoFilterInterface import VideoFilterInterface
from Video.Serializer.SerializerInterface import SerializerInterface
from Video.VideoTransmitter.VideoTransmitterInterface import VideoTransmitterInterface


class MockCamera(VideoCameraInterface):
    def __init__(self):
        self.readCameraInLoop = MagicMock()
        self.stopCamera = MagicMock()
        self.frame_callback = None

    def readCameraInLoop(self, frameCallback):
        self.frame_callback = frameCallback
        
    def stopCamera(self):
        pass
        
    def simulateFrame(self, frame):
        """Helper method to simulate a frame being captured"""
        if self.frame_callback:
            self.frame_callback(frame)


class MockFilter(VideoFilterInterface):
    def __init__(self):
        self.filter = MagicMock(return_value=numpy.zeros((10, 10, 3), dtype=numpy.uint8))
        
    def filter(self, frame):
        return frame


class MockSerializer(SerializerInterface):
    def __init__(self):
        self.serialize = MagicMock(return_value=b'serialized_data')
        
    def serialize(self, data):
        return b'serialized_data'
        
    def deserialize(self, data):
        return numpy.zeros((10, 10, 3), dtype=numpy.uint8)


class MockCompressor(CompressorInterface):
    def __init__(self):
        self.compress = MagicMock(return_value=b'compressed_data')
        
    def compress(self, data):
        return b'compressed_data'
        
    def decompress(self, data):
        return b'decompressed_data'


class MockTransmitter(VideoTransmitterInterface):
    def __init__(self):
        self.transmit = MagicMock()
        self.transmitted_data = []
        
    def transmit(self, data):
        self.transmitted_data.append(data)