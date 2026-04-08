import typing

import msgpack

from BusTransactions.Serialization.SerializationProtocol import SerializationProtocol


class SerializerMsgPack(SerializationProtocol):

    def serialize(self, data: typing.Any) -> bytes:
        serializedData: bytes = msgpack.packb(data)
        return serializedData

    def deSerialize(self, serializedData: bytes) -> typing.Any:
        deserializedData: typing.Any = msgpack.unpackb(serializedData)
        return deserializedData