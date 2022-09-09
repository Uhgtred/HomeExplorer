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
        self.frame = None
        self.__conf = ConfigReader()
        self.__Host = self.__conf.readConfigParameter('Socket_IP_Address')
        self.__Port = int(self.__conf.readConfigParameter('Socket_IP_Port'))
        self.__Header = int(self.__conf.readConfigParameter('MessageHeader'))
        self.__Format = self.__conf.readConfigParameter('MessageFormat')
        self.__VideoSize = int(self.__conf.readConfigParameter('VideoSize'))
        self.socketDelay = float(self.__conf.readConfigParameter('SocketDelay'))
        self.__Address = (self.__Host, self.__Port)
        self.__serverConn = None
        self.__DisconnectMessage = '!DISCONNECT'
        self.__socketServer = None
        self.__userInformed = False
        self.sendMsg = ''
        self.rcvMsg = ''
        self.vidData = ''
        self.payloadSize = struct.calcsize('Q')

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
        msg = msg
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
            
    def rcvMessage(self):
        msg = ''
        msgLength = self.__serverConn.recv(self.__Header).decode(self.__Format)
        if msgLength:
            msgLength = int(msgLength)
            msg = self.__serverConn.recv(msgLength)
            print(msg)
            if msg and type(msg) is bytes:
                msg = msg.decode(self.__Format)
            if str(msg) == self.__DisconnectMessage:
                print('Client disconnected!')
                self.start()
        return msg

    def rcvVideo(self):
        """source: https://www.youtube.com/watch?v=7-O7yeO3hNQ"""
        while len(self.vidData) < self.payloadSize:
            data = self.getData()
            if data:
                if len(data) > 500:  # make sure we got a videoframe cause nothing else would be >500 byte
                    packet = self.getData()
                    if not packet:
                        break
                    self.vidData += packet
        packed_msg_size = self.vidData[:self.payloadSize]
        self.vidData = self.vidData[self.payloadSize:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]
        while len(self.vidData) < msg_size:
            data = self.getData()
            if data:
                if len(data) > 500:  # make sure we got a videoframe cause nothing else would be >500 byte
                    self.vidData += self.getData()
        frame_data = self.vidData[:msg_size]
        self.vidData = self.vidData[msg_size:]
        frame = pickle.loads(frame_data)
        return frame

    def disconnect(self):
        if self.__serverConn is not None:
            self.sendData(self.__DisconnectMessage)
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
