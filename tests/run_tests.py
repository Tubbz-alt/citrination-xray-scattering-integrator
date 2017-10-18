from __future__ import print_function
import unittest
import os

import paws.api
import test_convert

runner = unittest.TextTestRunner(verbosity=3)

print('======================================================================')
print('--- testing convert() ---'+os.linesep)
convert_tests = unittest.TestSuite()
convert_tests.addTest(test_convert.TestIntegrator('test'))
runner.run(convert_tests)
print(os.linesep+'--- done testing convert() ---')
print('======================================================================')


