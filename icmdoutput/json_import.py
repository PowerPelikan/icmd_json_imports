""" providing json-filetype reading, pandas dataframe datastructure """
import os
import json
import pandas as pd


class jsonData:
    """Class to convert json file from icmd data into human readable lists and Dataframes"""

    def __init__(self, path: str):

        if not os.path.isfile(path):
            raise ValueError(path + " does not exist")

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
        """Return a list of all used models"""
        return list(self.data['models'].keys())


    def __get_elements(self):
        """Return a list of all used elements"""

        list_of_data = []
        for i in self.models:
            try:
                list_of_data.append(self.data['models'][i]['coords']['component']['data'])
            except RuntimeError:
                print('Error in finding model elements')
        df = pd.DataFrame(list_of_data, index=self.models).T

        return df


    def __get_datakeys_of_models(self):

        """ Return calculated model data keys """
        list_of_data = []
        for i in self.models:
            try:
                list_of_data.append(self.data['models'][i]['data_vars'].keys())
            except KeyError:
                print('Error in finding data keys')
        df = pd.DataFrame(list_of_data, index=self.models).T

        return df

    def __get_data_from_key(self, datakey: str, model: str):
        """Function return values under given datakey and model"""

        try:
            self.is_model(model)
            self.is_datakey(datakey, model)
        except ValueError:
            return False

        return self.data["models"][model]["data_vars"][datakey].values

    def get_model(self):
        """Function return used models"""
        return self.models

    def get_data(self):
        """Function return data as loaded json"""
        return self.data

    def get_elements(self):
        """Funciton return used elements in given data as list"""
        return self.elements

    def get_datakeys_of_models(self) -> list:
        """Function return all datakey in given data as list"""
        return self.datakeys

    def is_model(self, model: str) -> bool:
        """Function chekcks, if given model in given data"""
        if model in self.models:
            return True
        raise ValueError("Model is not in given data")

    def check_datakeys(self, datakey: str, *model ):
        """Function checks if given datakey is in model"""

        if not model:
            model = self.models

        for m in model:
            self.is_model(m)
            if datakey in self.datakeys[m].values:
                print(datakey + "is in " + m)
            else:
                print("Not in " + m)

    def is_datakey(self, datakey: str, model: str) -> bool:
        """Function return, if given datakey is in given model"""

        if datakey in self.datakeys[model].values:
            return True
        raise ValueError("Datakey " + datakey + " is not in model " + model)

    def get_data_from_keys(self, datakeys: list, model):
        """Function return values of given datakeys and models in a dataframe"""
        list_of_data = []
        for d in datakeys:
            list_of_data.append(self.__get_data_from_key(d, model).values)

        df = pd.DataFrame(list_of_data, index=datakeys).T

        return df
