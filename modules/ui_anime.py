import requests

from PyQt6.uic import load_ui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import  QPixmap
from PyQt6.QtWidgets import QMessageBox, QLabel, QWidget, QHBoxLayout

from main import MainWindow
from ui.anime_column_ui import Ui_AnimeColumn

from .ui_config import UIConfig
from .dialog import AddDialog, EditDialog
from .models import AnimeItem
from .ui_animation import UIAnimationFunctions

from .custom_decorators import deprecated


class AnimeItemWidget(QWidget, Ui_AnimeColumn):
    UI_LOCATION = f"{UIConfig.LOCAL_DIR}../ui/anime_column.ui"
    STYLE_LOCATION = f"{UIConfig.LOCAL_DIR}../ui/anime_style.qss"
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
        UIAnimationFunctions.drop_shadow_on_hovered(self, self)
        self.display_description()

    def display_description(self):
        description_text = self.anime.release_date + "\n" \
                            + "Rating: " + str(self.anime.rating) +"/10"
        img_pixmap = QPixmap(self.anime.image)
        self.ui.animeTitle.setText(self.anime.title)
        self.ui.animeInfo.setText(description_text)
        self.ui.animeView.setPixmap(img_pixmap)


class AnimeManageFunctions(MainWindow):
    def add_anime(self):
        currIndex = self.ui.animeList.currentRow()
        add_dialog = AddDialog()
        if add_dialog.exec():
            inputs = add_dialog.return_input_fields()
            self.ui.animeList.insertItem(currIndex, inputs["title"])
            self.dtb.add_item_from_dict(inputs)

    def edit_anime(self):
        curr_index = self.ui.animeList.currentRow()
        item = self.ui.animeList.item(curr_index)
        item_title = item.text()
        edit_item = self.dtb.get_item_by_title(item_title)
        if item is not None:
            edit_dialog = EditDialog(edit_item)
            if edit_dialog.exec():
                inputs = edit_dialog.return_input_fields()
                item.setText(inputs["title"])
                self.dtb.edit_item_from_dict(item_title, inputs)

    def delete_anime(self):
        curr_index = self.ui.animeList.currentRow()
        item = self.ui.animeList.item(curr_index)
        item_title = item.text()
        if item is None:
            return
        question = QMessageBox.question(self, "Remove Anime",
                                        "Do you want to remove this anime?", 
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if question == QMessageBox.StandardButton.Yes:
            item = self.ui.animeList.takeItem(curr_index)
            self.dtb.delete_item(item_title)
    
    def search_anime(self):
        search_anime_field = self.ui.inputAnime.text().strip()
        if search_anime_field:
            matched_items = self.ui.animeList.findItems(search_anime_field, Qt.MatchFlag.MatchContains)
            for i in range(self.ui.animeList.count()):
                it = self.ui.animeList.item(i)
                it.setHidden(it not in matched_items)
        else:
            for i in range(self.ui.animeList.count()):
                it = self.ui.animeList.item(i)
                it.setHidden(False)

            
class UIDisplayAnime(MainWindow):
    def updateAnimeLayout(self, layout:QHBoxLayout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        for anime in self.dtb.anime_item_list:
            anime_item_widget = AnimeItemWidget(anime)
            horizontal_layout.addWidget(anime_item_widget)

    def displayAnimeLayout(self):
        global horizontal_layout
        horizontal_layout = QHBoxLayout(self.ui.animeListWidget)
        for anime in self.dtb.anime_item_list:
            anime_item_widget = AnimeItemWidget(anime)
            horizontal_layout.addWidget(anime_item_widget)
        
        self.ui.animeListWidget.setLayout(horizontal_layout)

    def viewSortedByRating(self):
        self.dtb.sort_item_by_rating()
        UIDisplayAnime.updateAnimeLayout(self, horizontal_layout)

    def viewSortedByDate(self):
        self.dtb.sort_item_by_date()        
        UIDisplayAnime.updateAnimeLayout(self, horizontal_layout)
    
    def viewSortedAtoZ(self):
        self.dtb.sort_item_by_title()
        UIDisplayAnime.updateAnimeLayout(self, horizontal_layout)


    @deprecated
    def viewAnimeInColumn(self, anime:AnimeItem, description:QLabel, title:QLabel, image:QLabel):
        description_text = anime.release_date + "\n" \
                            + "Rating: " + str(anime.rating) +"/10"
        img_pixmap = QPixmap(anime.image)
        title.setText(anime.title)
        description.setText(description_text)
        image.setPixmap(img_pixmap)

    @deprecated
    def viewAnimeInColumn_byUrl(self, anime:AnimeItem, anime_info:QLabel, anime_title:QLabel):
        img_url = anime.image
        img_data = requests.get(img_url, timeout=10).content
        img_pixmap = QPixmap()
        img_pixmap.loadFromData(img_data)
        img_pixmap = img_pixmap.scaled(225, 318, Qt.AspectRatioMode.KeepAspectRatio)
        description_text = anime.release_date + "\n" \
                            + "Rating: " + str(anime.rating) +"/10"
        anime_info.setText(description_text)
        # anime_info.setAlignment("AlignLeft")
        anime_title.setText(anime.title)
        # img_view.setPixmap(img_pixmap)
