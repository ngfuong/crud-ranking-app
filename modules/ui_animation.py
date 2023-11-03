from PyQt6.uic import load_ui
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import  QPixmap, QIcon, QColorConstants
from PyQt6.QtWidgets import QLabel, QGraphicsDropShadowEffect 

from main import MainWindow
from .ui_config import UIConfig


class UIAnimationFunctions(MainWindow):
    def toggle_menu(self):
        # GET WIDTH
        width = self.ui.leftMenu.width()
        maxExtend = UIConfig.MENU_FULL_WIDTH
        standard = UIConfig.MENU_COLLAPSED_WIDTH

        # SET MAX WIDTH
        if width == standard:
            widthExtended = maxExtend
        else:
            widthExtended = standard

        # ANIMATION
        self.animation = QPropertyAnimation(self.ui.leftMenu, b"minimumWidth")
        self.animation.setDuration(UIConfig.TOGGLE_ANIMATION_DURATION)
        self.animation.setStartValue(width)
        self.animation.setEndValue(widthExtended)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuart)
        self.animation.start()
    
    def toggleButtonMousePressed(self, pressed=False):
        icon = QIcon()
        if pressed:
            icon.addPixmap(QPixmap("ui/sidebar/bars-solid-f26419.svg"))
            self.toggleButtonPressed = False
        else:
            icon.addPixmap(QPixmap("ui/sidebar/x-solid-f26419.svg"))
            self.toggleButtonPressed = True
        self.ui.toggleButton.setIcon(icon)
    
    def drop_shadow_on(self, target_widget):
        effect = QGraphicsDropShadowEffect(target_widget)
        effect.setColor(QColorConstants.White)
        effect.setOffset(*UIConfig.DROP_SHADOW_OFFSET)
        effect.setBlurRadius(UIConfig.DROP_SHADOW_BLUR_RADIUS)
        target_widget.setGraphicsEffect(effect)

    def drop_shadow_off(self, target_widget):
        target_widget.setGraphicsEffect(None)

    def drop_shadow_on_hovered(self, target_widget:QLabel):
        target_widget.enterEvent = lambda x: UIAnimationFunctions.drop_shadow_on(self, target_widget)
        target_widget.leaveEvent = lambda x: UIAnimationFunctions.drop_shadow_off(self, target_widget)

