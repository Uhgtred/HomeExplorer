#!/usr/bin/env python3
# @author   Markus Kösters
import pickle
import struct

import cv2

from Remote.Configuration.ConfigReader import ConfigReader
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
        self.__VideoSize = int(self.__conf.readConfigParameter('VideoSize'))
        self.__DisconnectMessage = '!DISCONNECT'
        self.__socketServer = None
        self.__userInformed = False
    
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

    def rcvVideo(self):
        """source: https://www.youtube.com/watch?v=7-O7yeO3hNQ"""
        try:
            if self.__serverConn is not None:
                rawVidData = b''
                payLoadLength = struct.calcsize('Q')
                if self.__serverConn:
                    while len(rawVidData) <= payLoadLength:
                        tmpMessage = self.__serverConn.recv(self.__VideoSize)
                        if not tmpMessage:
                            break
                        rawVidData += tmpMessage
                    packedMessage = rawVidData[:payLoadLength]
                    rawVidData = rawVidData[payLoadLength:]
                    msgLength = struct.unpack('Q', packedMessage)[0]
                    while len(rawVidData) < msgLength:
                        rawVidData += self.__serverConn.recv(self.__VideoSize)
                    vidData = rawVidData[:msgLength]
                    rawVidData = rawVidData[msgLength:]
                    vid = pickle.loads(vidData)
                    cv2.imshow('RobotStream', vid)
                    key = cv2.waitKey(1) & 0xFF
        except Exception as e:
            print('Video-stream interrupted', e)

    def disconnect(self):
        try:
            if self.__serverConn is not None:
                self.sendMessage(self.__DisconnectMessage)
                self.__serverConn.close()
        except:
            pass
