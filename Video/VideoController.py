#!/usr/bin/env python3
# @author: Markus Kösters
from logging import exception

import numpy

from ProjectLogging import Logger
from Video.Compressor.CompressorInterface import CompressorInterface
from Video.Compressor.CompressorZlib import CompressorZlib
from Video.VideoCamera import VideoCameraInterface
from Video.VideoFilter import VideoFilterInterface
from Video.Serializer import SerializerInterface
from Video.VideoTransmitter import VideoTransmitterInterface


class VideoController:
    """
    Manages a video processing pipeline for capturing, filtering, compressing, serializing,
    and transmitting video data.

    This class provides the necessary structure to manage different stages of video
    processing systematically. Each step in the pipeline is handled by respective interface
    implementations, ensuring modular and maintainable code. The pipeline is designed to
    be flexible, allowing components like filtering, serialization, compression, and
    transmission to be swapped or modified as needed.
    """

    isRunning: bool = False

    def __init__(self):
        """
        Initializes the VideoProcessingPipeline class. This class is responsible for
        constructing and managing a video processing pipeline that may include
        camera input, video filtering, serialization, compression, and data transmission.
        Each step/component of the pipeline is represented by an appropriate interface
        to ensure modular and flexible usage. It provides a way to handle the various
        components of the pipeline systematically, primarily focused on video data.

        Attributes:
            __camera (VideoCameraInterface | None): Represents the camera module for
                capturing video input. It follows the VideoCameraInterface for consistency
                in implementation.
            __filtering (VideoFilterInterface | None): Represents the video filtering
                module responsible for processing and filtering video data. Adheres to the
                VideoFilterInterface.
            __serialization (SerializerInterface | None): Handles the serialization
                of video data, making it ready for further processing such as transmission
                or storage. It implements SerializerInterface.
            __compression (CompressorInterface | None): Represents the module responsible
                for compressing video data. The component can reduce bandwidth usage in
                transmission processes. Follows the CompressorInterface.
            __transmission (VideoTransmitterInterface | None): Manages the transmission
                of processed video data to the designated target. It is implemented
                according to VideoTransmitterInterface.
        """
        self.__camera: VideoCameraInterface | None = None
        self.__filtering: VideoFilterInterface | None = None
        self.__serialization: SerializerInterface | None = None
        self.__compression: CompressorInterface | None = None
        self.__transmission: VideoTransmitterInterface | None = None
        self.__logger: Logger.getLogger = Logger('VideoController', 'VideoControllerLog.log').getLogger

    def setCamera(self, camera: VideoCameraInterface) -> None:
        """
        Setter-Method for the camera interface.
        :param camera: VideoCamera interface that will be used to read video data.
        """
        self.__camera = camera

    def setSerialization(self, serialization: SerializerInterface) -> None:
        """
        Sets the serialization strategy for the VideoController.

        The method sets the SerializerInterface (serialization strategy) object,
        which will be used by the VideoController to serialize data.

        :param serialization: The serialization object to be used by the VideoController.
        """
        self.__serialization = serialization

    def setFiltering(self, filtering: VideoFilterInterface) -> None:
        """
        Setter-Method for the filtering of video data. Not yet implemented.
        :param filtering: VideoFilter that will be applied to the video data.
        """
        self.__logger.warning('Filtering has not been implemented yet!')

    def setCompression(self, compression: CompressorInterface) -> None:
        """
        Setter-Method for the compression of video data.
        :param compression: Compressor that will be used to compress video data.
        """
        self.__compression = compression

    def setTransmission(self, transmission: VideoTransmitterInterface) -> None:
        """
        Setter-Method for the transmission or storage of video data.
        :param transmission: Can be a transmitting or storage object.
        """
        self.__transmission = transmission

    def start(self) -> None:
        """
        Method that starts the VideoController and starts the video processing.
        """
        if not self.isRunning and self.__camera is not None:
            self.isRunning = True
            self.__camera.readCameraInLoop(self.__processFrame)
        elif self.__camera is None:
            exceptionMessage: str = "VideoCamera not initialized! Cannot start video stream!"
            self.__logger.exception(exceptionMessage)
            raise Exception(exceptionMessage)

    def stop(self) -> None:
        """
        Method that stops the VideoController and releases resources.
        """
        if self.isRunning:
            self.__camera.stopCamera()
            self.isRunning = False

    def __processFrame(self, imageFrame: numpy.ndarray) -> None:
        """
        Private Method for processing the video frame.
        :param imageFrame: Image frame that will be processed.
        """
        filteredImage: numpy.ndarray = self.__filter(imageFrame)
        # numpy.ndarray is not the real type here but some compression-format
        compressedImage: numpy.ndarray = self.__compress(filteredImage)
        serializedImageFile: bytes = self.__serialize(compressedImage)
        self.__transmit(serializedImageFile)

    def __filter(self, imageFrame: numpy.ndarray) -> numpy.ndarray:
        """
        Private Method for filtering the video data.
        :param imageFrame: Image frame that will be filtered.
        :return: Filtered image-data.
        """
        if self.__filtering is not None:
            self.__logger.warning('Filtering not yet implemented!')
        return imageFrame

    def __compress(self, imageFrame: numpy.ndarray) -> numpy.ndarray:
        """
        Private Method for compressing the video data.
        :param imageFrame: Image frame that will be compressed.
        :return: Compressed image-data.
        """
        return self.__compression.compress(imageFrame)

    def __serialize(self, imageFrame: numpy.ndarray) -> bytes:
        """
        Private Method for serializing the video data.
        :param imageFrame: Image frame that will be serialized.
        :return: Serialized image file-path.
        """
        if self.__serialization is not None:
            return self.__serialization.serialize(imageFrame)
        else:
            exceptionMessage: str = ('Unable to serialize Image Frame. No transmission object set. Unserialized Image'
                                     ' Frame cannot be transmitted.')
            self.__logger.exception(exceptionMessage)
            raise Exception(exceptionMessage)

    def __transmit(self, frameData: bytes) -> None:
        """
        Private Method for transmitting the image to the client.
        :param frameData: Frame data that will be transmitted.
        """
        if self.__transmission is not None:
            self.__transmission.transmit(frameData)
        else:
            exceptionMessage: str = 'Unable to transmit Image Frame. No transmission object set.'
            self.__logger.exception(exceptionMessage)
            raise Exception(exceptionMessage)
