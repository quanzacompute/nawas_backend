
import unittest

from app import app, db
from test import *

class TestAPI(unittest.TestSuite):

    @classmethod
    def suite(cls):
        suite = unittest.TestSuite()
        suite.addTest(unittest.TestLoader.loadTestsFromTestCase(test_tenant.TestTenants))
        suite.addTest(unittest.TestLoader.loadTestsFromTestCase(test_asn.TestASNs))
        suite.addTest(unittest.TestLoader.loadTestsFromTestCase(test_prefix.TestPrefixes))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(TestAPI.suite())

