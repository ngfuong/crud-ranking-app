from datetime import datetime
import json

class AnimeItem:
    def __init__(self, id, title, release_date, image=None, rating=None):
        self.id = id
        self.title = title
        self.release_date = release_date
        self.image = image
        self.rating = rating

    def __str__(self):
        return f"{self.title}\t{self.release_date}\t{self.image==True}\t{self.rating}"

JSON_PATH = 'data/data.json'
"""
data.json item example 
    {
        "id": 1,
        "title": "Sousou no Frieren",
        "release_date": "Sep 2023",
        "image": "https://cdn.myanimelist.net/r/100x140/images/anime/1015/138006.webp?s=a7e9bb2976a01ff4edcdede0e7ad15e8",
        "rating": "None"
    },
"""
class AnimeDatabase:
    def __init__(self):
        self.anime_item_list = list()
        self.anime_dict_list = AnimeDatabase.__load_json_data()
        self.anime_title_list = self.get_title_list()
    
    def load_data(self):
        for anime_dict in self.anime_dict_list:
            anime = AnimeItem(id=anime_dict["id"],
                          title=anime_dict["title"],
                          release_date=anime_dict["release_date"],
                          image=anime_dict["image"],
                          rating=anime_dict["rating"])
            self.anime_item_list.append(anime)

    def get_item_by_title(self, anime_title):
        for anime_item in self.anime_item_list:
            if anime_item.title == anime_title:
                return anime_item

    def add_item(self, anime):
        self.anime_data = self.anime_data.append(anime)
        AnimeDatabase.__write_json_data(self.anime_data)

    # def add_new_anime(self):
    #     new_title = input("Input anime title: ")
    #     new_release_date = datetime.strptime(input("Input release date (DD/MM/YYYY):"), "%d/%m/%Y")
    #     new_category = input("Input category: ")
    #     new_score = float(input("Input score: "))

    #     new_anime = Anime(new_title, new_release_date, new_category, new_score)
    #     self.add(new_anime)
    #     print(f"Anime \"{new_anime.title}\" added!")
    #     print(f"List length = {len(self.anime_list)}")

    def delete_by_title(self, title):
        pass

    def edit_by_title(self, title):
        pass

    def __load_json_data():
        with open(JSON_PATH, "r") as json_in:
            anime_dict_list = json.load(json_in)
        return anime_dict_list
    
    def __write_json_data(json_data):
        with open(JSON_PATH, "w") as json_out:
            json.dump(json_data, json_out)
    
    def get_title_list(self):
        titles = [anime["title"] for anime in self.anime_dict_list]
        return titles