#!/usr/bin/env python3
# @author: Markus Kösters
import time
import unittest

from Runners import ThreadRunner


def testTask(*args):
    print(f"Testing {args}")
    time.sleep(5)


class MyTestCase(unittest.TestCase):
    testRunner = ThreadRunner()

    def test_threadOpening(self):
        self.testRunner.addTask(testTask, ['test', 'test2'])
        assert 'testTask_thread' in self.testRunner._ThreadRunner__threads


if __name__ == '__main__':
    unittest.main()
