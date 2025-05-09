"""loading module to test, unittest for classtesting"""
import sys
import os
# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from icmdoutput import json_import


if __name__ == '__main__':
    data1 = json_import.IcmdData('test/testfiles/susair-var_ni_cu.json')
    print(data1.get_datakeys_of_models())
    data2 = json_import.IcmdData('test/testfiles/tesla_tempStep_solidif.json')
    print(data2.get_datakeys_of_models())
