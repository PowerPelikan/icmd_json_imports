from icmdoutput import json_import

import unittest

class TESTicmd_data(unittest.TestCase):
    def TEST_get_data(self):
        data1 = json_import.icmd_data('test/testfiles/susair-var_ni_cu.json')
        data2 = json_import.icmd_data('test/testfiles/tesla_tempStep.json')
        print(data1.get_data())
        print(data2.get_data())



if __name__ == '__main__':
    unittest.main()
