import sys
from copy import deepcopy

from PyQt6.QtWidgets import QMainWindow, QApplication, QGraphicsDropShadowEffect, QFrame, \
                            QHBoxLayout
from PyQt6.QtCore import Qt

# from ui.desktop_app_ui import Ui_MainWindow
from ui.desktop_app_scrollable_ui import Ui_MainWindow

from modules import *
from modules.models import AnimeDatabase


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
        self.toggleButtonPressed = False
        widgets.toggleButton.clicked.connect(lambda:UIAnimationFunctions.toggle_menu(self))
        widgets.toggleButton.clicked.connect(lambda:UIAnimationFunctions.toggleButtonMousePressed(self, pressed=self.toggleButtonPressed))

        # CRUD Model: Setup Manage Views
        self.dtb = AnimeDatabase()
        self.dtb.load_data()
        widgets.animeList.addItems(self.dtb.anime_title_list)
        widgets.animeList.setCurrentRow(0)
        widgets.addButton.clicked.connect(lambda:AnimeManageFunctions.add_anime(self))
        widgets.editButton.clicked.connect(lambda:AnimeManageFunctions.edit_anime(self))
        widgets.removeButton.clicked.connect(lambda:AnimeManageFunctions.delete_anime(self))
        widgets.searchAnime.clicked.connect(lambda:AnimeManageFunctions.search_anime(self))

        # RANKING VIEW: Setup Anime by Columns
        UIDisplayAnime.displayAnimeLayout(self)
        widgets.sortRankButton.clicked.connect(lambda:UIDisplayAnime.viewSortedByRating(self))
        widgets.sortDateButton.clicked.connect(lambda:UIDisplayAnime.viewSortedByDate(self))
        widgets.AtoZButton.clicked.connect(lambda:UIDisplayAnime.viewSortedAtoZ(self))
        

    # Function for searching anime
    def on_searchButton_clicked(self):
        # Set index for searching
        self.ui.stackedWidget.setCurrentIndex(5) # ???
        search_text = self.ui.searchInput.text().strip()
        if search_text:
            self.ui.label_8.setText(search_text)
    
    # Function for changing page to user page
    def on_userButton_clicked(self):
        # Set index to change to user page=4
        self.ui.stackedWidget.setCurrentIndex(4)
    
    # Function for changing menu page
    # (0) Home Page -> (1) Tv Show -> (2) Movies -> (3) Ranking -> (4) User
    def on_homeButton_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def on_tvshowsButton_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)
                
    def on_moviesButton_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def on_rankButton_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(3)
    
    def on_exitButton_1_clicked(self):
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load style
    with open("ui/style.qss", "r") as style_file:
        style_config = style_file.read()
    app.setStyleSheet(style_config)


    window = MainWindow()
    window.show()

    sys.exit(app.exec())