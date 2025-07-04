"""loading module to test, unittest for classtesting"""
import sys
import os
# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from icmdoutput import json_import
from icmdoutput.models.solidification import Solidification


if __name__ == '__main__':
    data1 = json_import.JsonData('test/testfiles/susair-var_ni_cu.json')
    data2 = json_import.JsonData('test/testfiles/tesla_tempStep_solidif.json')

    print(data1.get_model())
    print(data2.get_model())
    print(data2.get_datakeys_of_models())

    sol = Solidification('test/testfiles/tesla_tempStep_solidif.json', 'Solidification')
    print(sol.get_sold_reg())
    print(sol.get_phase_fraction())
    print(sol.get_temperature_by_phase_region())
    print(sol.get_percent_solidified_molar())
    print(sol.set_new_temp_by_phase())