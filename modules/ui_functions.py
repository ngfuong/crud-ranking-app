import requests

from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, Qt
from PyQt6.QtGui import  QPixmap, QIcon, QColorConstants
from PyQt6.QtWidgets import QMessageBox, QLabel, QGraphicsDropShadowEffect

from main import MainWindow
from .ui_config import UIConfig
from .dialog import AddDialog, EditDialog
from .models import AnimeItem

from .tools import deprecated


class UIFunctions(MainWindow):
    def toggle_menu(self):
        # GET WIDTH
        width = self.ui.leftMenu.width()
        maxExtend = UIConfig.MENU_FULL_WIDTH
        standard = UIConfig.MENU_COLLAPSED_WIDTH

        # SET MAX WIDTH
        if width == standard:
            widthExtended = maxExtend
        else:
            widthExtended = standard

        # ANIMATION
        self.animation = QPropertyAnimation(self.ui.leftMenu, b"minimumWidth")
        self.animation.setDuration(UIConfig.TOGGLE_ANIMATION_DURATION)
        self.animation.setStartValue(width)
        self.animation.setEndValue(widthExtended)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuart)
        self.animation.start()
    
    def toggleButtonMousePressed(self, pressed=False):
        icon = QIcon()
        if pressed:
            icon.addPixmap(QPixmap("ui/sidebar/bars-solid-f26419.svg"))
            self.toggleButtonPressed = False
        else:
            icon.addPixmap(QPixmap("ui/sidebar/x-solid-f26419.svg"))
            self.toggleButtonPressed = True
        self.ui.toggleButton.setIcon(icon)
    
    def drop_shadow_on(self, target_widget):
        effect = QGraphicsDropShadowEffect(target_widget)
        effect.setColor(QColorConstants.White)
        effect.setOffset(*UIConfig.DROP_SHADOW_OFFSET)
        effect.setBlurRadius(UIConfig.DROP_SHADOW_BLUR_RADIUS)
        target_widget.setGraphicsEffect(effect)

    def drop_shadow_off(self, target_widget):
        target_widget.setGraphicsEffect(None)

    def drop_shadow_on_hovered(self, target_widget:QLabel):
        target_widget.enterEvent = lambda x: UIFunctions.drop_shadow_on(self, target_widget)
        target_widget.leaveEvent = lambda x: UIFunctions.drop_shadow_off(self, target_widget)


class UIManageFunctions(MainWindow):
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


class AnimeColumnView(MainWindow):
    def updateAnimeView(self):
        anime1 = self.dtb.anime_item_list[0]
        anime2 = self.dtb.anime_item_list[1]
        anime3 = self.dtb.anime_item_list[2]
        anime4 = self.dtb.anime_item_list[3]
        AnimeColumnView.viewAnimeInColumn(self, anime1, self.ui.animeLabel1, self.ui.animeTitle1, self.ui.animeView1)
        AnimeColumnView.viewAnimeInColumn(self, anime2, self.ui.animeLabel2, self.ui.animeTitle2, self.ui.animeView2)
        AnimeColumnView.viewAnimeInColumn(self, anime3, self.ui.animeLabel3, self.ui.animeTitle3, self.ui.animeView3)
        AnimeColumnView.viewAnimeInColumn(self, anime4, self.ui.animeLabel4, self.ui.animeTitle4, self.ui.animeView4)

    def viewSortedByRating(self):
        self.dtb.sort_item_by_rating()
        AnimeColumnView.updateAnimeView(self)

    def viewSortedByDate(self):
        self.dtb.sort_item_by_date()        
        AnimeColumnView.updateAnimeView(self)
    
    def viewSortedAtoZ(self):
        self.dtb.sort_item_by_title()
        AnimeColumnView.updateAnimeView(self)
    
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
