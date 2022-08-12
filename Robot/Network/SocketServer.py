#!/usr/bin/env python3
# @author      Markus Kösters

import socket
import threading

from Robot.Configurations.ConfigReader import ConfigReader


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
        self.msg = ''
        self.__data = ''

    def setupServer(self):
        socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketServer.bind(self.__Address)
        print(self.__Address)
        return socketServer

    def handleClient(self, addr, debug=False):
        print(f'Robot with address:   {addr}   connected.')
        connected = True
        while connected:
            msgLength = self.__clientConnection.recv(self.__Header).decode(self.__Format)
            if msgLength:
                msgLength = int(msgLength)
                try:
                    self.msg = self.__clientConnection.recv(msgLength)  # if nothing is received this is blocking me
                    self.msg = self.msg.decode(self.__Format)
                except Exception as e:
                    print('Something failed in sockets: ', e)
                if debug:
                    print(f'[{addr}] {self.msg}')
                if str(self.msg) == self.__DisconnectMessage:
                    connected = False
                    print('Robot disconnected!')
                    self.start()

    def getData(self):
        data = self.msg
        return data

    def sendData(self, data):
        print('trying to send data', len(data))
        self.__clientConnection.sendall(data)
        self.__data = data

    def start(self, debug=False):
        server = self.setupServer()
        server.listen()
        self.__clientConnection = None
        addr = None
        while not self.__clientConnection:
            self.__clientConnection, addr = server.accept()
            thread = threading.Thread(target=self.handleClient, args=(addr, debug))
            thread.start()
            if debug:
                print(f'[ACTIVE CONNECTIONS] {threading.active_count() - 1}')
        return self.__clientConnection, addr


if __name__ == '__main__':
    import os

    os.chdir('/home/pi/Desktop/Ro*')
    from HardwareConfiguration.ConfigReader import ConfigReader

    print('[STARTING] server is starting...')
    obj = Server()
    obj.start()
    obj.getData()
