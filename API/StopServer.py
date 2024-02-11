#!/usr/bin/env python3
# @author: Markus Kösters

import subprocess
from flask import Response, jsonify
from flask_restful import Resource


class RestartServer(Resource):
    """
    Class to restart server through the API.
    Source: https://gist.github.com/eyJhb/9668061f06163421b5b46b61f41d2c48
    """

    def get(self) -> Response:
        """
        Method for shutting down the flask server.
        :return: A response informing about restarting the server.
        """
        subprocess.run("shutdown -r 0", shell=True, check=True)  # -r restart -h shutdown
        return jsonify("Restarting API-Server!")
