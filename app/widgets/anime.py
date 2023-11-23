import webbrowser
import os

from PyQt6 import uic
from PyQt6.QtGui import QPixmap, QColorConstants
from PyQt6.QtWidgets import QWidget, QLabel, QGraphicsDropShadowEffect

from config import Config
try:
    from ui.anime_column_ui import Ui_AnimeColumn
except ImportError:
    pass
from app.models import AnimeItem


class AnimeItemWidget(QWidget):
    STYLE_LOCATION = os.path.join(Config.UI_DIR, "style_anime.qss")
    UI_LOCATION = os.path.join(Config.UI_DIR, "anime_column.ui")
    def __init__(self, anime:AnimeItem):
        QWidget.__init__(self)
        try:
            self.ui = uic.loadUi(self.UI_LOCATION, self)
        except FileNotFoundError:
            self.ui = Ui_AnimeColumn()
            self.ui.setupUi(self)

        with open(self.STYLE_LOCATION, "r") as style_file:
            style_config = style_file.read()
        self.setStyleSheet(style_config)

        self.anime = anime
        self.display_description()

        Animation.drop_shadow_on_hovered(self, self)
        self.ui.animeCol.mouseDoubleClickEvent = lambda x: self.open_link(self.anime.link)
        if self.anime.link != 'None':
            self.ui.animeCol.setToolTip("Double click to watch")

    def display_description(self):
        description_text = self.anime.release_date + "\n" \
                            + "Rating: " + str(self.anime.rating) +"/10"
        img_pixmap = QPixmap(self.anime.image)
        self.ui.animeTitle.setText(self.anime.title)
        self.ui.animeInfo.setText(description_text)
        self.ui.animeView.setPixmap(img_pixmap)

    def open_link(self, url):
        if url != 'None':
            webbrowser.open(url)


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