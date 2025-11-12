""" providing json-filetype reading, pandas dataframe datastructure """
import os
import json
import pandas as pd


class JsonData:
    """Class to convert json file from icmd data into human readable lists and Dataframes"""

    def __init__(self, path: str):
        if not os.path.isfile(path):
            raise FileNotFoundError(f"{path} does not exist")
        self.data = self._import_data(path)
        self.elememts = self._extract_elements()
        self.models = self._extract_models()

    def _import_data(self, path: str) -> dict:
        """Open json-file and return the loaded data"""
        try:
            with open(path, "r", encoding='utf-8') as f:
                return json.load(f)
        except OSError as e:
            raise IOError(f"Cannot open or read '{path}'") from e


    def _extract_models(self) -> list:
        """Return a list of all used models"""
        return list(self.data.get("models", {}).keys())

    def _extract_elements(self) -> pd.DataFrame:
        """Return a list of all used elements"""
        rows = []
        for model in self._extract_models():
            try:
                rows.append(self.data['models'][model]['coords']['component']['data'])
            except KeyError:
                print(f"Faild to extract elements for model '{model}'")
        return pd.DataFrame(rows, index=self._extract_models()).T


    def _extract_datakeys(self) -> pd.DataFrame:
        """ Return calculated model data keys """
        keys = []
        for model in self._extract_models():
            try:
                keys.append(self.data['models'][model]['data_vars'].keys())
            except KeyError:
                print(f"Missing data keys in model '{model}'")
        return pd.DataFrame(keys, index=self._extract_models()).T

    def _get_data_var(self, data_key: str, model: str):
        self._validate_model(model)
        self._validate_datakey(data_key, model)
        return self.data['models'][model]['data_vars'][data_key]

    def get_models(self) -> list:
        """Function return used models list"""
        return self.models

    def get_data(self) -> dict:
        """Function return data as dict"""
        return self.data

    def get_elements(self) -> pd.DataFrame:
        """Funciton return used elements in given data as list"""
        return self.elememts

    def get_datakeys_of_models(self) -> pd.DataFrame:
        """Function return all datakey in given data as list"""
        return self._extract_datakeys()

    def _validate_model(self, model: str) -> bool:
        """Function chekcks, if given model in given data"""
        if model not in self._extract_models():
            raise ValueError(f"Model '{model}' is not in data")

    def _validate_datakey(self, data_key: str, model:str) -> bool:
        """Function checks if given datakey is in model"""
        if data_key not in self._extract_datakeys()[model].values:
            raise ValueError(f"Datakey '{data_key}' not found in '{model}'")
        return True

    def get_data_from_keys(self, data_keys: list, model: str) -> pd.DataFrame:
        """Function return values of given datakeys and models in a dataframe"""
        values = [self._get_data_var(k, model) for k in data_keys]
        return pd.DataFrame(values, index=data_keys).T

class SingleModel(JsonData):
    '''Access data from a single model within the JSON file'''

    def __init__(self, path: str, model_name: str):
        super().__init__(path)
        self._validate_model(model_name)
        self.data = self.data['models'][model_name]
        self.model_name = model_name

    def _get_gradient_component(self):
        return self.data['coords']['gradient_component']['data']
    
    def get_gradient_component(self) -> pd.DataFrame:
        '''Get dataframe with gradient components'''
        return pd.DataFrame(self._get_gradient_component())

    def get_parameter_values(self):
        '''Return used Parameter values if used'''
        return self.data['data_vars']['parameter_values']['data']

    def get_parameter(self):
        '''Return used Parameter if used'''
        return self.data['coords']['parameter']['data']
