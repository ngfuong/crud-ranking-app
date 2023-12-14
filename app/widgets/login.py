import os

from PyQt6 import uic
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal, Qt

from config import Config
try:
    from ui.ui_login_window import Ui_LoginWindow 
except ImportError:
    pass

from app.credential_handler import check_credentials, register


class LoginWindow(QWidget):
    UI_LOCATION = os.path.join(Config.UI_DIR, "login_window.ui")
    STYLE_LOCATION = os.path.join(Config.UI_DIR, "style_login.qss")
    
    login_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        try:
            self.ui = uic.loadUi(self.UI_LOCATION, self)
        except FileNotFoundError:
            self.ui = Ui_LoginWindow()
            self.ui.setupUi(self)

        with open(self.STYLE_LOCATION, "r") as style_file:
            style_config = style_file.read()
        self.setStyleSheet(style_config)

        self.ui.frame.setFocus()

        self.ui.right_button.clicked.connect(self.handle_signup)
        self.ui.button.clicked.connect(self.handle_login)
    
    def handle_login(self):
        username = self.ui.username_input.text()
        password = self.ui.password_input.text()

        register(username, password)
        login_successful = check_credentials(username, password)
        if login_successful:
            print("Login successful!")
            self.login_signal.emit()

        print("Login failed!")

    def handle_signup(self):
        self.ui.title.setText("Sign up for Ranking App")
        self.ui.button.setText("Create account")
        self.ui.left_label.setText("Already have an account?")
        self.ui.right_button.setText("Log in")