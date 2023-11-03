import math

from PyQt6.QtCore import QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import  QPixmap, QIcon, QColorConstants
from PyQt6.QtWidgets import QLabel, QGraphicsDropShadowEffect

from main import MainWindow

class PaginationHelper:
    def __init__(self, collection, items_per_page=4) -> None:
        self.collection = collection
        self.items_per_page = items_per_page
    
    def item_count(self):
        return len(self.collection)

    def page_count(self):
        return math.ceil(self.item_count()/self.items_per_page)

    def page_item_count(self, page_index):
        page_index += 1 # Indexing starts at 1
        if page_index in range(0, self.page_count()):
            return self.items_per_page
        if page_index == self.page_count():
            return self.item_count()%self.items_per_page
        return -1

    def page_index(self, item_index):
        if item_index not in range (0, self.item_count()):
            return -1
        return math.floor(item_index/self.items_per_page)
        

class UIPagination(MainWindow):
    def displayPage(self):
        pass