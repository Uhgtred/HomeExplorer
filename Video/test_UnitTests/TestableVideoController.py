#!/usr/bin/env python3
# Simplified version of VideoController for testing

import numpy
from unittest.mock import MagicMock

# Mock interfaces
class MockVideoCameraInterface:
    def readCameraInLoop(self, frameCallback):
        pass
    
    def stopCamera(self):
        pass

class MockVideoFilterInterface:
    def filter(self, frame):
        return frame

class MockSerializerInterface:
    def serialize(self, data):
        return b'serialized_data'
    
    def deserialize(self, data):
        return numpy.zeros((10, 10, 3), dtype=numpy.uint8)

class MockCompressorInterface:
    def compress(self, data):
        return b'compressed_data'
    
    def decompress(self, data):
        return b'decompressed_data'

class MockVideoTransmitterInterface:
    def transmit(self, data):
        pass

# Simplified VideoController
class VideoController:
    """
    Simplified version of VideoController for testing
    """
    isRunning = False
    
    def __init__(self):
        self.__camera = None
        self.__filtering = None
        self.__serialization = None
        self.__compression = None
        self.__transmission = None
        self.__logger = MagicMock()
    
    def setCamera(self, camera):
        self.__camera = camera
    
    def setSerialization(self, serialization):
        self.__serialization = serialization
    
    def setFiltering(self, filtering):
        self.__filtering = filtering
        self.__logger.warning('Filtering has not been implemented yet!')
    
    def setCompression(self, compression):
        self.__compression = compression
    
    def setTransmission(self, transmission):
        self.__transmission = transmission
    
    def start(self):
        if not self.isRunning and self.__camera is not None:
            self.isRunning = True
            self.__camera.readCameraInLoop(self.__processFrame)
        elif self.__camera is None:
            exceptionMessage = "VideoCamera not initialized! Cannot start video stream!"
            self.__logger.exception(exceptionMessage)
            raise Exception(exceptionMessage)
    
    def stop(self):
        if self.isRunning:
            self.__camera.stopCamera()
            self.isRunning = False
    
    def __processFrame(self, imageFrame):
        if imageFrame is None:
            return
        filteredImage = self.__filter(imageFrame)
        self.__logger.debug(f'Filtered Image Frame of type {type(filteredImage)}')
        serializedImageData = self.__serialize(filteredImage)
        self.__logger.debug(f'Serialized Image Frame of type {type(serializedImageData)}')
        compressedImage = self.__compress(serializedImageData)
        self.__logger.debug(f'Compressed Image Frame of type {type(compressedImage)}')
        self.__transmit(compressedImage)
    
    def __filter(self, imageFrame):
        if self.__filtering is not None:
            self.__logger.warning('Filtering not yet implemented!')
        return imageFrame
    
    def __compress(self, imageFrame):
        return imageFrame if self.__compression is None else self.__compression.compress(imageFrame)
    
    def __serialize(self, imageFrame):
        self.__logger.debug(f'Serializing Image Frame of type {type(imageFrame)}')
        if self.__serialization is not None:
            return self.__serialization.serialize(imageFrame)
        return imageFrame
    
    def __transmit(self, frameData):
        if self.__transmission is not None:
            self.__transmission.transmit(frameData)
        else:
            exceptionMessage = 'Unable to transmit Image Frame. No transmission object set.'
            self.__logger.exception(exceptionMessage)
            raise Exception(exceptionMessage)

# Simplified VideoControllerBuilder
class VideoControllerBuilder:
    def __init__(self):
        self.videoController = VideoController()
    
    def addCamera(self, camera):
        self.videoController.setCamera(camera)
        return self
    
    def addFiltering(self, filtering):
        self.videoController.setFiltering(filtering)
        return self
    
    def addSerialization(self, serialization):
        self.videoController.setSerialization(serialization)
        return self
    
    def addCompression(self, compression):
        self.videoController.setCompression(compression)
        return self
    
    def addTransmission(self, transmission):
        self.videoController.setTransmission(transmission)
        return self
    
    def build(self):
        return self.videoController