"""loading module to test, unittest for classtesting"""
import sys
import os
# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from icmdoutput import json_import
from icmdoutput.models.solidification import Solidification
from icmdoutput.redundant_data import PhasesAndTemps
from icmdoutput.models.equilibrium import Equilibrium
from icmdoutput.models.tempearture_step import TemperatureStep


if __name__ == '__main__':
    data1 = json_import.JsonData('test/testfiles/susair-var_ni_cu.json')
    data2 = json_import.JsonData('test/testfiles/tesla_tempStep_solidif.json')

    print(data1._extract_models())
    print(data2._extract_models())
    print(data2.get_datakeys_of_models())

    sol = Solidification('test/testfiles/tesla_tempStep_solidif.json', 'Solidification')
    print(sol.get_solid_regions())
    print(sol.get_phase_fraction())
    print(sol.get_temperature_by_phase_region())
    print(sol.get_percent_solidified_molar())

    comp = PhasesAndTemps('test/testfiles/tesla_tempStep_solidif.json', 'Solidification')
    print(comp.get_phase_names())
    print(comp.get_composition(['AL2SI2SR', 'C16_A2B', 'Q_PHASE']))
    print(comp.get_composition())

    equi = json_import.JsonData('test/testfiles/equi.json')
    print(equi.get_datakeys_of_models())

    equi = Equilibrium('test/testfiles/equi.json', 'Equilibrium')
    print(equi.get_molar_volume())
    print(equi.get_pressure())
    print(equi.get_thermal_conductivity())
    print(equi.get_system_size_mass())
    print(equi.get_system_size_moles())
    print(equi.get_system_size_volume())
    print(equi.get_enthalpy())
    print(equi.get_system_electrical_resistivity())
    print(equi.get_electrical_resistivity())
    print(equi.get_surface_tension())
    print(equi.get_dynamic_viscosity())
    print(equi.get_tracer_diffusion_coefficient())
    print(equi.get_gradient_component().values[:,0])
    #print(equi.get_chemical_diffusion_coefficient())

    tempStep = TemperatureStep('test/testfiles/tesla_tempStep_solidif.json', 'Temperature Step')
    print(tempStep.get_phase_fraction())
    print(tempStep.get_volume_fraction())