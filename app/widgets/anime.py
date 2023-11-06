from PyQt6.uic import load_ui
from PyQt6.QtGui import QPixmap, QColorConstants
from PyQt6.QtWidgets import QWidget, QLabel, QGraphicsDropShadowEffect

from config import Config
from ui.anime_column_ui import Ui_AnimeColumn
from app.models import AnimeItem


class AnimeItemWidget(QWidget, Ui_AnimeColumn):
    UI_LOCATION = f"{Config.LOCAL_DIR}/ui/anime_column.ui"
    STYLE_LOCATION = f"{Config.LOCAL_DIR}/ui/style_anime.qss"
    def __init__(self, anime:AnimeItem):
        QWidget.__init__(self)
        try:
            self.ui = Ui_AnimeColumn()
            self.ui.setupUi(self)
        except NameError:
            self.ui = load_ui.loadUi(self.UI_LOCATION)

        with open(self.STYLE_LOCATION, "r") as style_file:
            style_config = style_file.read()
        self.setStyleSheet(style_config)

        self.anime = anime
        Animation.drop_shadow_on_hovered(self, self)
        self.display_description()

    def display_description(self):
        description_text = self.anime.release_date + "\n" \
                            + "Rating: " + str(self.anime.rating) +"/10"
        img_pixmap = QPixmap(self.anime.image)
        self.ui.animeTitle.setText(self.anime.title)
        self.ui.animeInfo.setText(description_text)
        self.ui.animeView.setPixmap(img_pixmap)


class Animation:
    def drop_shadow_on(self, target_widget):
        effect = QGraphicsDropShadowEffect(target_widget)
        effect.setColor(QColorConstants.White)
        effect.setOffset(*Config.DROP_SHADOW_OFFSET)
        effect.setBlurRadius(Config.DROP_SHADOW_BLUR_RADIUS)
        target_widget.setGraphicsEffect(effect)

    def drop_shadow_off(self, target_widget):
        target_widget.setGraphicsEffect(None)

    def drop_shadow_on_hovered(self, target_widget:QLabel):
        target_widget.enterEvent = lambda x: Animation.drop_shadow_on(self, target_widget)
        target_widget.leaveEvent = lambda x: Animation.drop_shadow_off(self, target_widget)