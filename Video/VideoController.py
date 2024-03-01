#!/usr/bin/env python3
# @author: Markus Kösters

import numpy

from Video.VideoCamera import VideoCameraInterface
from Video.VideoFilter import VideoFilterInterface
from Video.Serializer import SerializerInterface
from Video.VideoTransmitter import VideoTransmitterInterface


class VideoController:
    """
    Class for controlling video.
    """

    def __init__(self):
        self.isRunning = False
        self.__camera = None
        self.__filtering = None
        self.__serialization = None
        self.__compression = None
        self.__transmission = None

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
        Setter-Method for the filtering of video data.
        :param filtering: VideoFilter that will be applied to the video data.
        """

    def setCompression(self, compression) -> None:
        """
        Setter-Method for the compression of video data.
        :param compression: Compressor that will be used to compress video data.
        """
        if self.__compression is not None:
            # TODO: implement compression if needed. Else remove this.
            pass

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
            raise Exception("VideoCamera not initialized! Cannot start video stream!")

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
        compressedImage: numpy.ndarray = self.__compress(filteredImage)
        serializedImageFile: str = self.__serialize(compressedImage)
        self.__transmit(serializedImageFile)

    def __filter(self, imageFrame: numpy.ndarray) -> numpy.ndarray:
        """
        Private Method for filtering the video data.
        :param imageFrame: Image frame that will be filtered.
        :return: Filtered image-data.
        """
        if self.__filtering is not None:
            # TODO: implement filtering if needed. Else remove this.
            pass
        return imageFrame

    def __compress(self, imageFrame: numpy.ndarray) -> numpy.ndarray:
        """
        Private Method for compressing the video data.
        :param imageFrame: Image frame that will be compressed.
        :return: Compressed image-data.
        """
        if self.__filtering is not None:
            # TODO: implement compression if needed. Else remove this.
            pass
        return imageFrame

    def __serialize(self, imageFrame: numpy.ndarray) -> str:
        """
        Private Method for serializing the video data.
        :param imageFrame: Image frame that will be serialized.
        :return: Serialized image file-path.
        """
        if self.__serialization is not None:
            return self.__serialization.serialize(imageFrame)
        else:
            raise Exception('Unable to serialize Image Frame. No transmission object set. Unserialized Image Frame '
                            'cannot be transmitted.')

    def __transmit(self, imageFilePath: str) -> None:
        """
        Private Method for transmitting the image to the client.
        :param imageFilePath: Path to the serialized image-file.
        """
        if self.__transmission is not None:
            with open(imageFilePath, 'rb') as imageFile:
                imageData = imageFile.read()
            self.__transmission.transmit(imageData)
        else:
            raise Exception('Unable to transmit Image Frame. No transmission object set.')
