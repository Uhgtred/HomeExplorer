#!/usr/bin/env python3
# @author: Markus Kösters

from flask import jsonify, Response
from flask_restful import Resource

from BusTransactions.BusFactory import BusFactory


class RequestSocket(Resource):
    """
    Class to create a direct socket-connection to the server.
    """

    @staticmethod
    def get(port: int) -> Response:
        """
        Method to create a direct socket-connection to the server.
        :return: List containing the ip and port that the connection will run on if connection is successful. Else returns None.
        """
        socket = BusFactory.produceUDP_Transceiver(host=True, port=port)
        # returning socket-address and port if socket does exist (from open socket)
        if socket is not None:
            return jsonify(socket.bus.sock.getsockname()[0], socket.bus.sock.getsockname()[1])
        return jsonify(None)
