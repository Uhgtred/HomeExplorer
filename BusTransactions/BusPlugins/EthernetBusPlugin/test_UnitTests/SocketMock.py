#!/usr/bin/env python3
# @author: Markus Kösters

class MockSocket:
    """
    Todo: make the buffer a dictionary with IP as key and buffer as value.
    """
    buffer = []
    state = False
    AF_INET = None
    SOCK_STREAM = None
    SOCK_DGRAM = None
    passedArgs = []

    def __init__(self, *args, **kwargs):
        self.passedArgs.extend(args)
        self.passedArgs.extend(kwargs)

    @classmethod
    def recvfrom(cls, messageSize):
        # print(f'Receiving {messageSize} bytes.')
        if cls.buffer:
            message = cls.buffer.pop(0)
            if len(message[messageSize:]) > 0:
                cls.buffer.append(message[messageSize:])
            return message[:messageSize]    
        else:
            return None

    @staticmethod
    def bind(address):
        print(f'Address of socket: {address}')

    @classmethod
    def socket(cls, *args):
        if cls.state:
            cls.state = True
        else:
            cls.state = False
        return cls

    @classmethod
    def sendto(cls, message, address):
        print(f'Sending message: {message} to socket: {address}')
        cls.buffer.append(message)

    @property
    def getBuffer(self):
        return self.buffer

    @classmethod
    def close(cls) -> None:
        """
        Closes the class-level state.

        This method is used to modify the class attribute `state`. It sets the
        `state` attribute to `False`, effectively closing or deactivating the
        state. The method acts on the class level and modifies the shared
        state attribute for all instances of the class.

        :raises: No exceptions are raised by this function.
        """
        cls.state = False