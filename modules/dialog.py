from PyQt6.uic import load_ui
from PyQt6 import QtWidgets

from ui.add_dialog_ui import Ui_AddDialog
from ui.edit_dialog_ui import Ui_EditDialog

from .ui_config import UIConfig
from .models import AnimeItem


class Dialog(QtWidgets.QDialog):
    """
    Prorotype Dialog
    """
    def __init__(self, dialog_type):
        super().__init__()
        self.ui = None

    def _browse_files(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self,
                                            'Open file', 
                                            '.', 
                                            filter='Image files (*.png, *.jpg, *.svg)'
                                            )
        self.ui.uploadImgButton.setText(fname[0])
        return fname
    
    def return_input_fields(self) -> dict:
        return {
            "title": self.ui.titleInput.text(),
            "release_date": self.ui.releasedateInput.text(),
            "image": self.ui.uploadImgButton.text(),
            "rating": self.ui.ratingInput.text()
        }


class AddDialog(Dialog):
    """
    Add Dialog
    """
    UI_LOCATION = f"{UIConfig.LOCAL_DIR}../ui/add_dialog.ui"
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
    

class EditDialog(Dialog):
    """
    Edit Dialog
    """
    UI_LOCATION = f"{UIConfig.LOCAL_DIR}../ui/edit_dialog.ui"
    def __init__(self, edit_item:AnimeItem):
        super().__init__(EditDialog)
        try:
            self.ui = Ui_EditDialog()
            self.ui.setupUi(self)
        except NameError:
            self.ui = load_ui.loadUi(self.UI_LOCATION)

        self.ui.titleInput.setText(edit_item.title)
        self.ui.releasedateInput.setText(edit_item.release_date)
        self.ui.uploadImgButton.setText(edit_item.image)
        self.ui.ratingInput.setText(str(edit_item.rating))

        self.ui.uploadImgButton.clicked.connect(lambda: self._browse_files())
