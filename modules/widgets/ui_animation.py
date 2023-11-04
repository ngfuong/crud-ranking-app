from PyQt6.QtGui import QColorConstants
from PyQt6.QtWidgets import QLabel, QGraphicsDropShadowEffect

from config import Config


class UIAnimation:
    def drop_shadow_on(self, target_widget):
        effect = QGraphicsDropShadowEffect(target_widget)
        effect.setColor(QColorConstants.White)
        effect.setOffset(Config.DROP_SHADOW_OFFSET)
        effect.setBlurRadius(Config.DROP_SHADOW_BLUR_RADIUS)
        target_widget.setGraphicsEffect(effect)

    def drop_shadow_off(self, target_widget):
        target_widget.setGraphicsEffect(None)

    def drop_shadow_on_hovered(self, target_widget:QLabel):
        target_widget.enterEvent = lambda x: UIAnimation.drop_shadow_on(self, target_widget)
        target_widget.leaveEvent = lambda x: UIAnimation.drop_shadow_off(self, target_widget)

