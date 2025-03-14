#!/usr/bin/env python3
# @author: Markus Kösters

import unittest

from ..ActorController import ActorController
from ..ActorControlFactory import ActorControlFactory


class test_ActorControlFactory(unittest.TestCase):

    def test_produceActor(self):
        testObject = ActorControlFactory.produceActorControlStub()
        self.assertIsInstance(testObject, ActorController)


if __name__ == '__main__':
    unittest.main()
