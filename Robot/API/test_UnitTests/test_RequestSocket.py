#!/usr/bin/env python3
# @author: Markus Kösters
import json
import time
import unittest
import requests

from API.main import Main


class test_RequestSocket(unittest.TestCase):
    mainObject = None

    def setUp(self):
        self.mainObject = Main()

    def test_get(self):
        self.mainObject.runServer()
        time.sleep(5)
        sock = requests.get('http://127.0.0.1:2000/getSocketAddress')
        sockResponse = json.loads(sock.content)
        # self.assertListEqual(sockResponse, ['127.0.0.1', 2001])
        self.assertGreater(sockResponse[1], 2000)
        self.assertEqual(sockResponse[0], '127.0.0.1')
        Main.stopServer()


if __name__ == '__main__':
    unittest.main()
