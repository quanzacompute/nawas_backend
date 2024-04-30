
import unittest

from app import app, db
from test import *

class TestAPI(unittest.TestSuite)

    @classmethod
    def suite(cls):
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(TestTenants))
        suite.addTest(unittest.makeSuite(TestASNs))
        suite.addTest(unittest.makeSuite(TestPrefixes))

if __name __ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(TestAPI.suite())

