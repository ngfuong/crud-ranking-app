import os


class Config():
    LOCAL_DIR = os.path.dirname(os.path.realpath(__file__)) + '/'
    JSON_PATH = 'data/data.json'
    MENU_COLLAPSED_WIDTH = 50
    MENU_FULL_WIDTH = 150
    TOGGLE_ANIMATION_DURATION = 500
    
    DROP_SHADOW_OFFSET = (5,5)
    DROP_SHADOW_BLUR_RADIUS = 40

    HOME_IMG_SIZE = (980, 700)