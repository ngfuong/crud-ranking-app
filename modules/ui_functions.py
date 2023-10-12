from main import MainWindow
from PyQt6.QtCore import pyqtSlot, QFile, QTextStream, QPropertyAnimation, QEasingCurve

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