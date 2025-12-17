from cryptography.fernet import Fernet

class Encryption:

    def __init__(self):
        self.__key: bytes = None

    def generateKey(self) -> bytes:
        return Fernet.generate_key()

    def setKey(self, key: bytes) -> None:
        self.__key = key

    def encrypt(self, data: bytes) -> bytes:
        return Fernet(self.__key).encrypt(data)


    def decrypt(self, data: bytes) -> bytes:
        return Fernet(self.__key).decrypt(data)
