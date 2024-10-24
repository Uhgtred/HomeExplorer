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
    MyIPAddress: str = '192.168.178.36'
    YourIPAddress: str = '192.168.178.44'
    busLibrary: socket = socket
