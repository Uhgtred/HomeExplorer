#!/usr/bin/env python3
# @author   Markus Kösters
import logging
import os

import API
import Runners
from ActorControl import ActorController
from ActorControl.ActorControlFactory import ActorControlFactory
from BusTransactions.BusFactory import BusFactory
from Events import EventManager
from ProjectLogging.Logger import Logger
from Video import VideoControllerBuilder, Serializer, Compressor, VideoController
from Video.Compressor.CompressorFactory import CompressorFactory
from Video.Serializer.SerializerFactory import SerializerFactory
from Video.VideoCamera import VideoCameraFactory, VideoCamera
from Video.VideoTransmitter import VideoTransmitter
from Video.VideoTransmitter.VideoTransmitterFactory import VideoTransmitterFactory

# changing working-directory to parent of this file
os.chdir(os.path.dirname(os.getcwd()))


class Main:
    """
    Main program for managing the process and starting the program.
    """
    __ports: dict = {'controllerPort': 2001, 'APIPort': 3000, 'videoPort': 2002}

    def __init__(self):
        """
        Initializes and runs asynchronous and threaded runners for task execution.

        This constructor sets up and initializes both an asynchronous and a threaded
        runner to handle tasks. The function ensures proper setup of runners and their
        subsequent execution. This can include initializing resources required for
        asynchronous and threaded processing, preparing tasks, and starting task
        execution in both runners.

        Attributes:
            __threadRunner: An instance of `AsyncRunner` for handling asynchronous
                tasks.
            __threadRunner: An instance of `ThreadRunner` for handling threaded tasks.

        Raises:
            Any exceptions that might occur during setup or task execution.

        """
        # Todo: After Systemtest check the versions of the code in BusTransactions repository vs the versions in HomeExplorer and RobotRemote
        # Most importantly, there needs to be the close function inside the all ethernet plugins
        self.__logger = Logger('Main', 'MainLog.log').getLogger
        self.__logger.info('Starting initialization process...')
        self.__threadRunner = Runners.threadRunner.ThreadRunner()
        self.__setup()
        self.__logger.info('Initialization process complete! Robot ready!')

    def __setup(self) -> None:
        """
            Sets up the components required for the system by initializing
            steering control, video control, and API setup processes. If any
            step fails, throws a BaseException with an appropriate error message.

            :raises BaseException: If an error occurs during setup, it wraps and
                re-raises the exception with a descriptive message.
            """
        try:
            pass
            self.__steeringControl()
            self.__videoControl()
            # Todo: activate proper use of the api for maintainability.
            # self.__apiSetup()
            self.__threadRunner.runTasks()
        except Exception as e:
            self.__logger.exception(f'An error occurred during setup: {e}')
            raise BaseException(f'An error occurred during setup: {e}')

    def __steeringControl(self) -> None:
        """
        Sets up the steering mechanism by integrating remote control socket communication
        with actor control and event management. Creates and configures the necessary
        parts such as a remote control socket, an actor controller, and an event
        manager to facilitate asynchronous handling of control inputs.

        The method subscribes the actor controller to the event manager and schedules
        an asynchronous task to continuously read data from the remote control socket
        and notify all subscribed components when new data is received.
        """
        self.__logger.info('Setting up steering control...')
        remoteControlSocket = BusFactory.produceUDP_Transceiver(port=self.__ports.get('controllerPort'))
        actorController: ActorController = ActorControlFactory.produceActorControl()
        remoteControlEvent = EventManager.produceEvent('controllerEvent')
        remoteControlEvent.subscribe(actorController.processInput)
        self.__threadRunner.addTask(remoteControlSocket.readBusUntilStopFlag, remoteControlEvent.notifySubscribers)
        self.__logger.info('Steering control setup complete!')

    def __apiSetup(self):
        """
        Sets up and initializes the API server.

        This method creates an instance of the `API.Main` class configured with
        a port number fetched from a dictionary and starts the API server by
        invoking the `runServer` method.

        :raises KeyError: If 'APIPort' key is not found in the `self.__ports` dictionary.
        """
        self.__logger.info('Setting up API server...')
        apiObject = API.Main(port=self.__ports.get('APIPort'))
        apiObject.runServer()
        self.__logger.info('API server started!')

    def __videoControl(self) -> None:
        """
        Sets up video streaming by initializing required components such as a camera, serializer,
        and transmitter, then setting up video control logic through a `VideoController` instance.
        The video control task is registered to a thread runner for asynchronous execution.

        :raises KeyError: If the 'videoPort' key is missing in the `self.__ports` dictionary.
        """
        self.__logger.info('Setting up video streaming...')
        camera: VideoCamera = VideoCameraFactory.produceDefaultCameraInstance()
        serializer: Serializer = SerializerFactory.produceSerializationMsgPack()
        transmitter: VideoTransmitter = VideoTransmitterFactory.produceDefaultVideoTransmitter(self.__ports.get('videoPort'))
        compressor: Compressor = CompressorFactory.produceCompressorZlib()
        videoController: VideoController = (VideoControllerBuilder()
                           .addCamera(camera)
                           .addSerialization(serializer)
                           .addTransmission(transmitter)
                           .addCompression(compressor)
                           .build())
        self.__threadRunner.addTask(videoController.start)
        self.__logger.info('Video streaming setup complete!')


if __name__ == '__main__':
    main = Main()
