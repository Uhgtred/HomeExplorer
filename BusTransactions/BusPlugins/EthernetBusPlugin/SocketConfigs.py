#!/usr/bin/env python3
# @author: Markus Kösters

from dataclasses import dataclass
import socket


@dataclass
class UdpSocketConfig:
    """
    Config-dataclass for Serial-busses.
    """
    IPAddress: str
    messageSize: int
    startPort: int
    busLibrary: socket = socket
