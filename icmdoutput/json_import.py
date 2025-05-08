import json
import pandas as pd


class icmd_data:
    def __init__(self, path: __path__, **kwargs):
        try:
            self.data = self.__import_data(path)
        except: 
            print("No valid path given")

        try:
            self.models = self.__get_models()
            self.elements = self.__get_elements()
            self.datakeys = self.__get_datakeys_of_models()
        except: 
            print("Error in loading file data")

    def __import_data(path):
        # open json-file and return it    
        with open(path, 'r') as f: 
            data = json.load(f)
            return data

    def __get_models(self):

        # Return a list of all used models
        return list(self.data['models'].keys())


    def __get_elements(self):

        df = pd.DataFrame()
        for i in self.models:
            try:
                df[f'{i}'] = self.data['models'][i]['coords']['components']['data']
            except:
                print('Error in finding model elements')


        return df


    def __get_datakeys_of_models(self):

        df = pd.DataFrame()
        # Return calculated model data keys
        for i in self.models:
            try: 
                df[f'{i}'] = self.data['models'][i]['data_vars'].keys()
            except:
                print('Error in finding data keys')
    
    def get_data(self):
        return self.data

    def get_elements(self):
        return self.elements
    
    def get_datakeys_of_models(self):
        return self.datakeys