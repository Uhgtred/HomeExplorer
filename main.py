#!/usr/bin/env python3
# @author   Markus Kösters

import os

import API
import Runners
from ActorControl import ActorController
from ActorControl.ActorControlFactory import ActorControlFactory
from BusTransactions.BusFactory import BusFactory
from Events import EventManager
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
        # Todo: System test for communication between remote-control and robot.
        # Todo: After Systemtest check the versions of the code in BusTransactions repository vs the versions in HomeExplorer and RobotRemote
        # Most importantly, there needs to be the close function inside the all ethernet plugins
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
            self.__steeringControl()
            self.__videoControl()
            self.__apiSetup()
        except Exception as e:
            raise BaseException(f'An error occurred during setup: {e}')

    def __steeringControl(self) -> None:
        """
        Method that sets up connection and communication to the Arduino.
        """
        remoteControlSocket = BusFactory.produceUDP_Transceiver(host=True, port=self.__ports.get('controllerPort'))
        actorController = ActorControlFactory.produceActorControl()
        remoteControlEvent = EventManager.produceEvent('controllerEvent')
        remoteControlEvent.subscribe(actorController.processInput)
        remoteControlEvent.subscribe(self.print_)
        self.__asyncRunner.addTask(remoteControlSocket.readBusUntilStopFlag, remoteControlEvent.notifySubscribers)

    def __apiSetup(self):
        apiObject = API.Main(port=self.__ports.get('APIPort'))
        apiObject.runServer()

    def print_(self, message):
        print(message)

    def __videoControl(self) -> None:
        """
        Method that sets up video-recording serialization and streaming.
        """
        camera = VideoCameraFactory.produceDefaultCameraInstance()
        serializer = SerializerFactory.produceSerializationJoblib()
        transmitter = VideoTransmitterFactory.produceDefaultVideoTransmitter(self.__ports.get('videoPort'))
        videoController = VideoControllerBuilder().addCamera(camera).addSerialization(serializer).addTransmission(transmitter).build()
        self.__threadRunner.addTask(videoController.start)


if __name__ == '__main__':
    main = Main()
