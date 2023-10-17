from main import MainWindow
from PyQt6.QtCore import pyqtSlot, QFile, QTextStream, QPropertyAnimation, QEasingCurve

from PyQt6.QtGui import QColor, QPixmap, QPainter, QPixmap, QIcon
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QDialog, QLineEdit, QDialogButtonBox, \
                            QFormLayout, QMessageBox
from PyQt6 import QtSvg
# from PyQt6.QtCore import

from .ui_config import UIConfig

class UIFunctions(MainWindow):
    def toggle_menu(self, enabled):
        if enabled:
            # GET WIDTH
            width = self.ui.leftMenu.width()
            maxExtend = UIConfig.MENU_FULL_WIDTH 
            standard = UIConfig.MENU_COLLAPSED_WIDTH

            # SET MAX WIDTH
            if width == UIConfig.MENU_COLLAPSED_WIDTH:
                widthExtended = maxExtend
                self.ui.logoLabel_3.show()
            else:
                widthExtended = standard
                self.ui.logoLabel_3.hide()
            
            # ANIMATION
            self.animation = QPropertyAnimation(self.ui.leftMenu, b"minimumWidth")
            self.animation.setDuration(UIConfig.MENU_TOGGLE_ANIMATION)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QEasingCurve.Type.InOutQuart)
            self.animation.start()
    
    def toggleLeftBox(self, enabled):
        if enabled:
            # GET WIDTH
            width = self.ui.extraLeftBox.width()
    
    def toggleButtonMousePressed(self, pressed=False):
        icon = QIcon()
        if pressed:
            icon.addPixmap(QPixmap("ui/sidebar/bars-solid-f26419.svg"))
            self.toggleButtonPressed = False 
        else:
            icon.addPixmap(QPixmap("ui/sidebar/x-solid-f26419.svg"))
            self.toggleButtonPressed = True 
        self.ui.toggleButton.setIcon(icon)

    # CRUD APPLICATIONS
    # def show_add_menu(self):
    #     msg = QMessageBox


class AddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title = QLineEdit(self)
        self.release_date = QLineEdit(self)
        self.image = QLineEdit(self)
        self.rating = QLineEdit(self)

        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, self)

        layout = QFormLayout(self)
        layout.addRow("Title", self.title)
        layout.addRow("Release Date", self.release_date)
        layout.addRow("Image", self.image)
        layout.addRow("Rating", self.rating)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
    
    def getInputs(self):
        return {
            "title": self.title.text(),
            "release_date": self.release_date.text(),
            "image": self.image.text(), 
            "rating": self.rating.text()
        }


class UIManageFunctions(MainWindow):
    def addAnime(self):
        currIndex = self.ui.animeList.currentRow()
        dialog = AddDialog()
        if dialog.exec():
            inputs = dialog.getInputs()
            self.ui.animeList.insertItem(currIndex, inputs["title"])

    def editAnime(self):
        currIndex = self.ui.animeList.currentRow()
        item = self.ui.animeList.item(currIndex)
        if item is not None:
            dialog = AddDialog()
            if dialog.exec():
                inputs = dialog.getInputs()
                item.setText(inputs["title"])

    def deleteAnime(self):
        currIndex = self.ui.animeList.currentRow()
        item = self.ui.animeList.item(currIndex)
        if item is None:
            return
        question = QMessageBox.question(self, "Remove Anime",
                                        "Do you want to remove this anime?", 
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if question == QMessageBox.StandardButton.Yes:
            item = self.ui.animeList.takeItem(currIndex)
            del item
    
    def searchAnime(self):
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

    def updateData(self):
        pass
"""
    # Change color of svg icons

    def change_icon_color(widget, color):
        color = Qt.GlobalColor.white
        new_pixmap = svg_to_pixmap(widget.fileName, widget.width(), widget.height(), background_color=color)
        widget.setPixmap(new_pixmap)

def paint_pixmap(old_pixmap, width, height, background_color):
    # renderer = QtSvg.QSvgRenderer(svg_filename)
    # pixmap = QPixmap(width, height)
    # pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(old_pixmap)
    renderer.render(painter)
    painter.setCompositionMode(painter.CompositionMode.CompositionMode_SourceIn)
    if background_color:
        painter.fillRect(pixmap.rect(), background_color)
    painter.end()
    return pixmap
"""