""" Importing Solidification-Model data from json in Pandas Dataframes"""
import pandas as pd
import numpy as np
from icmdoutput.json_import import JsonData

class Solidification(JsonData):
    ''' Soldification data of a json'''
    # TODO: Extract Datakeys: phase_fraction, volume_fraction, composition,
    # solidified_composition, temperature, temperature_by_phase_region,
    # cracking_susceptibility_index, freezing_range, percent_solidified_molar_values,
    # heat, dendride_arm_spacing

    def __init__(self, path, modelename: str, parameter = False):
        super().__init__(path)
        self.modelname = modelename
        self.data = self.data['models'][self.modelname]

        if parameter:
            self.parameter_names= self.__get_parameter_names()
            self.parameter_values = self.__get_parameter_values()

    def __get_parameter_names(self):
        return self.data['data_vars']['parameter_values']['attrs']['units']

    def __get_parameter_values(self):
        return self.data['data_vars']['parameter_values']['data']

    def __get_phase_names(self):
        return self.data['coords']['phase']['data']

    def __get_solid_reg(self):
        return self.data['coords']['solidification_region']['data']

    def __get_temperatures(self):
        return self.data['data_vars']['temperature']['data']

    def __get_temp_reg(self):
        return self.data['data_vars']['temperature_by_phase_region']['data']
    
    def __get_perc_sol_mol(self):
        return self.data['data_vars']['percent_solidified_molar_values']['data'][0]

    def get_phase_names(self):
        '''Return all calulated phases'''

        return pd.DataFrame(self.__get_phase_names())
    
    def get_sold_reg(self):
        ''' Return calculated solidification region'''

        return pd.DataFrame(self.__get_solid_reg())

    def get_phase_fraction(self, phase_unit = 'mole', temp_unit = 'C' ):
        ''' Return Dataframme with Phasefraction in mole or mass'''

        if phase_unit == 'mole':
            phase_values = np.array(
                self.data['data_vars']['phase_fraction']['data']
                )[0,:,:,0]
        else:
            phase_values = np.array(
                self.data['data_vars']['phase_fraction']['data']
                )[0,:,:,0]

        temps = self.get_temperatures(temp_unit)
        phase = pd.DataFrame(phase_values, columns=self.__get_phase_names())

        return pd.concat([temps, phase], axis=1)

    def get_volume_fraction(self):
        """ Return Dataframe with Volume Fractions"""

        volume_values = np.array(
            self.data['data_vars']['volume_fraction']['data']
        )
        return pd.DataFrame(volume_values, self.__get_phase_names)
    
    def get_temperatures(self, unit = "C"):
        """ Return Temperature values"""

        match unit:
            case 'C':
                temperature_values = np.array(self.__get_temperatures())[0,:,0]
            case 'F':
                temperature_values = np.array(self.__get_temperatures())[0,:,1]
            case 'K':
                temperature_values = np.array(self.__get_temperatures())[0,:,2]

        return pd.DataFrame(temperature_values, columns=['Temperature in ' + unit])
    
    def get_temperature_by_phase_region(self, unit = 'C'):
        """ Return Temperature by phase region values"""

        match unit:
            case 'C':
                temperature_values = np.array(self.__get_temp_reg())[0,:,:,0]
            case 'F':
                temperature_values = np.array(self.__get_temp_reg())[0,:,:,1]
            case 'K':
                temperature_values = np.array(self.__get_temp_reg())[0,:,:,2]

        return pd.DataFrame(temperature_values, columns=self.__get_solid_reg())

    def get_percent_solidified_molar(self):
        ''' Return Percetage of solidification'''

        return pd.DataFrame(self.__get_perc_sol_mol(), columns=['Percent solidified molar'])
    