#!/usr/bin/env python3
# Tests for VideoController

import unittest
import numpy
from unittest.mock import patch, MagicMock

# Use the simplified VideoController for testing
from Video.test_UnitTests.TestableVideoController import VideoController
from Video.test_UnitTests.MockObjects import (
    MockCamera, MockFilter, MockSerializer, MockCompressor, MockTransmitter
)


class TestVideoController(unittest.TestCase):
    def setUp(self):
        self.controller = VideoController()
        self.camera = MockCamera()
        self.filter = MockFilter()
        self.serializer = MockSerializer()
        self.compressor = MockCompressor()
        self.transmitter = MockTransmitter()

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
        camera = MockCamera()
        controller.setCamera(camera)
        # We can't directly test private attributes, but we can test behavior
        # that depends on them being set correctly
        controller.setTransmission(self.transmitter)
        with self.assertRaises(Exception):
            # This should raise an exception because we're missing other components
            controller.start()

    def test_setFiltering(self):
        """Test setting the filtering"""
        controller = VideoController()
        filter = MockFilter()
        # This should log a warning but not raise an exception
        controller.setFiltering(filter)

    def test_setSerialization(self):
        """Test setting the serialization"""
        controller = VideoController()
        serializer = MockSerializer()
        controller.setSerialization(serializer)

    def test_setCompression(self):
        """Test setting the compression"""
        controller = VideoController()
        compressor = MockCompressor()
        controller.setCompression(compressor)

    def test_setTransmission(self):
        """Test setting the transmission"""
        controller = VideoController()
        transmitter = MockTransmitter()
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
        self.camera.stopCamera.assert_called_once()

    def test_process_frame(self):
        """Test processing a frame"""
        # Start the controller to set up the frame callback
        self.controller.start()

        # Create a test frame
        test_frame = numpy.zeros((10, 10, 3), dtype=numpy.uint8)

        # Simulate a frame being captured
        self.camera.simulateFrame(test_frame)

        # Verify that the transmitter received data
        self.assertEqual(len(self.transmitter.transmitted_data), 1)

    def test_process_none_frame(self):
        """Test processing a None frame"""
        # Start the controller to set up the frame callback
        self.controller.start()

        # Simulate a None frame being captured
        self.camera.simulateFrame(None)

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
            self.camera.simulateFrame(test_frame)

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
        self.camera.simulateFrame(test_frame)

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
        self.camera.simulateFrame(test_frame)

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
        self.camera.simulateFrame(test_frame)

        # Verify that the transmitter received data
        self.assertEqual(len(self.transmitter.transmitted_data), 1)


if __name__ == '__main__':
    unittest.main()
