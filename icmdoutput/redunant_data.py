'''Define Phasefraction, volume fraction and temperatture values for multiple models'''
import numpy as np
import pandas as pd
from .json_import import SingleModel

class PhasesAndTemps(SingleModel):
    '''Get Phasefraction, Volumefraction and Temperature from Models'''

    def get_phase_names(self):
        return self.data['coords']['phase']['data']

    def __get_temperatures(self, unit):
        try:
            temps = self.data['data_vars']['temperature_values']['data'][0]
        except KeyError:
            temps = self.data['data_vars']['temperature']['data'][0]

        match unit: 
            case 'C':
                return [elem[0] for elem in temps]
            case 'K':
                return [elem[1] for elem in temps]
            case 'F':
                return [elem[2] for elem in temps]
            
    def __get_composition(self, phase, unit, phaselist):
        try:
            phase_index = phaselist.isin([phase]).any(axis=1).idxmax()
        except KeyError:
            print(phase + ' is not in Data')

        try:
            data = self.data['data_vars']['composition']['data'][0]
        except KeyError:
            data = self.data['data_vars']['phase_composition']['data'][0]
        
        if unit == 'mass':
            comp = [
                [
                    [elem[1] for elem in row]
                    for row in block
                ]
                for block in data
            ]
            return [elem[phase_index] for elem in comp]

        comp = [
            [
                [elem[0] for elem in row]
                for row in block
            ]
            for block in data
        ]
        return [elem[phase_index] for elem in comp]

    def __get_elements(self):
        return self.data['coords']['component']['data']

    def __get_volume_fraction(self):
        return self.data['data_vars']['volume_fraction']['data'][0]

    def __get_phase_fraction(self, unit, parameter):
        if parameter:
            data = self.data['data_vars']['phase_fraction']['data']
            if unit == 'mass':
                return [
                    [
                    [elem[1] for elem in row]
                    for row in block
                ]
                for block in data
                ]
            else:
                return [
                    [
                    [elem[0] for elem in row]
                    for row in block
                ]
                for block in data
                ]
            
        data = self.data['data_vars']['phase_fraction']['data'][0]

        if unit == 'mass':
            return [
                [elem[1] for elem in plane]
                for plane in data
            ]

        return [
            [elem[0] for elem in plane]
            for plane in data
        ]

    def get_components_df_complete(self):
        return pd.DataFrame(self.data['attrs']['input_dict']['composition']['components'])
    
    def get_components(self, exclude = []):

        df = self.get_components_df_complete()

        if exclude:
            df = df[df['name'] != exclude]
        
        res = pd.DataFrame({
            row['name']: row['samples'] for _, row in df.iterrows()
        })

        return res


    def get_composition(self, phases= None, unit= 'mole' ):
        ''' Return Dataframe with compostion of given phases over the temperature'''

        phaselist = self.get_phase_names_df()
        if phases is None:
            phases = self.get_phase_names()

        print(phases)

        col = self.__get_elements()
        df = pd.DataFrame(columns=col)
        for pha in phases:
            print(pha)
            comp = self.__get_composition(pha, unit, phaselist)
            df = pd.concat([df, pd.DataFrame(comp, columns= col ,index=[pha]*len(comp))], axis=0)
        return df

    def get_phase_names_df(self):
        '''Return a Dataframe with all calculated Phases'''
        return pd.DataFrame(self.get_phase_names())

    def get_elements(self):
        '''Return Dataframe with all Elements'''
        return pd.DataFrame(self.__get_elements())

    def get_phase_fraction(self, phase_unit = 'mole', temp_unit = 'C', parameter = False):
        ''' Return Dataframme with Phasefraction in mole or mass'''
        phase_values = self.__get_phase_fraction(phase_unit, parameter)

        temps = self.get_temperatures(temp_unit)

        if parameter: 
            list_df = []
            components = self.get_components()
            for pa, pf in zip(components.values, phase_values):
                pa_df = pd.DataFrame([pa]*temps.size, columns=self.get_components().keys())
                pf_df = pd.DataFrame(pf, columns=self.get_phase_names())
                df = pd.concat( [pa_df, temps, pf_df], axis=1)

                list_df.append(df)
            return pd.concat(list_df, ignore_index=True)
            
        temps = self.get_temperatures(temp_unit)
        phase = pd.DataFrame(phase_values, columns=self.get_phase_names())

        return pd.concat([temps, phase], axis=1)

    def get_volume_fraction(self, temp_unit = 'C'):
        """ Return Dataframe with Volume Fractions"""

        volume_values = self.__get_volume_fraction()
        temps = self.get_temperatures(temp_unit)
        phase = pd.DataFrame(volume_values, columns=self.get_phase_names())

        return pd.concat([temps, phase], axis=1)

    def get_temperatures(self, unit = "C"):
        """ Return Temperature values"""

        return pd.DataFrame(self.__get_temperatures(unit), columns=['Temperature in ' + unit])
