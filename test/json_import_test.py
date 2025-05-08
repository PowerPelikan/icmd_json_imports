"""loading module to test, unittest for classtesting"""
import unittest
from icmdoutput import json_import

class IcmdDataTest(unittest.TestCase):
    """Testing Class methods"""
    def get_data_test(self):
        """Testing get_data with testdata"""
        data1 = json_import.IcmdData('test/testfiles/susair-var_ni_cu.json')
        data2 = json_import.IcmdData('test/testfiles/tesla_tempStep.json')
        print(data1.get_data())
        print(data2.get_data())



if __name__ == '__main__':
    unittest.main()
