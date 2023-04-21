#!/usr/bin/env python3
# @author      Markus Kösters
import socket
import struct

from Configurations import ConfigReader


class SocketMessenger:

    def __init__(self):
        self.conf = ConfigReader()
        self.__maxMsgSize = self.conf.readConfigParameter('MaxMessageSize')

    def __rcvMessageLength(self, socket_: socket.socket):
        """
        Receiving the length of the message, which itself has a length of 8 byte and is packed via struct.pack.
        Returns the message-length of the following, incoming message!
        """
        msgLengthFieldLength = struct.calcsize('Q')
        msgLength = b''
        # running loop until size of message-length (msgLengthFieldLength (8byte)) has been reached
        while len(msgLength) < msgLengthFieldLength:
            # varying receive-length to only receive the bytes necessary for this operation
            rcvSize = msgLengthFieldLength - len(msgLength)
            # receiving dynamic size of packets until every byte has been received
            packet = socket_.recv(rcvSize if rcvSize <= self.__maxMsgSize else self.__maxMsgSize)
            if not packet:
                break
            # adding up the snippets of the message
            msgLength += packet
        # unpacking the message-length
        msgLength = struct.unpack('Q', msgLength)[0]
        return msgLength

    def rcvMessage(self, socket_: socket.socket):
        """
        Receiving the actual message, depending on the message-length that is being received through rcvMessageLength!
        Returns the ENCODED data from the received message (for decoding use: msgData.decode('utf-8'))!
        """
        msgLength = self.__rcvMessageLength(socket_)
        msgData = b''
        # running loop until size of message-length (msgLength) has been reached
        while len(msgData) < msgLength:
            # varying receive-length to only receive the bytes of this specific message
            rcvSize = msgLength - len(msgData)
            # receiving dynamic size of packets until every byte has been received
            msgData += socket_.recv(rcvSize if rcvSize <= self.__maxMsgSize else self.__maxMsgSize)
        return msgData

    @staticmethod
    def sendMessage(msg, socket_: socket.socket):
        """Sending encoded message-content + length of the message to the passed socket-object"""
        if type(msg) is not bytes:
            msg = msg.encode()
        __msgLengthSend = len(msg)
        __message = struct.pack('Q', __msgLengthSend) + msg
        socket_.sendall(__message)


if __name__ == '__main__':
    # testing
    import os

    os.chdir('/home/pi/Desktop/Ro*')
    # from Configurations.ConfigReader import ConfigReader

    print('[STARTING] server is starting...')
    obj = SocketMessenger()
    obj.start()
    obj.getData()
