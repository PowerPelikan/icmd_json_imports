import json

def import_data(path):
    # open json-file and return it    
    with open(path, 'r') as f: 
        data = json.load(f)
        return data

def show_allkeys(data, parent_key=""):
    keys = []
    if isinstance(data, dict):
        for k, v in data.items():
            full_key = f"{parent_key}.{k}" if parent_key else k
            keys.append(full_key)
            keys.extend(show_allkeys(v, full_key))
    elif isinstance(data, list):
        for item in data: 
            keys.extend(show_allkeys(item, parent_key))
    return keys

def show_models(data):
    return list(data['models'].keys())

def show_elements(data, model = ""):

    # take the first model for element getting
    if model == "":
        model = show_models(data)[0]

    return data['models'][model]['coords']['component']['data']