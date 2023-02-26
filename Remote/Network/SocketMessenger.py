#!/usr/bin/env python3
# @author      Markus Kösters

import struct


class SocketMessenger:

    def __init__(self):
        self.__maxMsgSize = 4096

    def rcvMessage(self, _socket: object):
        __msgLengthExpected = struct.calcsize('Q')
        __msgLengthReceived = b''
        while len(__msgLengthReceived) < __msgLengthExpected:
            rcvSize = __msgLengthExpected - len(__msgLengthReceived)
            packet = _socket.recv(rcvSize if rcvSize <= self.__maxMsgSize else self.__maxMsgSize)
            if not packet:
                break
            __msgLengthReceived += packet
        __msgData = b''
        __msgLengthReceived = struct.unpack('Q', __msgLengthReceived)[0]
        while len(__msgData) < __msgLengthReceived:
            rcvSize = __msgLengthReceived - len(__msgData)
            __msgData += _socket.recv(rcvSize if rcvSize <= self.__maxMsgSize else self.__maxMsgSize)
        return __msgData

    @staticmethod
    def sendMessage(msg, _socket: object):
        if type(msg) is not bytes:
            msg = msg.encode()
        __msgLengthSend = len(msg)
        __message = struct.pack('Q', __msgLengthSend) + msg
        _socket.sendall(__message)


if __name__ == '__main__':
    import os

    os.chdir('/home/pi/Desktop/Ro*')
    # from Configurations.ConfigReader import ConfigReader

    print('[STARTING] server is starting...')
    obj = SocketMessenger()
    obj.start()
    obj.getData()
