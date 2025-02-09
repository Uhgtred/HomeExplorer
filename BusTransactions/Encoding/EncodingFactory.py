#!/usr/bin/env python3
# @author Markus Kösters

from . import BusEncodings


class EncodingFactory:
    """
    Container to make all Encodings available through one object.
    """

    @staticmethod
    def arduinoSerialEncoding():
        return BusEncodings.ArduinoSerialEncoding()

    @staticmethod
    def socketEncoding(encodingType: str = "json"):
        match encodingType:
            case "json": return BusEncodings.SocketEncodingJson()
            case "python": return BusEncodings.SocketEncoding()
        raise ValueError("Unknown encoding type!")