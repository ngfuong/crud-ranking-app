import os


class Config():
    # LOCAL_DIR = os.path.dirname(__file__)
    LOCAL_DIR = os.getcwd()
    UI_DIR = os.path.join(LOCAL_DIR, "ui")

    JSON_PATH = 'data/data.json'
    
    MENU_COLLAPSED_WIDTH = 50
    MENU_FULL_WIDTH = 150
    TOGGLE_ANIMATION_DURATION = 500

    DROP_SHADOW_OFFSET = (5,5)
    DROP_SHADOW_BLUR_RADIUS = 40

    HOME_IMG_SIZE = (980, 700)

    HOME_PAGE_INDEX = 0
    RANK_PAGE_INDEX = 1
    CRUD_MENU_INDEX= 2
    TVSHOW_PAGE_INDEX = 3
    USER_PAGE_INDEX = 4
    SEARCH_ANIME_INDEX = 5

    MICROPHONE_INDEX = 1
    GIF_PATH = "ui\header\loading-20.gif"
