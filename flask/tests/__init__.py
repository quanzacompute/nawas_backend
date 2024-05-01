
import unittest

import test_tenant
import test_asn
import test_prefix

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader.loadTestsFromTestCase(test_tenant.TestTenants))
    suite.addTest(unittest.TestLoader.loadTestsFromTestCase(test_asn.TestASNs))
    suite.addTest(unittest.TestLoader.loadTestsFromTestCase(test_prefix.TestPrefixes))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

