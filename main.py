#!/usr/bin/env python3
# @author   Markus Kösters

import os

import API
import Runners
from BusTransactions.BusFactory import BusFactory
from Events import EventFactory
from Video import VideoController, VideoControllerBuilder
from Video.Serializer.SerializerFactory import SerializerFactory
from Video.VideoCamera import VideoCameraFactory
from Video.VideoTransmitter import VideoTransmitterFactory

# changing working-directory to parent of this file
os.chdir(os.path.dirname(os.getcwd()))


class Main:
    """
    Main program for managing the process and starting the program.
    """
    __ports: dict = {'controllerPort': 2001, 'APIPort': 3000, 'videoPort': 2002}

    def __init__(self):
        """Starting the Robot-Program and configuring everything"""
        self.__asyncRunner = Runners.asyncRunner.AsyncRunner()
        self.__threadRunner = Runners.threadRunner.ThreadRunner()
        self.__setup()
        self.__asyncRunner.runTasks()
        self.__threadRunner.runTasks()

    def __setup(self) -> None:
        """
        Method for handling any setups necessary for the program to run.
        Catches exceptions that may occur during the setup process.
        """
        try:
            self.__arduinoConnection()
            self.__videoControl()
            self.__threadRunner.addTask(API.Main(self.__ports.get('APIPort')))
        except Exception as e:
            raise BaseException(f'An error occurred during setup: {e}')

    def __arduinoConnection(self) -> None:
        """
        Method that sets up connection and communication to the Arduino.
        """
        remoteControlSocket = BusFactory.produceUDP_Transceiver(host=True, port=self.__ports.get('controllerPort'))
        arduinoSerial = BusFactory.produceSerialTransceiver()
        remoteControlEvent = EventFactory.produceEvent('controllerEvent')
        remoteControlEvent.subscribe(arduinoSerial.writeSingleMessage)
        self.__asyncRunner.addTask(remoteControlSocket.readBusUntilStopFlag(remoteControlEvent.notifySubscribers))

    def __videoControl(self) -> None:
        """
        Method that sets up video-recording serialization and streaming.
        """
        camera = VideoCameraFactory.produceDefaultCameraInstance()
        serializer = SerializerFactory.produceSerializationJoblib()
        transmitter = VideoTransmitterFactory.produceDefaultVideoTransmitter(self.__ports.get('videoPort'))
        videoController = VideoControllerBuilder().addCamera(camera).addSerialization(serializer).addTransmitter(transmitter).build()
        self.__threadRunner.addTask(videoController)



if __name__ == '__main__':
    main = Main()
