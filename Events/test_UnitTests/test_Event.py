#!/usr/bin/env python3
# @author: Markus Kösters

import unittest

from Events import EventManager

class MyEvent(unittest.TestCase):

    var = None

    def myFunction(self, arg):
        if arg:
            self.var = arg

class test_Event(unittest.TestCase):

    eventManager = EventManager()
    myEvent = MyEvent()

    def test_ProduceEvent(self):
        self.eventManager.produceEvent('testEvent')
        self.assertIn('testEvent', self.eventManager.getEventsList)

    def test_subscribe(self):
        event = self.eventManager.produceEvent('testEvent')
        event.subscribe(self.myEvent.myFunction)
        self.assertTrue(self.myEvent.myFunction in event._Event__subscribers)

    def test_notifySubscribers(self):
        event = self.eventManager.produceEvent('testEvent')
        event.subscribe(self.myEvent.myFunction)
        event.notifySubscribers('Hello World!')
        self.assertEqual(self.myEvent.var, 'Hello World!')


if __name__ == '__main__':
    unittest.main()
