#!/usr/bin/env python3
# @author: Markus Kösters

import unittest

from ActorControl.ActorController import ActorController
from ActorControl.ActorControlFactory import ActorControlFactory


class test_ActorControlFactory(unittest.TestCase):
    def test_produceActor(self):
        testObject = ActorControlFactory.produceActorControl()
        self.assertIsInstance(testObject, ActorController)

if __name__ == '__main__':
    unittest.main()
