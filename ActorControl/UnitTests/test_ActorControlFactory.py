#!/usr/bin/env python3
# @author: Markus Kösters

import unittest

from ..ActorController import ActorController
from ..ActorControlFactory import ActorControlFactory


class test_ActorControlFactory(unittest.TestCase):

    def test_produceActor(self):
        """
        Tests the method `produceActorControlStub` in `ActorControlFactory` to verify
        that it produces an instance of the `ActorController` class.

        :raises AssertionError: If the produced object is not an instance of
                                `ActorController`.

        :return: None
        """
        print(f'!!!!!!!!!!!!!!!!!!!!!!! shit {ActorControlFactory}!!!!!!!!!!!!!!!!!!!!!!11')
        try:
            testObject = ActorControlFactory.produceActorControlStub()
        except Exception as e:
            print(e)
        print(f'!!!!!!!!!!!!!!!!!!!!!!! DAFUQ{type(testObject)}!!!!!!!!!!!!!!!!!!!!!!11')
        self.assertIsInstance(testObject, ActorController)


if __name__ == '__main__':
    unittest.main()
