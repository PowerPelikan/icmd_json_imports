""" providing json-filetype reading, pandas dataframe datastructure """
import json
import pandas as pd


class IcmdData:
    """Class to convert json file from icmd data into human readable lists and Dataframes"""
    def __init__(self, path: str):
        self.data = self.__import_data(path)
        self.models = self.__get_models()
        self.elements = self.__get_elements()
        self.datakeys = self.__get_datakeys_of_models()

    def __import_data(self, path: str):
        """ open json-file and return it """
        with open(path, 'r', encoding="utf-8") as f:
            try:
                data = json.load(f)
            except OSError:
                print("Cannot open given path")

            return data


    def __get_models(self):

        # Return a list of all used models
        return list(self.data['models'].keys())


    def __get_elements(self):

        df = pd.DataFrame()
        for i in self.models:
            try:
                df[f'{i}'] = self.data['models'][i]['coords']['components']['data']
            except RuntimeError:
                print('Error in finding model elements')

        return df


    def __get_datakeys_of_models(self):

        df = pd.DataFrame()
        # Return calculated model data keys
        for i in self.models:
            try:
                df[f'{i}'] = self.data['models'][i]['data_vars'].keys()
            except KeyError:
                print('Error in finding data keys')
        return df

    def get_data(self) -> pd.DataFrame:
        """Function return data as dataframe"""
        return self.data

    def get_elements(self):
        """Funciton return used elements in given data as list"""
        return self.elements

    def get_datakeys_of_models(self) -> list:
        """Function return all datakey in given data as list"""
        return self.datakeys
