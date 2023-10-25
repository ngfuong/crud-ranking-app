import json
from modules.ui_config import UIConfig


def load_json_data():
    anime_dict_data = list()
    with open(UIConfig.JSON_PATH, "r") as json_in:
        json_data = json.load(json_in)
    anime_dict_data.extend(json_data)
    return anime_dict_data

def write_json_data(json_data):
    with open(UIConfig.JSON_PATH, "w") as json_out:
        json.dump(json_data, json_out)
    
    