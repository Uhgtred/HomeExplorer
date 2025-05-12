#!/usr/bin/env python3
# Standalone test runner for VideoController tests

import unittest
import sys
import os

# Add the parent directory to the path so we can import our test modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import the test classes
from Video.test_UnitTests.test_VideoController import TestVideoController
from Video.test_UnitTests.test_VideoControllerBuilder import TestVideoControllerBuilder

if __name__ == '__main__':
    # Create a test suite
    suite = unittest.TestSuite()
    
    # Add the test cases
    suite.addTest(unittest.makeSuite(TestVideoController))
    suite.addTest(unittest.makeSuite(TestVideoControllerBuilder))
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print a summary
    print(f"\nRan {result.testsRun} tests")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    # Exit with appropriate code
    sys.exit(len(result.failures) + len(result.errors))