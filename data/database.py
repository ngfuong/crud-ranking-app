import json
from models import Anime

class Database:
    def create():
        with open("data.json", "r") as data_file:
            data_str = json.loads(data_file)
    
    def add_record():
        pass
        