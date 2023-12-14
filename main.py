import sys

from PyQt6.QtWidgets import QApplication
from main_window import MainWindow
from app.widgets.login import LoginWindow


def launch_main_window(parent, app):
    window = MainWindow(app)
    parent.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    login_window = LoginWindow()
    login_window.login_signal.connect(lambda: launch_main_window(login_window, app))
    login_window.show()

    sys.exit(app.exec())