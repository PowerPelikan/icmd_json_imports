"""loading module to test, unittest for classtesting"""
import unittest

import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from icmdoutput import json_import

class IcmdDataTest(unittest.TestCase):
    """Testing Class methods"""
    def setUp(self):
        """load testdata"""
        self.data1 = json_import.jsonData('test/testfiles/susair-var_ni_cu.json')
        self.data2 = json_import.jsonData('test/testfiles/tesla_tempStep_solidif.json')

    def test_get_model(self):
        # Testing get_model method
        self.assertEqual(self.data1.get_model(), ['Equilibrium'], "Not the right models")
        self.assertEqual(self.data2.get_model(), ['Temperature Step', 'Solidification'], "Not the right models")


if __name__ == '__main__':
    unittest.main()
