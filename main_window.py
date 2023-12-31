import os

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox, QHBoxLayout 
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, Qt, \
                        QThreadPool
from PyQt6.QtGui import QPixmap, QIcon, QMovie

from config import Config
try:
    from ui.ui_main_window import Ui_MainWindow
except ImportError:
    pass

from app.models import AnimeDatabase
from app.widgets.anime import AnimeItemWidget
from app.widgets.dialog import AddDialog, EditDialog
from app.threading import Worker

import speech_recognition as sr
from playsound import playsound


class MainWindow(QMainWindow):
    UI_LOCATION = os.path.join(Config.UI_DIR, "main_window.ui")
    STYLE_LOCATION = os.path.join(Config.UI_DIR, "style_main.qss")
    def __init__(self, parent:QApplication):
        super(MainWindow, self).__init__()
        self.app = parent
        try:
            self.ui = uic.loadUi(self.UI_LOCATION, self)
        except FileNotFoundError:
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)

        with open(self.STYLE_LOCATION, "r") as style_file:
            style_config = style_file.read()
        self.setStyleSheet(style_config)

        global widgets
        widgets = self.ui

        global database
        self.dtb = AnimeDatabase()
        database = self.dtb

        global h_layout 
        self.horizontal_layout = QHBoxLayout(widgets.animeListWidget)
        h_layout = self.horizontal_layout
        h_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout = AnimeHorizontalLayout()

        widgets.stackedWidget.setCurrentIndex(Config.HOME_PAGE_INDEX)
        self.setup_leftMenu()
        self.setup_CRUD_page()
        self.setup_rank_page()
        
        self.speech = ""
        self.sttPrevPixmap = widgets.sttLabel.pixmap()
        # Display ui first
        self.show()

        # Handle multithreading
        self.threadpool = QThreadPool()
        # self.threadpool.setMaxThreadCount(2)
        print(f"Multithreading with maximum {self.threadpool.maxThreadCount()} threads...")
        self.setup_stt()

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
        self.layout.display_layout()
        widgets.sortRankButton.clicked.connect(lambda:self.layout.sort_by_rating())
        widgets.sortDateButton.clicked.connect(lambda:self.layout.sort_by_date())
        widgets.AtoZButton.clicked.connect(lambda:self.layout.sort_by_alphabet())
    
    def setup_stt(self):
        widgets.sttLabel.mousePressEvent = lambda x: self.on_listening_started()

    def thread_complete(self, val='finished'):
        print(f'def thread_complete(self, obj): {val}')
        self.gif.stop()                                  # <---- +++
        self.ui.sttLabel.setPixmap(self.sttPrevPixmap)
        if self.speech:
            self.on_speech_recognized()
    
    def progress_fn(self, val):
        print(f'def progress_fn(self, obj): {val}')


    def on_listening_started(self):
        self.gif = QMovie(Config.GIF_PATH)
        self.gif.setSpeed(100)
        widgets.sttLabel.setMovie(self.gif)
        self.gif.start()
        # Function to execute TTS
        worker = Worker(self.get_voice_input)
        worker.signals.finished.connect(self.thread_complete)
        self.threadpool.start(worker)

    def get_voice_input(self):
        """
        Text-to-speech
        """
        self.speech = ""
        r = sr.Recognizer()
        with sr.Microphone(device_index=Config.MICROPHONE_INDEX) as source:
            print("Say something!")
            playsound("ui/assets/voice.mp3")
            audio = r.listen(source, phrase_time_limit=3)

        try:
            self.speech = r.recognize_google(audio)
            print("Google Speech Recognition thinks you said " + self.speech)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        
        return self.speech

    def print_output(self, obj):
        print(f'def print_output(self, obj): {obj}')

    def on_speech_recognized(self):
        self.speech = self.speech.strip().lower()
        widgets.stackedWidget.setCurrentIndex(Config.RANK_PAGE_INDEX)
        widgets.searchInput.setText(self.speech)
        matched_items = database.search_by_title(self.speech)
        if len(matched_items) != 0:
            formatted_text = f"Search results for \"{self.speech}\""
            self.layout.update_layout(item_list=matched_items)
        else:
            formatted_text = f"No results for \"{self.speech}\""
        
        widgets.searchInput.setPlaceholderText(formatted_text)
    
    def on_searchButton_clicked(self):
        widgets.stackedWidget.setCurrentIndex(Config.RANK_PAGE_INDEX)
        search_text = widgets.searchInput.text().strip()

        if search_text:
            matched_items = database.search_by_title(search_text)
            self.layout.clear_layout()
            if len(matched_items) != 0:
                formatted_text = f"Search results for \"{search_text}\""
                self.layout.update_layout(item_list=matched_items)
            else:
                formatted_text = f"No results for \"{search_text}\""
            
            widgets.searchInput.setPlaceholderText(formatted_text)
            return matched_items

    def on_userButton_clicked(self):
        widgets.stackedWidget.setCurrentIndex(Config.USER_PAGE_INDEX)

    def on_homeButton_toggled(self):
        widgets.stackedWidget.setCurrentIndex(Config.HOME_PAGE_INDEX)

    def on_tvshowsButton_toggled(self):
        widgets.stackedWidget.setCurrentIndex(Config.TVSHOW_PAGE_INDEX)

    def on_CRUDButton_toggled(self):
        widgets.stackedWidget.setCurrentIndex(Config.CRUD_MENU_INDEX)

    def on_rankButton_toggled(self):
        widgets.stackedWidget.setCurrentIndex(Config.RANK_PAGE_INDEX)
    
    def on_rankButton_clicked(self):
        self.layout.update_layout()

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
            database.add_item(inputs)

    def edit(self):
        curr_index = widgets.animeList.currentRow()
        item = widgets.animeList.item(curr_index)
        item_title = item.text()
        edit_item = database.get_first_item_by_title(item_title)
        if item is not None:
            edit_dialog = EditDialog(edit_item)
            if edit_dialog.exec():
                inputs = edit_dialog.return_input_fields()
                item.setText(inputs["title"])
                database.edit_item(item_title, inputs)

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
        search_anime_field = widgets.inputAnime.text().strip().lower()
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
            h_layout.addWidget(anime_item_widget)
        widgets.animeListWidget.setLayout(h_layout)
    
    def clear_layout(self):
        while h_layout.count():
            child = h_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def update_layout(self, item_list=None):
        self.clear_layout()
        
        if item_list is None:
            item_list = database.anime_item_list
        # Update layout from custom item list
        for anime in item_list:
            anime_item_widget = AnimeItemWidget(anime)
            h_layout.addWidget(anime_item_widget)

    def sort_by_rating(self):
        database.sort_item_by_rating()
        self.update_layout()

    def sort_by_date(self):
        database.sort_item_by_date()
        self.update_layout()
    
    def sort_by_alphabet(self):
        database.sort_item_by_title()
        self.update_layout()
