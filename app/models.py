import operator
from datetime import datetime

from app.data_io import load_json_data, write_json_data


class AnimeItem:
    def __init__(self, anime_id, title, release_date, image=None, rating=None):
        self.id = anime_id
        self.title = title
        self.release_date = release_date
        self.image = image
        self.rating = float(rating)

    def __str__(self):
        return f"{self.title}\t{self.release_date}\t{bool(self.image)}\t{self.rating}"

    def update(self, new_data):
        # Empty field is not updated
        for k, v in new_data.items():
            if v:
                setattr(self, k, v)

class AnimeDatabase:
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
    def __init__(self):
        self.anime_item_list = list()
        self.anime_dict_data = load_json_data()
        self.anime_title_list = self.get_title_list()
    
    def item_to_data(self):
        json_data = list()
        for anime in self.anime_item_list:
            json_data.append(anime.__dict__)
        return json_data

    def load_data(self):
        for anime_dict in self.anime_dict_data:
            anime = AnimeItem(anime_id=anime_dict["id"],
                          title=anime_dict["title"],
                          release_date=anime_dict["release_date"],
                          image=anime_dict["image"],
                          rating=anime_dict["rating"])
            self.anime_item_list.append(anime)

    def get_item_by_title(self, anime_title) -> AnimeItem:
        for anime_item in self.anime_item_list:
            if anime_item.title == anime_title:
                return anime_item

    def add_item_from_dict(self, anime_dict):
        anime_dict["id"] = len(self.anime_item_list)
        new_item = AnimeItem(anime_id=anime_dict["id"],
                             title=anime_dict["title"],
                             release_date=anime_dict["release_date"],
                             image=anime_dict["image"],
                             rating=anime_dict["rating"])
        self.anime_item_list.append(new_item)
        self.anime_dict_data.append(anime_dict)
        write_json_data(self.anime_dict_data)
    
    def edit_item_from_dict(self, edit_title, anime_dict: AnimeItem):
        anime_edit = self.get_item_by_title(edit_title)
        anime_edit.update(anime_dict)
        self.anime_dict_data = self.item_to_data()
        write_json_data(self.anime_dict_data)
    
    def delete_item(self, delete_title):
        anime_delete = self.get_item_by_title(delete_title)
        self.anime_item_list.remove(anime_delete)
        self.anime_dict_data = self.item_to_data()
        write_json_data(self.anime_dict_data)
    
    def search_by_title(self, search_title) -> list[AnimeItem]:
        matched_items = []
        for anime_item in self.anime_item_list:
            if search_title in anime_item.title:
                matched_items.append(anime_item)
        return matched_items

    def sort_item_by_rating(self, top=None):
        self.anime_item_list = sorted(self.anime_item_list, 
                                      key=operator.attrgetter('rating'),
                                      reverse=True
                                      )
        if top:
            return self.anime_item_list[top]
    
    def sort_item_by_title(self, top=None):
        self.anime_item_list = sorted(self.anime_item_list, 
                                      key=operator.attrgetter('title')
                                      )
        if top:
            return self.anime_item_list[top]
    
    def sort_item_by_date(self, top=None):
        self.anime_item_list = sorted(self.anime_item_list, 
                                      key=lambda x: format_date(x.release_date),
                                      reverse=True)
        if top:
            return self.anime_item_list[top]
    
    def get_title_list(self):
        titles = [anime["title"] for anime in self.anime_dict_data]
        return titles

def format_date(date_text):
    return datetime.strptime(date_text, '%b %Y')