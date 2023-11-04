import sys

from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox, QLabel, QHBoxLayout
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, Qt
from PyQt6.QtGui import QPixmap, QIcon

from ui.desktop_app_scrollable_ui import Ui_MainWindow

from config import Config

from modules.widgets.models import AnimeDatabase
from modules.widgets.anime import AnimeItem, AnimeItemWidget
from modules.widgets.dialog import AddDialog, EditDialog
from modules.utils import deprecated


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # QDir.setCurrent("./")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        widgets.leftMenu.show()
        widgets.logoLabel_3.hide()

        # UI: Toggle menu
        widgets.toggleButton.clicked.connect(lambda:LeftMenuAnimation.on_toggled(self))
        self.toggleButtonPressed = False
        self.toggleButtonPressed = widgets.toggleButton.clicked.connect(lambda:LeftMenuAnimation.toggleButtonMousePressed(self, pressed=self.toggleButtonPressed))

        # CRUD Model: Setup Manage Views
        self.dtb = AnimeDatabase()
        global database
        database = self.dtb

        database.load_data()
        widgets.animeList.addItems(database.anime_title_list)
        widgets.animeList.setCurrentRow(0)
        widgets.addButton.clicked.connect(lambda:AnimeCRUD.add_anime(self))
        widgets.editButton.clicked.connect(lambda:AnimeCRUD.edit_anime(self))
        widgets.removeButton.clicked.connect(lambda:AnimeCRUD.delete_anime(self))
        widgets.searchAnime.clicked.connect(lambda:AnimeCRUD.search_anime(self))

        # RANKING VIEW: Setup Anime by Columns
        UIDisplayAnime.displayAnimeLayout(self)
        widgets.sortRankButton.clicked.connect(lambda:UIDisplayAnime.viewSortedByRating(self))
        widgets.sortDateButton.clicked.connect(lambda:UIDisplayAnime.viewSortedByDate(self))
        widgets.AtoZButton.clicked.connect(lambda:UIDisplayAnime.viewSortedAtoZ(self))
        

    HOME_PAGE_INDEX = 0
    TV_SHOW_INDEX = 1
    MANAGE_MENU_INDEX=2
    RANK_PAGE_INDEX = 3
    USER_PAGE_INDEX = 4
    SEARCH_ANIME_INDEX = 5

    def on_searchButton_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(self.SEARCH_ANIME_INDEX)
        search_text = self.ui.searchInput.text().strip()
        if search_text:
            self.ui.label_8.setText(search_text)
    
    def on_userButton_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(self.USER_PAGE_INDEX)
    
    def on_homeButton_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(self.HOME_PAGE_INDEX)

    def on_tvshowsButton_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(self.TV_SHOW_INDEX)
                
    def on_moviesButton_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(self.MANAGE_MENU_INDEX)

    def on_rankButton_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(self.RANK_PAGE_INDEX)
    
    def on_exitButton_1_clicked(self):
        QApplication.quit()


class LeftMenuAnimation:
    def on_toggled(self):
        # GET WIDTH
        width = widgets.leftMenu.width()
        maxExtend = Config.MENU_FULL_WIDTH
        standard = Config.MENU_COLLAPSED_WIDTH

        # SET MAX WIDTH
        if width == standard:
            widthExtended = maxExtend
        else:
            widthExtended = standard

        # ANIMATION
        self.animation = QPropertyAnimation(widgets.leftMenu, b"minimumWidth")
        self.animation.setDuration(Config.TOGGLE_ANIMATION_DURATION)
        self.animation.setStartValue(width)
        self.animation.setEndValue(widthExtended)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuart)
        self.animation.start()
    
    def toggleButtonMousePressed(self, pressed=False) -> bool:
        icon = QIcon()
        if pressed:
            icon.addPixmap(QPixmap("ui/sidebar/bars-solid-f26419.svg"))
            pressed = False
        else:
            icon.addPixmap(QPixmap("ui/sidebar/x-solid-f26419.svg"))
            pressed = True
        widgets.toggleButton.setIcon(icon)
        return pressed

class AnimeCRUD():
    def add_anime(self):
        currIndex = widgets.animeList.currentRow()
        add_dialog = AddDialog()
        if add_dialog.exec():
            inputs = add_dialog.return_input_fields()
            widgets.animeList.insertItem(currIndex, inputs["title"])
            database.add_item_from_dict(inputs)

    def edit_anime(self):
        curr_index = widgets.animeList.currentRow()
        item = widgets.animeList.item(curr_index)
        item_title = item.text()
        edit_item = database.get_item_by_title(item_title)
        if item is not None:
            edit_dialog = EditDialog(edit_item)
            if edit_dialog.exec():
                inputs = edit_dialog.return_input_fields()
                item.setText(inputs["title"])
                database.edit_item_from_dict(item_title, inputs)

    def delete_anime(self):
        curr_index = widgets.animeList.currentRow()
        item = widgets.animeList.item(curr_index)
        item_title = item.text()
        if item is None:
            return
        question = QMessageBox.question(self, "Remove Anime",
                                        "Do you want to remove this anime?", 
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if question == QMessageBox.StandardButton.Yes:
            item = widgets.animeList.takeItem(curr_index)
            database.delete_item(item_title)
    
    def search_anime(self):
        search_anime_field = widgets.inputAnime.text().strip()
        if search_anime_field:
            matched_items = widgets.animeList.findItems(search_anime_field, Qt.MatchFlag.MatchContains)
            for i in range(widgets.animeList.count()):
                it = widgets.animeList.item(i)
                it.setHidden(it not in matched_items)
        else:
            for i in range(widgets.animeList.count()):
                it = widgets.animeList.item(i)
                it.setHidden(False)
        
class UIDisplayAnime():
    def updateAnimeLayout(self, layout:QHBoxLayout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        for anime in database.anime_item_list:
            anime_item_widget = AnimeItemWidget(anime)
            horizontal_layout.addWidget(anime_item_widget)

    def displayAnimeLayout(self):
        global horizontal_layout
        horizontal_layout = QHBoxLayout(widgets.animeListWidget)
        for anime in database.anime_item_list:
            anime_item_widget = AnimeItemWidget(anime)
            horizontal_layout.addWidget(anime_item_widget)
        
        widgets.animeListWidget.setLayout(horizontal_layout)

    def viewSortedByRating(self):
        database.sort_item_by_rating()
        UIDisplayAnime.updateAnimeLayout(self, horizontal_layout)

    def viewSortedByDate(self):
        database.sort_item_by_date()        
        UIDisplayAnime.updateAnimeLayout(self, horizontal_layout)
    
    def viewSortedAtoZ(self):
        database.sort_item_by_title()
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

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load style
    with open("ui/style.qss", "r") as style_file:
        style_config = style_file.read()
    app.setStyleSheet(style_config)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
