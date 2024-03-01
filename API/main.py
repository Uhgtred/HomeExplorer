#!/usr/bin/env python3
# @author: Markus Kösters

from multiprocessing import Process

from flask import Flask
from flask_restful import Api

from API import RequestSocket
from API.StopServer import RestartServer


class Main:
    """
    Main class for setting up and starting the Flask application and API.
    """

    __app: Flask = Flask(__name__)
    __resources: dict = {
        RequestSocket: '/getSocketAddress/<int:port>',
        RestartServer: '/restartAPIServer'
    }
    __process: Process = None

    def __init__(self, port: int) -> None:
        self.__app: Flask = Flask('RobotAPI')
        self.api: Api = Api(self.__app)
        self.__port: int = port

    def __addRoutes(self) -> None:
        """
        Method that adds routes to the api instance.
        """
        for resource in self.__resources:
            self.api.add_resource(resource, self.__resources.get(resource))

    @property
    def getResources(self) -> dict:
        """
        Getter-method for the possible requests to the api.
        :return: Dictionary with the methods available for the api and their url.
        """
        return self.__resources

    def runServer(self) -> None:
        """
        Method that starts the api server in a separate process and adds routes to the api instance.
        """
        self.__addRoutes()
        self.__process = Process(target=self.__serverSetup, daemon=True)
        self.__process.start()

    def __serverSetup(self) -> None:
        """
        Internal method to setup server-credentials.
        """
        self.__app.run(host='127.0.0.1', port=self.__port)

    @classmethod
    def stopServer(cls) -> None:
        """
        Method for stopping the process that the api server is running on.
        """
        if cls.__process is not None:
            cls.__process.kill()
            cls.__process = None
