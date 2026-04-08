#!/usr/bin/env python3
# @author   Markus Kösters

import os
import typing

import API
import ProjectLogging
import Runners
from ActorControl import ActorController
from ActorControl.ActorControlFactory import ActorControlFactory

from BusTransactions.BusInterface import BusInterface
from BusTransactions.DefaultBusFactory import DefaultBusFactory
from Events import EventManager, Event
from PortsEnum import PortsEnum
from Video import VideoControllerBuilder, VideoController
from Video.VideoCamera import VideoCameraFactory, VideoCamera
from Video.VideoTransmitter import VideoTransmitterInterface, VideoTransmitterFactory

# changing working-directory to parent of this file
os.chdir(os.path.dirname(os.getcwd()))


class Main:
    """
    Main program for managing the process and starting the program.
    """

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
        #       This should be a subrepository inside this repository or even a package on pypi, so it can be imported with it's latest version.
        # Most importantly, there needs to be the close function inside the all ethernet plugins
        self.__ports = PortsEnum
        self.__logger = ProjectLogging.Logger('Main', 'MainLog.log').getLogger
        self.__threadRunner = Runners.threadRunner.ThreadRunner()
        self.__setup()

    def __setup(self) -> None:
        """
            Sets up the components required for the system by initializing
            steering control, video control, and API setup processes. If any
            step fails, throws a BaseException with an appropriate error message.

            :raises BaseException: If an error occurs during setup, it wraps and
                re-raises the exception with a descriptive message.
            """
        self.__logger.info('Starting initialization process...')
        try:
            self.__logger.info('Press Ctrl+C to exit...')
            self.__steeringControl()
            self.__videoControl()
            # Todo: activate proper use of the api for maintainability.
            # self.__apiSetup()
            self.__threadRunner.runTasks()
        except Exception as e:
            self.__logger.exception(f'An error occurred during setup: {e}')
            raise BaseException(f'An error occurred during setup: {e}')
        except KeyboardInterrupt:
            self.__logger.info('Robot interrupted by user!')
        self.__logger.info('Initialization process complete! Robot ready!')


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
        remoteControlSocket: typing.Type[BusInterface] = (
            DefaultBusFactory.produceUPD_Transceiver_Python_Encoding(port = self.__ports.CONTROLLERPORT.value))
        actorController: ActorController = ActorControlFactory.produceActorControlXbox()
        remoteControlEvent: Event = EventManager.produceEvent('controllerEvent')
        # Subscribes to an event that notifies the subscribers with the buttons that have been pushed.
        remoteControlEvent.subscribe(actorController.processInput)
        self.__threadRunner.addTask(remoteControlSocket.readBusUntilStopFlag,
                                    remoteControlEvent.notifySubscribers)
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
        apiObject = API.Main(port=self.__ports.APIPORT.value)
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
        transmitter: VideoTransmitterInterface = (VideoTransmitterFactory.
                                                  produceDefaultVideoTransmitter(self.__ports.VIDEOPORT.value))
        videoController: VideoController = (VideoControllerBuilder()
                                            .addCamera(camera)
                                            .addTransmission(transmitter)
                                            .build())
        self.__threadRunner.addTask(videoController.start)
        self.__logger.info('Video streaming setup complete!')


if __name__ == '__main__':
    main = Main()
