#!/usr/bin/env python3
# @author      Markus Kösters

import socket
import threading

from Configurations.ConfigReader import ConfigReader


class Server:
    def __init__(self):
        self.__conf = ConfigReader()
        self.__Header = int(self.__conf.readConfigParameter('MessageHeader'))
        self.__Port = int(self.__conf.readConfigParameter('Socket_IP_Port'))
        self.__Server = self.__conf.readConfigParameter('Server_IP_Address')
        self.__Address = (self.__Server, self.__Port)
        self.__Format = self.__conf.readConfigParameter('MessageFormat')
        self.__DisconnectMessage = '!DISCONNECT'
        self.__clientConnection = None

    def __setupServer(self):
        socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketServer.bind(self.__Address)
        print(self.__Address)
        return socketServer

    def getData(self):
        try:
            if self.__clientConnection is not None:
                msg = ''
                msgLength = self.__clientConnection.recv(self.__Header).decode(self.__Format)
                if msgLength:
                    msgLength = int(msgLength)
                    msg = self.__clientConnection.recv(msgLength)
                    if msg and type(msg) is bytes:
                        msg = msg.decode(self.__Format)
                    if str(msg) == self.__DisconnectMessage:
                        print('Robot disconnected!')
                        self.start()
                return msg
        except Exception as e:
            print(f'Receiving data from client failed: {e}')

    def sendData(self, msg):
        try:
            if type(msg) is not str:
                msg = str(msg)
            if type(msg) is not bytes:
                msg = msg.encode(self.__Format)
            msgLength = len(msg)
            sendLength = str(msgLength).encode(self.__Format)
            sendLength += b' ' * (self.__Header - len(sendLength))
            self.__clientConnection.sendall(sendLength)
            self.__clientConnection.sendall(msg)
        except Exception as e:
            print(f'Sending data to client failed: {e}')

    def start(self, debug=False):
        server = self.__setupServer()
        server.listen()
        self.__clientConnection = None
        addr = None
        while not self.__clientConnection:
            self.__clientConnection, addr = server.accept()
            if debug:
                print(f'[ACTIVE CONNECTIONS] {threading.active_count() - 1}')
        print(f'Robot with address:   {addr}   connected.')


if __name__ == '__main__':
    import os

    os.chdir('/home/pi/Desktop/Ro*')
    #from Configurations.ConfigReader import ConfigReader

    print('[STARTING] server is starting...')
    obj = Server()
    obj.start()
    obj.getData()
