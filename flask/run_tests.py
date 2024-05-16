
import os
import sys

# Add the project directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from tests.test_asn import TestASN
from tests.test_tenant import TestTenant
from tests.test_prefix import TestPrefix
from tests.test_prefix_change import TestPrefixChange, TestPrefixChangeById

from app import db

def nawas_test_suite():
    test_loader = unittest.TestLoader()
    
    test_suite = test_loader.loadTestsFromTestCase(TestTenant)
    test_suite = test_loader.loadTestsFromTestCase(TestASN)
    test_suite = test_loader.loadTestsFromTestCase(TestPrefix)
    test_suite = test_loader.loadTestsFromTestCase(TestPrefixChange)
    test_suite = test_loader.loadTestsFromTestCase(TestPrefixChangeById)


    return test_suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(nawas_test_suite())

