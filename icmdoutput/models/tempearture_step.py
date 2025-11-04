""" Importing TemperatureStep-Model data from json in Pandas Dataframes"""
import pandas as pd
import numpy as np
from icmdoutput.models.equilibrium import Equilibrium

class TemperatureStep(Equilibrium):
    ''' Get data from Temperautre Step model in usefull dataframes'''
    # system_volume, molar_volume, system_densitiy, desitiy, solvus, liquidus, solidus, system_thermal_conductivity, system_compostition, pressure, system_size
    # system_enthalpy, enthalpy, system_electrical_resistivity, electrical_resitivity, surface_tension, dynamic_viscosity, tracer_diffusion_coefficient

