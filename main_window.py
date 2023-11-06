from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox, QHBoxLayout
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, Qt
from PyQt6.QtGui import QPixmap, QIcon

from config import Config
from ui.desktop_app_scrollable_ui import Ui_MainWindow

from modules.widgets.models import AnimeDatabase
from modules.widgets.anime import AnimeItemWidget
from modules.widgets.dialog import AddDialog, EditDialog


class MainWindow(QMainWindow):
    STYLE_LOCATION = f"{Config.LOCAL_DIR}/ui/style_main.qss"
    def __init__(self):
        super(MainWindow, self).__init__()
        with open(self.STYLE_LOCATION, "r") as style_file:
            style_config = style_file.read()
        self.setStyleSheet(style_config)

        global widgets
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        widgets = self.ui

        global database
        self.dtb = AnimeDatabase()
        database = self.dtb

        global horizontal_layout
        self.horizontal_layout = QHBoxLayout(widgets.animeListWidget)
        horizontal_layout = self.horizontal_layout

        widgets.stackedWidget.setCurrentIndex(Config.HOME_PAGE_INDEX)
        self.setup_leftMenu()
        self.setup_CRUD_page()
        self.setup_rank_page()

    def setup_leftMenu(self):
        widgets.leftMenu.show()
        widgets.logoLabel_3.hide()
        widgets.toggleButton.clicked.connect(lambda:self.on_leftMenu_toggled())

    def setup_CRUD_page(self):
        database.load_data()
        widgets.animeList.addItems(database.anime_title_list)
        widgets.animeList.setCurrentRow(0)
        widgets.addButton.clicked.connect(lambda:AnimeCRUD.add(self))
        widgets.editButton.clicked.connect(lambda:AnimeCRUD.edit(self))
        widgets.removeButton.clicked.connect(lambda:AnimeCRUD.delete(self))
        widgets.searchAnime.clicked.connect(lambda:AnimeCRUD.search(self))

    def setup_rank_page(self):
        AnimeHorizontalLayout.display_layout(self)
        widgets.sortRankButton.clicked.connect(lambda:AnimeHorizontalLayout.sort_by_rating(self))
        widgets.sortDateButton.clicked.connect(lambda:AnimeHorizontalLayout.sort_by_date(self))
        widgets.AtoZButton.clicked.connect(lambda:AnimeHorizontalLayout.sort_by_alphabet(self))

    def on_searchButton_clicked(self):
        widgets.stackedWidget.setCurrentIndex(Config.SEARCH_ANIME_INDEX)
        search_text = widgets.searchInput.text().strip()
        if search_text:
            formatted_text = f"Searching for \"{search_text}\"..."
            widgets.search_text.setText(formatted_text)

    def on_userButton_clicked(self):
        widgets.stackedWidget.setCurrentIndex(Config.USER_PAGE_INDEX)

    def on_homeButton_toggled(self):
        widgets.stackedWidget.setCurrentIndex(Config.HOME_PAGE_INDEX)

    def on_tvshowsButton_toggled(self):
        widgets.stackedWidget.setCurrentIndex(Config.TV_SHOW_INDEX)

    def on_CRUDButton_toggled(self):
        widgets.stackedWidget.setCurrentIndex(Config.CRUD_MENU_INDEX)

    def on_rankButton_toggled(self):
        widgets.stackedWidget.setCurrentIndex(Config.RANK_PAGE_INDEX)
        AnimeHorizontalLayout.update_layout(self)

    def on_exitButton_clicked(self):
        QApplication.quit()

    def on_leftMenu_toggled(self):
        # Get width
        width = widgets.leftMenu.width()
        maxExtend = Config.MENU_FULL_WIDTH
        standard = Config.MENU_COLLAPSED_WIDTH
        # Get current icon
        icon = QIcon()

        # Set animation width and icon 
        if width == standard:
            widthExtended = maxExtend
            icon.addPixmap(QPixmap("ui/sidebar/x-solid-f26419.svg"))
        else:
            widthExtended = standard
            icon.addPixmap(QPixmap("ui/sidebar/bars-solid-f26419.svg"))

        # Animation 
        self.animation = QPropertyAnimation(widgets.leftMenu, b"minimumWidth")
        self.animation.setDuration(Config.TOGGLE_ANIMATION_DURATION)
        self.animation.setStartValue(width)
        self.animation.setEndValue(widthExtended)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuart)
        self.animation.start()
        widgets.toggleButton.setIcon(icon)


class AnimeCRUD():
    def add(self):
        currIndex = widgets.animeList.currentRow()
        add_dialog = AddDialog()
        if add_dialog.exec():
            inputs = add_dialog.return_input_fields()
            widgets.animeList.insertItem(currIndex, inputs["title"])
            database.add_item_from_dict(inputs)

    def edit(self):
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

    def delete(self):
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

    def search(self):
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
    

class AnimeHorizontalLayout():
    def display_layout(self):
        for anime in database.anime_item_list:
            anime_item_widget = AnimeItemWidget(anime)
            horizontal_layout.addWidget(anime_item_widget)
        widgets.animeListWidget.setLayout(horizontal_layout)

    def update_layout(self):
        while horizontal_layout.count():
            child = horizontal_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        for anime in database.anime_item_list:
            anime_item_widget = AnimeItemWidget(anime)
            horizontal_layout.addWidget(anime_item_widget)

    def sort_by_rating(self):
        database.sort_item_by_rating()
        AnimeHorizontalLayout.update_layout(self)

    def sort_by_date(self):
        database.sort_item_by_date()
        AnimeHorizontalLayout.update_layout(self)
    
    def sort_by_alphabet(self):
        database.sort_item_by_title()
        AnimeHorizontalLayout.update_layout(self)
