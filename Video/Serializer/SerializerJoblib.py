#!/usr/bin/env python3
# @author: Markus Kösters

# import fileinput
# import os
#
# import joblib
# import numpy
#
# from .SerializerConfig import SerializerConfig
# from .SerializerInterface import SerializerInterface

"""
This code is currently not used and not compatible with the current version of the project.
"""
#
# class SerializerJoblib(SerializerInterface):
#     """
#     Class for serializing numpy array before sending it through socket.
#     """
#
#     def __init__(self, config: SerializerConfig):
#         self.__imageFile = config.storageFile
#
#     def serialize(self, imageData: numpy.ndarray = None, filePath: str = '') -> os.path:
#         """
#         Serializes the given image data to a file and returns the absolute path of the file.
#
#         This method serializes image data using joblib and saves it to the specified file
#         path or a default file path determined by the class. It is intended to handle
#         image serialization efficiently and ensures the serialized file path is
#         returned for further usage.
#
#         :param imageData: The image data to serialize. Expected as a numpy array.
#         :type imageData: numpy.ndarray
#         :param filePath: The path of the file where the image data is serialized. An empty
#             string defaults to the class-defined file path.
#         :type filePath: str
#         :return: The absolute filepath of the serialized image file.
#         :rtype: str
#         """
#         super().serialize(imageData, filePath)
#         joblib.dump(imageData, self.__imageFile)
#         # returning absolute filepath of the image-file that has been created.
#         return {'imageFile': os.path.abspath(self.__imageFile)}
#
#     def deserialize(self, filePath: str) -> numpy.ndarray:
#         """
#             Method to load a numpy array from a file
#             :param filePath: The path of the file to load the numpy array from.
#             :return: The loaded numpy array.
#             """
#         return joblib.load(filePath)
