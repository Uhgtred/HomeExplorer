#!/usr/bin/env python3
# @author: Markus Kösters

import unittest

from ActorControl import ActorControlFactory, ActorController


class TestActorControlFactory(unittest.TestCase):

    def test_produceActor(self):
        """
        Tests the method `produceActorControlStub` in `ActorControlFactory` to verify
        that it produces an instance of the `ActorController` class.

        :raises AssertionError: If the produced object is not an instance of
                                `ActorController`.

        :return: None
        """
        testObject = ActorControlFactory.produceActorControlStub()
        self.assertIsInstance(testObject, ActorController)


if __name__ == '__main__':
    unittest.main()
