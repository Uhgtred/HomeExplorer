#!/usr/bin/env python3
# @author: Markus Kösters

from dataclasses import dataclass
import socket


@dataclass
class UdpSocketConfig:
    """
    Config-dataclass for Serial-busses.
    """
    messageSize: int
    port: int
    host: bool
    # IP-Address of the device that this script is running on
    MyIPAddress: str = '192.168.178.36'
    # IP-Address of the device that will be connected to the socket from the other side.
    YourIPAddress: str = '192.168.178.44'
    busLibrary: socket = socket
