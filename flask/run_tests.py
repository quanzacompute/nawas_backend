
import os
import sys

# Add the project directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from tests.test_asn import TestASN, TestASNAPI
from tests.test_tenant import TestTenant, TestTenantAPI
from tests.test_prefix import TestPrefix, TestPrefixAPI
from tests.test_prefix_change import TestPrefixChange, TestPrefixChangeAPICall

from app import db

def nawas_test_suite():
    test_loader = unittest.TestLoader()
    
    test_suite = test_loader.loadTestsFromTestCase(TestTenant)
    test_suite = test_loader.loadTestsFromTestCase(TestTenantAPI)
    test_suite = test_loader.loadTestsFromTestCase(TestASN)
    test_suite = test_loader.loadTestsFromTestCase(TestASNAPI)
    test_suite = test_loader.loadTestsFromTestCase(TestPrefix)
    test_suite = test_loader.loadTestsFromTestCase(TestPrefixAPI)
    test_suite = test_loader.loadTestsFromTestCase(TestPrefixChange)
    test_suite = test_loader.loadTestsFromTestCase(TestPrefixChangeAPICall)


    return test_suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(nawas_test_suite())

