import pandas as pd
import numpy as np
from icmdoutput.models.solidification import Solidification

class Scheil(Solidification):

    def __init__(self, path: str, modelname: str, parameter = False):
        super().__init__(path, modelname, parameter)

        self.temp_by_phase = self.__new_temp_by_phase()


    def __get_present_phases(self, row, threshhold):
        df = self.get_phase_fraction()
        phase_columns = [col for col in df.columns if col != 'Temperature' and col != 'SOLID']
        return [phase for phase in phase_columns if row[phase]>threshhold]

    def __new_temp_by_phase(self, threshhold = 1e-6):
        ''' Returns a better/other Phase Region DataFrame, if the ICMD outptu is wierd '''

        phase_region = self.get_phase_fraction().apply(lambda row: self.__get_present_phases(row, threshhold), axis=1)
        df_present = pd.DataFrame({
            "Temperature": np.ravel(self.get_temperatures()),
            "Phase_region": np.ravel(phase_region.apply(lambda phase: '+'.join(sorted(phase))))
        })
    
        return df_present

    def get_temp_by_phase(self):

        return self.temp_by_phase
    
    def get_scheil_df(self):

        return pd.concat([self.get_percent_solidified_molar(), self.temp_by_phase], axis=1)
