#!/usr/bin/env python3
# Standalone tests for VideoController and VideoControllerBuilder

import unittest
import numpy
from unittest.mock import MagicMock

# Mock interfaces
class MockVideoCameraInterface:
    def readCameraInLoop(self, frameCallback):
        self.frame_callback = frameCallback

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
    def __init__(self):
        self.transmitted_data = []

    def transmit(self, data):
        self.transmitted_data.append(data)

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

# Tests for VideoController
class TestVideoController(unittest.TestCase):
    def setUp(self):
        self.controller = VideoController()
        self.camera = MockVideoCameraInterface()
        self.filter = MockVideoFilterInterface()
        self.serializer = MockSerializerInterface()
        self.compressor = MockCompressorInterface()
        self.transmitter = MockVideoTransmitterInterface()

        # Set up the controller with mock components
        self.controller.setCamera(self.camera)
        self.controller.setFiltering(self.filter)
        self.controller.setSerialization(self.serializer)
        self.controller.setCompression(self.compressor)
        self.controller.setTransmission(self.transmitter)

    def test_init(self):
        """Test that the controller initializes correctly"""
        controller = VideoController()
        self.assertFalse(controller.isRunning)

    def test_setCamera(self):
        """Test setting the camera"""
        controller = VideoController()
        camera = MockVideoCameraInterface()
        controller.setCamera(camera)
        # We can't directly test private attributes, but we can test behavior
        # that depends on them being set correctly
        controller.start()
        self.assertTrue(controller.isRunning)
        # Verify that readCameraInLoop was called
        self.assertIsNotNone(camera.frame_callback)

    def test_setFiltering(self):
        """Test setting the filtering"""
        controller = VideoController()
        filter = MockVideoFilterInterface()
        # This should log a warning but not raise an exception
        controller.setFiltering(filter)

    def test_setSerialization(self):
        """Test setting the serialization"""
        controller = VideoController()
        serializer = MockSerializerInterface()
        controller.setSerialization(serializer)

    def test_setCompression(self):
        """Test setting the compression"""
        controller = VideoController()
        compressor = MockCompressorInterface()
        controller.setCompression(compressor)

    def test_setTransmission(self):
        """Test setting the transmission"""
        controller = VideoController()
        transmitter = MockVideoTransmitterInterface()
        controller.setTransmission(transmitter)

    def test_start_without_camera(self):
        """Test starting without a camera"""
        controller = VideoController()
        with self.assertRaises(Exception):
            controller.start()

    def test_start_with_camera(self):
        """Test starting with a camera"""
        self.controller.start()
        self.assertTrue(self.controller.isRunning)
        # Verify that readCameraInLoop was called
        self.assertIsNotNone(self.camera.frame_callback)

    def test_stop(self):
        """Test stopping the controller"""
        self.controller.start()
        self.assertTrue(self.controller.isRunning)
        self.controller.stop()
        self.assertFalse(self.controller.isRunning)

    def test_process_frame(self):
        """Test processing a frame"""
        # Start the controller to set up the frame callback
        self.controller.start()

        # Create a test frame
        test_frame = numpy.zeros((10, 10, 3), dtype=numpy.uint8)

        # Simulate a frame being captured
        self.camera.frame_callback(test_frame)

        # Verify that the transmitter received data
        self.assertEqual(len(self.transmitter.transmitted_data), 1)

    def test_process_none_frame(self):
        """Test processing a None frame"""
        # Start the controller to set up the frame callback
        self.controller.start()

        # Simulate a None frame being captured
        self.camera.frame_callback(None)

        # Verify that the transmitter did not receive data
        self.assertEqual(len(self.transmitter.transmitted_data), 0)

    def test_transmit_without_transmitter(self):
        """Test transmitting without a transmitter"""
        controller = VideoController()
        controller.setCamera(self.camera)

        # Start the controller to set up the frame callback
        controller.start()

        # Create a test frame
        test_frame = numpy.zeros((10, 10, 3), dtype=numpy.uint8)

        # Simulate a frame being captured - this should raise an exception
        with self.assertRaises(Exception):
            self.camera.frame_callback(test_frame)

    def test_filter_without_filter(self):
        """Test filtering without a filter"""
        # Remove the filter
        self.controller = VideoController()
        self.controller.setCamera(self.camera)
        self.controller.setTransmission(self.transmitter)

        # Start the controller to set up the frame callback
        self.controller.start()

        # Create a test frame
        test_frame = numpy.zeros((10, 10, 3), dtype=numpy.uint8)

        # Simulate a frame being captured
        self.camera.frame_callback(test_frame)

        # Verify that the transmitter received data
        self.assertEqual(len(self.transmitter.transmitted_data), 1)

    def test_compress_without_compressor(self):
        """Test compressing without a compressor"""
        # Remove the compressor
        self.controller = VideoController()
        self.controller.setCamera(self.camera)
        self.controller.setSerialization(self.serializer)
        self.controller.setTransmission(self.transmitter)

        # Start the controller to set up the frame callback
        self.controller.start()

        # Create a test frame
        test_frame = numpy.zeros((10, 10, 3), dtype=numpy.uint8)

        # Simulate a frame being captured
        self.camera.frame_callback(test_frame)

        # Verify that the transmitter received data
        self.assertEqual(len(self.transmitter.transmitted_data), 1)

    def test_serialize_without_serializer(self):
        """Test serializing without a serializer"""
        # Remove the serializer
        self.controller = VideoController()
        self.controller.setCamera(self.camera)
        self.controller.setTransmission(self.transmitter)

        # Start the controller to set up the frame callback
        self.controller.start()

        # Create a test frame
        test_frame = numpy.zeros((10, 10, 3), dtype=numpy.uint8)

        # Simulate a frame being captured
        self.camera.frame_callback(test_frame)

        # Verify that the transmitter received data
        self.assertEqual(len(self.transmitter.transmitted_data), 1)

