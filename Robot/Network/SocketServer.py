import socket
import threading
import sys
from HardwareConfiguration.ConfigReader import ConfigReader


class Server:
    def __init__(self):
        self.__conf = ConfigReader()
        # Port to listen to (non-privileged ports are > 1024)
        self.__Header = int(self.__conf.readConfigParameter('MessageHeader'))
        self.__Port = int(self.__conf.readConfigParameter('Socket_IP_Port'))
        self.__Server = self.__conf.readConfigParameter('Server_IP_Address')  # socket.gethostbyname(socket.gethostname())
        self.__Address = (self.__Server, self.__Port)
        self.__Format = self.__conf.readConfigParameter('MessageFormat')
        self.__DisconnectMessage = '!DISCONNECT'
        self.__socketServer = None
        self.msg = ''

    def setupServer(self):
        socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketServer.bind(self.__Address)
        print(self.__Address)
        return socketServer

    def handleClient(self, conn, addr, debug=False):
        print(f'Robot with address:   {addr}   connected.')
        connected = True
        while connected:
            msgLength = conn.recv(self.__Header).decode(self.__Format)
            if msgLength:
                msgLength = int(msgLength)
                try:
                    self.msg = conn.recv(msgLength)
                    self.msg = self.msg.decode(self.__Format)
                except:
                    pass
                if debug:
                    print(f'[{addr}] {self.msg}')
                if str(self.msg) == self.__DisconnectMessage:
                    connected = False
                    print('Robot disconnected!')
                    self.start()

    def getData(self):
        data = '00000000'
        data = self.msg
        return data

    def __sendData(self, conn, data):
        byteData = []
        transmissionSuccess = False
        try:
            for element in data:
                try:
                    byteData = (element.to_bytes(1, byteorder=sys.byteorder))
                except:
                    pass
            conn.sendall(byteData)
            transmissionSuccess = True
        except:
            transmissionSuccess = False
        return transmissionSuccess

    def start(self, debug=False):
        server = self.setupServer()
        server.listen()
        conn = None
        addr = None
        while not conn:
            conn, addr = server.accept()
            thread = threading.Thread(target=self.handleClient, args=(conn, addr, debug))
            thread.start()
            if debug:
                print(f'[ACTIVE CONNECTIONS] {threading.active_count() - 1}')
        return conn, addr


if __name__ == '__main__':
    import os
    os.chdir('/home/pi/Desktop/Ro*')
    from HardwareConfiguration.ConfigReader import ConfigReader
    print('[STARTING] serer is starting...')
    obj = Server()
    obj.start()
    obj.getData()
