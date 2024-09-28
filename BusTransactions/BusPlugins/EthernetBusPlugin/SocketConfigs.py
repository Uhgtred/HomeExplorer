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
    HostIPAddress: str = 'localhost'
    ClientIPAddress: str = ''
    busLibrary: socket = socket
