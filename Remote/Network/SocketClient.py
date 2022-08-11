#!/usr/bin/env python3
# @author   Markus Kösters

from HardwareConfiguration.ConfigReader import ConfigReader
import socket


class SocketClient:
    
    def __init__(self):
        self.__conf = ConfigReader()
        self.__serverConn = None
        self.__Host = self.__conf.readConfigParameter('Socket_IP_Address')
        self.__Port = int(self.__conf.readConfigParameter('Socket_IP_Port'))
        self.__Header = int(self.__conf.readConfigParameter('MessageHeader'))
        self.__Address = (self.__Host, self.__Port)
        self.__Format = self.__conf.readConfigParameter('MessageFormat')
        self.__DisconnectMessage = '!DISCONNECT'
        self.__socketServer = None
        self.__userInformed = False
        
    def __del__(self):
        self.disconnect()
    
    def connect(self):
        try:
            print(self.__Address)
            self.__serverConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__serverConn.connect(self.__Address)
            return True
        except Exception as e:
            print('Exception in server-connection', e)
            return False
            
    def sendMessage(self, msg):
        if type(msg) is not str:
            msg = str(msg)
        if type(msg) is not bytes:
            msg = msg.encode(self.__Format)
        __msgLength = len(msg)
        __sendLength = str(__msgLength).encode(self.__Format)
        __sendLength += b' ' * (self.__Header - len(__sendLength))
        self.__serverConn.send(__sendLength)
        self.__serverConn.send(msg)
    
    def rcvCommands(self): #HAS TO BE ADAPTED TO NEW HANDSHAKE-SYSTEM
        try:
            if self.__serverConn is not None:
                __msgLength = self.__serverConn.recv(self.__Header)
                __data = self.__serverConn.recv(__msgLength)
                for i in range(len(__data)):
                    try:
                        __data[i] = __data[i].decode(self.__Format)
                    except:
                        pass
                if str(__data) == self.__DisconnectMessage:
                    self.disconnect()
                return __data
        except:
            pass
        
    def disconnect(self):
        try:
            if self.__serverConn is not None:
                self.sendMessage(self.__DisconnectMessage)
                self.__serverConn.close()
        except:
            pass
