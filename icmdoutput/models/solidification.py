""" Importing Solidification-Model data from json in Pandas Dataframes"""
import pandas as pd
import numpy as np
from icmdoutput.redunant_data import PhasesAndTemps

class Solidification(PhasesAndTemps):
    ''' Soldification data of a json'''

    def __get_solid_reg(self):
        return self.data['coords']['solidification_region']['data']

    def __get_temp_reg(self):
        return self.data['data_vars']['temperature_by_phase_region']['data']
    
    def __get_perc_sol_mol(self):
        return self.data['data_vars']['percent_solidified_molar_values']['data'][0]

    def get_sold_reg(self):
        ''' Return calculated solidification region'''
        return pd.DataFrame(self.__get_solid_reg())

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

    def get_data_for_scheil_plot(self, tempunit='C'):
        '''Return Dataframe with percent_solidified_molar and temperature_by_phase_region data sorted in a dataframe'''

        phase_region = self.get_temperature_by_phase_region(unit=tempunit)
        
        #melt and clean it in a better dataframe
        pr_melted = phase_region.melt(var_name='Phase Region', value_name='Temperature in '+tempunit)
        pr_clean = pr_melted.dropna(subset=['Temperature in '+tempunit])
        pr_clean = pr_clean[['Temperature in '+tempunit, 'Phase Region']]
        pr_clean = pr_clean.sort_values(by='Temperature in '+tempunit).reset_index(drop=True)

        return pd.concat([self.get_percent_solidified_molar(), pr_clean], axis = 1)