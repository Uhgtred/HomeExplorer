#!/usr/bin/env python3
# @author: Markus Kösters
import json
import time
import unittest
import requests

from API.main import Main


class test_RequestSocket(unittest.TestCase):
    mainObject = None
    port = 3001

    def setUp(self):
        self.mainObject = Main(3000)

    def test_get(self):
        self.mainObject.runServer()
        time.sleep(5)
        sock = requests.get(f'http://127.0.0.1:3000/getSocketAddress/{self.port}')
        sockResponse = json.loads(sock.content)
        # self.assertListEqual(sockResponse, ['127.0.0.1', 2001])
        self.assertEqual(sockResponse[1], self.port)
        self.assertEqual(sockResponse[0], '127.0.0.1')
        Main.stopServer()


if __name__ == '__main__':
    unittest.main()
