#!/usr/bin/env python3
# @author      Markus Kösters

import socket
from threading import Thread
import time

from Configurations.ConfigReader import ConfigReader
from Network.SocketMessenger import SocketMessenger


class SocketController(Thread):
    instance = None
    __conf = ConfigReader()
    sockets = {'video': [None, int(__conf.readConfigParameter('Video_Port'))], 'controller': [None, int(__conf.readConfigParameter('Communication_Port'))]}

    def __new__(cls):
        """Making sure that the class is only being instanced once"""
        if not cls.instance:
            cls.instance = super(SocketController, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        Thread.__init__(self, name='SocketControllerThread', daemon=True)
        self.address = self.__conf.readConfigParameter('Socket_IP_Address')
        self.messenger = SocketMessenger()
        self.start()

    def connectToServer(self, device: str):
        """Connects client to server returning the socket-object and connection-object"""
        connection = None
        __socket, port = self.sockets.get(device)
        retryCounter = 1
        __socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        __socket.connect((self.address, port))
        retryCounter += 1
        time.sleep(1)
        print(f'Connection to Server established:\t{connection}')
        self.sockets[device][0] = __socket

    def startServer(self, device: str):
        """Starting the socket-server and returning a socket-object"""
        connection, port = self.sockets.get(device)
        socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketServer.bind((self.address, port))
        socketServer.listen()
        addr = None
        print(f'Starting Server: {self.address}:{port}')
        while not connection:
            connection, addr = socketServer.accept()
        print(f'Robot with address:   {addr}  connected.')
        self.sockets[device][0] = connection

    def sendMessage(self, msg, device: str):
        __socket = self.sockets.get(device)[0]
        self.messenger.sendMessage(msg, __socket)

    def receiveMessage(self, device: str):
        __socket = self.sockets.get(device)[0]
        return self.messenger.rcvMessage(__socket)