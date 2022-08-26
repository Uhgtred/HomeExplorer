#!/usr/bin/env python3
# @author   Markus Kösters

import pickle
import struct
import cv2
import time

from Configuration.ConfigReader import ConfigReader
import socket


class SocketClient:

    def __init__(self):
        self.__conf = ConfigReader()
        self.__Host = self.__conf.readConfigParameter('Socket_IP_Address')
        self.__Port = int(self.__conf.readConfigParameter('Socket_IP_Port'))
        self.__Header = int(self.__conf.readConfigParameter('MessageHeader'))
        self.__Format = self.__conf.readConfigParameter('MessageFormat')
        self.__VideoSize = int(self.__conf.readConfigParameter('VideoSize'))
        self.socketDelay = self.__conf.readConfigParameter('SocketDelay')
        self.__Address = (self.__Host, self.__Port)
        self.__serverConn = None
        self.__DisconnectMessage = '!DISCONNECT'
        self.__socketServer = None
        self.__userInformed = False
        self.sendMsg = ''
        self.rcvMsg = ''

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

    def sendMessage(self):
        while True:
            msg = self.sendMsg
            if msg:
                if type(msg) is not str:
                    msg = str(msg)
                if type(msg) is not bytes:
                    msg = msg.encode(self.__Format)
                __msgLength = len(msg)
                __sendLength = str(__msgLength).encode(self.__Format)
                __sendLength += b' ' * (self.__Header - len(__sendLength))
                self.__serverConn.sendall(__sendLength)
                self.__serverConn.sendall(msg)
            time.sleep(self.socketDelay)
    
    def rcvMessage(self):
        while True:
            msg = ''
            msgLength = self.__serverConn.recv(self.__Header).decode(self.__Format)
            if msgLength:
                msgLength = int(msgLength)
                msg = self.__serverConn.recv(msgLength)
                if msg and type(msg) is bytes:
                    msg = msg.decode(self.__Format)
                if str(msg) == self.__DisconnectMessage:
                    self.disconnect()
                    print('Server disconnected!')
            self.rcvMsg = msg
            time.sleep(self.socketDelay)
    
    def getData(self):
        if self.rcvMsg:
            return self.rcvMsg
    
    def sendData(self, data):
        self.sendMsg = data

    def rcvVideo(self):
        """source: https://www.youtube.com/watch?v=7-O7yeO3hNQ"""
        try:
            rawVidData = b''
            # payLoadLength = struct.calcsize('Q')
            if self.__serverConn:
                # while len(rawVidData) <= payLoadLength:
                #     tmpMessage = self.getData()
                #     if not tmpMessage:
                #         break
                #     rawVidData += tmpMessage
                packedMessage = self.getData()
                # packedMessage = rawVidData[:payLoadLength]
                # rawVidData = rawVidData[payLoadLength:]
                # vid = struct.unpack('Q', packedMessage)
                vid = pickle.loads(packedMessage)
                cv2.imshow('RobotStream', vid)
                key = cv2.waitKey(1) & 0xFF
        except Exception as e:
            print('Video-stream interrupted', e)

    def disconnect(self):
        if self.__serverConn is not None:
            self.sendMessage(self.__DisconnectMessage)
            self.__serverConn.close()

if __name__ == '__main__':
    import time
    msg = 'Furz'
    start = time.time()
    if type(msg) is not str:
        msg = str(msg)
    if type(msg) is not bytes:
        msg = msg.encode('utf-8')
    __msgLength = len(msg)
    print(__msgLength)
    __sendLength = str(__msgLength).encode('utf-8')
    print(__sendLength)
    __sendLength += b' ' * (32 - len(__sendLength))
    print(len(__sendLength))
    print(time.time() - start)
    #self.__serverConn.send(__sendLength)
    #self.__serverConn.send(msg)
