from PyQt6.uic import load_ui
from PyQt6.QtWidgets import QDialog, QFileDialog
from PyQt6.QtCore import QDate, QDir

from config import Config
from ui.add_dialog_ui import Ui_AddDialog
from ui.edit_dialog_ui import Ui_EditDialog

from app.models import AnimeItem
from app.models import date_to_text, format_date


class Dialog(QDialog):
    """
    Prorotype Dialog
    """
    STYLE_LOCATION = f"{Config.LOCAL_DIR}/ui/style_popup.qss"
    def __init__(self, dialog_type):
        super().__init__()
        self.ui = None
        
        with open(self.STYLE_LOCATION, "r") as style_file:
            style_config = style_file.read()
        self.setStyleSheet(style_config)

        self.dir = QDir(Config.LOCAL_DIR)

    def _browse_files(self):
        fname = QFileDialog.getOpenFileName(self,
                                            'Open file', 
                                            './ui/images',
                                            # filter='Image files (*.png, *.jpg, *.svg)'
                                            )
        self.ui.uploadImgButton.setText(fname[0])
        return fname
    
    def return_input_fields(self) -> dict:
        date_input = self.ui.releasedateInput.date().toPyDate() # formatted YYYY-mm-dd
        image_path_input = self.ui.uploadImgButton.text()
        if self.ui.urlInput.text():
            url_input = self.ui.urlInput.text()
        else:
            url_input = "None"

        return {
            "title": self.ui.titleInput.text(),
            "release_date": date_to_text(date_input),
            "image": self.dir.relativeFilePath(image_path_input),
            "rating": float(self.ui.ratingInput.text()),
            "link": url_input
        }
    

class AddDialog(Dialog):
    """
    Add Dialog
    """
    UI_LOCATION = f"{Config.LOCAL_DIR}/ui/add_dialog.ui"
    def __init__(self):
        super().__init__(AddDialog)
        if isinstance(self.ui, Ui_AddDialog):
            pass
        else:
            try:
                self.ui = Ui_AddDialog()
                self.ui.setupUi(self)
            except NameError:
                self.ui = load_ui.loadUi(self.UI_LOCATION)

        self.ui.uploadImgButton.clicked.connect(lambda: self._browse_files())
        self.ui.releasedateInput.setDisplayFormat("dd/MM/yyyy")

class EditDialog(Dialog):
    """
    Edit Dialog
    """
    UI_LOCATION = f"{Config.LOCAL_DIR}/ui/edit_dialog.ui"
    def __init__(self, edit_item:AnimeItem):
        super().__init__(EditDialog)
        try:
            self.ui = Ui_EditDialog()
            self.ui.setupUi(self)
        except NameError:
            self.ui = load_ui.loadUi(self.UI_LOCATION)

        self.ui.releasedateInput.setDisplayFormat("dd/MM/yyyy")
        self.ui.uploadImgButton.clicked.connect(lambda: self._browse_files())

        self.ui.titleInput.setText(edit_item.title)
        date = format_date(edit_item.release_date)
        self.ui.releasedateInput.setDate(QDate(date.year, date.month, date.day))
        self.ui.uploadImgButton.setText(self.dir.relativeFilePath(edit_item.image))
        self.ui.ratingInput.setText(str(edit_item.rating))
        self.ui.urlInput.setText(edit_item.link)
