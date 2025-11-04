import pandas as pd
import numpy as np
from icmdoutput.redunant_data import PhasesAndTemps

class Equilibrium(PhasesAndTemps):
    '''Get data from Equilibrium model'''

    def __get__molar_volume(self):
        return np.array(
            self.data['data_vars']['molar_volume']['data']
            )[0,:]
    
    def __get_system_desity(self):
        return self.data['data_vars']['system_density']['data']
    
    def __get_density(self):
        return self.data['data_vars']['density']['data'][0]

    def __get_pressure(self):
        return self.data['data_vars']['pressure']['data']
    
    def __get_thermal_conductivity(self):
        return self.data['data_vars']['thermal_conductivity']['data'][0]
    
    def __get_system_size_mass(self):
        return self.data['data_vars']['system_size_mass']['data']
    
    def __get_system_size_moles(self):
        return self.data['data_vars']['system_size_moles']['data']
    
    def __get_system_size_volume(self):
        return self.data['data_vars']['system_size_volume']['data']
    
    def __get_system_enthalpy(self):
        return self.data['data_vars']['system_enthalpy']['data']
    
    def __get_enthalpy(self):
        return self.data['data_vars']['enthalpy']['data'][0]

    def __get_system_electrical_resistivity(self):
        return self.data['data_vars']['system_electrical_resistivity']['data']
    
    def __get_electrical_resistivity(self):
        return self.data['data_vars']['electrical_resistivity']['data'][0]

    
    def __get_surface_tension(self):
        return self.data['data_vars']['surface_tension']['data'][0]
    
    def __get_dynamic_viscosity(self):
        return self.data['data_vars']['dynamic_viscosity']['data'][0]
    
    def __get_tracer_diffusion_coefficient(self):
        return self.data['data_vars']['tracer_diffusion_coefficient']['data'][0]

    def __get_chemical_diffusion_coefficient(self):
        return self.data['data_vars']['chemical_diffusion_coefficient']['data'][0]

    def get_molar_volume(self):
        '''Return molar volume from all phases as dataframe'''

        phaselist = np.array(self.get_phase_names_df())[:,0]
        return pd.DataFrame([self.__get__molar_volume()], columns=phaselist) 
    
    def get_system_desnity(self):
        '''Return system density in a dataframe'''

        return pd.DataFrame(self.__get_system_desity(), columns=['g/cm^3'])
        
    def get_density(self):
        '''Return denstity of the phases'''

        phaselist = self.get_phase_names_df().values[:,0]
        return pd.DataFrame([self.__get_density()], columns=phaselist)

    def get_pressure(self, unit='Pa'):
        '''Return pressure as a Dataframe'''
        
        match unit:
            case 'Pa':
                return pd.DataFrame([np.array(
                    self.__get_pressure())[0,0]], columns=['Pressure in Pa'])
            case 'ksi':
                return pd.DataFrame([np.array(
                    self.__get_pressure())[0,1]], columns=['Pressure in ksi'])
            case 'atm': 
                return pd.DataFrame([np.array(
                    self.__get_pressure())[0,2]], columns=['Pressure in atm'])
            case 'bar': 
                return pd.DataFrame([np.array(
                    self.__get_pressure())[0,3]], columns=['Pressure in bar'])

    def get_thermal_conductivity(self):
        '''Returns a Dataframe with the thermal conductivity of all phases'''

        phaselist = self.get_phase_names_df().values[:,0]
        return pd.DataFrame([self.__get_thermal_conductivity()], columns=phaselist)

    def get_system_size_mass(self):
        '''Return system size mass in dataframe'''

        return pd.DataFrame(self.__get_system_size_mass(), columns=['System size mass in g'])
        
    def get_system_size_moles(self):
        '''Return system size moles in dataframe'''

        return pd.DataFrame(self.__get_system_size_moles(), columns=['System size moles in mol'])

    def get_system_size_volume(self):
        '''Return system size volume in dataframe'''

        return pd.DataFrame(self.__get_system_size_volume(), columns=['System size volume in m^3'])

    def get_system_enthalpy(self):
        '''Return system enthalpy in dataframe'''

        return pd.DataFrame(self.__get_system_enthalpy(), columns=['System enthalpy in J'])

    def get_enthalpy(self):
        '''Returns a Dataframe with the enthalpy of all phases'''

        phaselist = self.get_phase_names_df().values[:,0]
        return pd.DataFrame([self.__get_enthalpy()],columns=phaselist)

    def get_system_electrical_resistivity(self):
        '''Return a datafarme with system electrical resistivity '''

        return pd.DataFrame(self.__get_system_electrical_resistivity(), columns=['System electrical resistivity in Ohm m'])

    def get_electrical_resistivity(self):
        '''Returns a Dataframe with the electrical resisitivity of all phases'''

        phaselist = self.get_phase_names_df().values[:,0]
        return pd.DataFrame([self.__get_electrical_resistivity()],columns=phaselist)

    def get_surface_tension(self):
        '''Returns a Dataframe with the electrical resisitivity of all phases'''

        phaselist = self.get_phase_names_df().values[:,0]
        return pd.DataFrame([self.__get_surface_tension()],columns=phaselist)

    def get_dynamic_viscosity(self):
        '''Returns a Dataframe with the dynamic viscosity of all phases'''

        phaselist = self.get_phase_names_df().values[:,0]
        return pd.DataFrame([self.__get_dynamic_viscosity()],columns=phaselist)

    def get_tracer_diffusion_coefficient(self):
        '''Returns a dataframe with dynamic viscosity over all phases and elements'''

        phaselist = self.get_phase_names_df().values[:,0]
        elements = self.get_elements().values[:,0]
        tdc = self.__get_tracer_diffusion_coefficient()
        return pd.DataFrame(tdc, index=phaselist, columns=elements)
    
    def get_chemical_diffusion_coefficent(self):

        phaselist = self.get_phase_names_df().values[:,0]
        gradient_components = self.get_gradient_component().values[:,0]

        return pd.DataFrame(self.__get_chemical_diffusion_coefficient(), columns=gradient_components, index=phaselist)