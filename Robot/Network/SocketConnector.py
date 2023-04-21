#!/usr/bin/env python3
# @author      Markus Kösters

import socket

from .SocketController import SocketController


class SocketConnector(SocketController):

    def __init__(self, IP, port):
        super().__init__(IP, port)

    def connectToServer(self, IP: str, port: int):
        """Connects client to server returning the socket-object and connection-object"""
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((IP, port))
        print(f'Connection to Server established!')
        return client
