from datetime import datetime

class Anime:
    def __init__(self, title, release_date, category, score):
        self.title = title
        self.release_date = release_date
        self.category = category
        self.score = score

    def __str__(self):
        return f"{self.title}\t {self.release_date}\t"

class AnimeList:
    def __init__(self):
        self.anime_list = list()
    
    def list_anime(self):
        # Loop self.anime_list: print(anime)
        for anime in self.anime_list:
            print(anime)

    def add(self, anime):
        self.anime_list.append(anime)

    def add_anime(self):
        new_title = input("Input anime title: ")
        new_release_date = datetime.strptime(input("Input release date (DD/MM/YYYY):"), "%d/%m/%Y")
        new_category = input("Input category: ")
        new_score = float(input("Input score: "))

        new_anime = Anime(new_title, new_release_date, new_category, new_score)
        self.add(new_anime)
        print(f"Anime \"{new_anime.title}\" added!")
        print(f"List length = {len(self.anime_list)}")

    def delete_by_title(self, title):
        pass

    def edit_by_title(self, title):
        pass