from typing import Protocol


class EncryptionProtocol(Protocol):

    def __init__(self):
        ...

    def generateKey(self) -> bytes:
        ...

    def setKey(self, key: bytes) -> None:
        ...

    def encrypt(self, data: bytes) -> bytes:
        ...

    def decrypt(self, data: bytes) -> bytes:
        ...