# Tests for VideoControllerBuilder
class TestVideoControllerBuilder(unittest.TestCase):
    def setUp(self):
        self.builder = VideoControllerBuilder()
        self.camera = MockVideoCameraInterface()
        self.filter = MockVideoFilterInterface()
        self.serializer = MockSerializerInterface()
        self.compressor = MockCompressorInterface()
        self.transmitter = MockVideoTransmitterInterface()

    def test_init(self):
        """Test that the builder initializes correctly"""
        builder = VideoControllerBuilder()
        self.assertIsInstance(builder.videoController, VideoController)

    def test_addCamera(self):
        """Test adding a camera"""
        result = self.builder.addCamera(self.camera)
        # Method should return self for chaining
        self.assertEqual(result, self.builder)

    def test_addFiltering(self):
        """Test adding filtering"""
        result = self.builder.addFiltering(self.filter)
        # Method should return self for chaining
        self.assertEqual(result, self.builder)

    def test_addSerialization(self):
        """Test adding serialization"""
        result = self.builder.addSerialization(self.serializer)
        # Method should return self for chaining
        self.assertEqual(result, self.builder)

    def test_addCompression(self):
        """Test adding compression"""
        result = self.builder.addCompression(self.compressor)
        # Method should return self for chaining
        self.assertEqual(result, self.builder)

    def test_addTransmission(self):
        """Test adding transmission"""
        result = self.builder.addTransmission(self.transmitter)
        # Method should return self for chaining
        self.assertEqual(result, self.builder)

    def test_build(self):
        """Test building the controller"""
        # Add all components
        self.builder.addCamera(self.camera)
        self.builder.addFiltering(self.filter)
        self.builder.addSerialization(self.serializer)
        self.builder.addCompression(self.compressor)
        self.builder.addTransmission(self.transmitter)

        # Build the controller
        controller = self.builder.build()

        # Verify that the controller is returned
        self.assertIsInstance(controller, VideoController)

    def test_method_chaining(self):
        """Test method chaining"""
        # Chain all methods
        controller = self.builder \
            .addCamera(self.camera) \
            .addFiltering(self.filter) \
            .addSerialization(self.serializer) \
            .addCompression(self.compressor) \
            .addTransmission(self.transmitter) \
            .build()

        # Verify that the controller is returned
        self.assertIsInstance(controller, VideoController)

        # Start the controller to verify that all components were set
        controller.start()
        self.assertTrue(controller.isRunning)

        # Create a test frame
        test_frame = numpy.zeros((10, 10, 3), dtype=numpy.uint8)

        # Simulate a frame being captured
        self.camera.frame_callback(test_frame)

        # Verify that the transmitter received data
        self.assertEqual(len(self.transmitter.transmitted_data), 1)

if __name__ == '__main__':
    unittest.main()
