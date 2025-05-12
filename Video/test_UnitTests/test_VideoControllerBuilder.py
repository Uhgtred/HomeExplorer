#!/usr/bin/env python3
# Tests for VideoControllerBuilder

import unittest
from unittest.mock import patch, MagicMock

# Use the simplified VideoControllerBuilder and VideoController for testing
from Video.test_UnitTests.TestableVideoController import VideoControllerBuilder, VideoController
from Video.test_UnitTests.MockObjects import (
    MockCamera, MockFilter, MockSerializer, MockCompressor, MockTransmitter
)


class TestVideoControllerBuilder(unittest.TestCase):
    def setUp(self):
        self.builder = VideoControllerBuilder()
        self.camera = MockCamera()
        self.filter = MockFilter()
        self.serializer = MockSerializer()
        self.compressor = MockCompressor()
        self.transmitter = MockTransmitter()

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
        import numpy
        test_frame = numpy.zeros((10, 10, 3), dtype=numpy.uint8)

        # Simulate a frame being captured
        self.camera.simulateFrame(test_frame)

        # Verify that the transmitter received data
        self.assertEqual(len(self.transmitter.transmitted_data), 1)


if __name__ == '__main__':
    unittest.main()
