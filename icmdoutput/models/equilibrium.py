import pandas as pd
import numpy as np
from icmdoutput.redundant_data import PhasesAndTemps


class Equilibrium(PhasesAndTemps):
    """Access equilibrium model data such as density, enthalpy, viscosity, etc."""

    # --- Internal data extraction helpers ----------------------------------

    def _get_array(self, *path, index=None):
        """Safely navigate nested keys and optionally extract index."""
        data = self.data
        for p in path:
            data = data[p]
        arr = np.array(data)
        if index is not None:
            return arr[index]
        return arr

    # --- Individual variables ----------------------------------------------

    def _get_molar_volume(self):
        return self._get_array("data_vars", "molar_volume", "data", index=0)

    def _get_system_density(self):
        return self._get_array("data_vars", "system_density", "data")

    def _get_density(self):
        return self._get_array("data_vars", "density", "data", index=0)

    def _get_pressure(self):
        return self._get_array("data_vars", "pressure", "data")

    def _get_thermal_conductivity(self):
        return self._get_array("data_vars", "thermal_conductivity", "data", index=0)

    def _get_system_size(self, key):
        return self._get_array("data_vars", key, "data")

    def _get_enthalpy(self):
        return self._get_array("data_vars", "enthalpy", "data", index=0)

    def _get_system_enthalpy(self):
        return self._get_array("data_vars", "system_enthalpy", "data")

    def _get_electrical_resistivity(self):
        return self._get_array("data_vars", "electrical_resistivity", "data", index=0)

    def _get_system_electrical_resistivity(self):
        return self._get_array("data_vars", "system_electrical_resistivity", "data")

    def _get_surface_tension(self):
        return self._get_array("data_vars", "surface_tension", "data", index=0)

    def _get_dynamic_viscosity(self):
        return self._get_array("data_vars", "dynamic_viscosity", "data", index=0)

    def _get_tracer_diffusion_coefficient(self):
        return self._get_array("data_vars", "tracer_diffusion_coefficient", "data", index=0)

    def _get_chemical_diffusion_coefficient(self):
        return self._get_array("data_vars", "chemical_diffusion_coefficient", "data", index=0)

    # --- Public accessors returning DataFrames -----------------------------

    def get_molar_volume(self):
        phases = self.get_phase_names_df().squeeze()
        return pd.DataFrame([self._get_molar_volume()], columns=phases)

    def get_system_density(self):
        return pd.DataFrame(self._get_system_density(), columns=["System density (g/cm³)"])

    def get_density(self):
        phases = self.get_phase_names_df().squeeze()
        return pd.DataFrame([self._get_density()], columns=phases)

    def get_pressure(self, unit="Pa"):
        pressure_map = {"Pa": 0, "ksi": 1, "atm": 2, "bar": 3}
        if unit not in pressure_map:
            raise ValueError(f"Unsupported pressure unit: {unit}")
        val = self._get_pressure()[0, pressure_map[unit]]
        return pd.DataFrame([[val]], columns=[f"Pressure ({unit})"])

    def get_thermal_conductivity(self):
        phases = self.get_phase_names_df().squeeze()
        return pd.DataFrame([self._get_thermal_conductivity()], columns=phases)

    def get_system_size_mass(self):
        return pd.DataFrame(self._get_system_size("system_size_mass"), columns=["Mass (g)"])

    def get_system_size_moles(self):
        return pd.DataFrame(self._get_system_size("system_size_moles"), columns=["Moles (mol)"])

    def get_system_size_volume(self):
        return pd.DataFrame(self._get_system_size("system_size_volume"), columns=["Volume (m³)"])

    def get_system_enthalpy(self):
        return pd.DataFrame(self._get_system_enthalpy(), columns=["System enthalpy (J)"])

    def get_enthalpy(self):
        phases = self.get_phase_names_df().squeeze()
        return pd.DataFrame([self._get_enthalpy()], columns=phases)

    def get_system_electrical_resistivity(self):
        return pd.DataFrame(
            self._get_system_electrical_resistivity(),
            columns=["System resistivity (Ω·m)"],
        )

    def get_electrical_resistivity(self):
        phases = self.get_phase_names_df().squeeze()
        return pd.DataFrame([self._get_electrical_resistivity()], columns=phases)

    def get_surface_tension(self):
        phases = self.get_phase_names_df().squeeze()
        return pd.DataFrame([self._get_surface_tension()], columns=phases)

    def get_dynamic_viscosity(self):
        phases = self.get_phase_names_df().squeeze()
        return pd.DataFrame([self._get_dynamic_viscosity()], columns=phases)

    def get_tracer_diffusion_coefficient(self):
        phases = self.get_phase_names_df().squeeze()
        elements = self.get_elements().squeeze()
        return pd.DataFrame(self._get_tracer_diffusion_coefficient(), index=phases, columns=elements)

    def get_chemical_diffusion_coefficient(self):
        phases = self.get_phase_names_df().squeeze()
        gradients = self.get_gradient_component().squeeze()
        return pd.DataFrame(self._get_chemical_diffusion_coefficient(), index=phases, columns=gradients)
    