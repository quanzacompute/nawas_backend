
import unittest
from app import app, db

def nawas_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(nawas_test_suite())

