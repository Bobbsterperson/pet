from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, QSize, Qt


class InfoIconButton(QPushButton):
    hovered = pyqtSignal(str)   # Signal to update info bar
    unhovered = pyqtSignal()    # Signal to clear info bar

    def __init__(self, icon_path_0, icon_path_1, hover_text, parent=None):
        super().__init__(parent)
        self.icon_path_0 = icon_path_0
        self.icon_path_1 = icon_path_1
        self.hover_text = hover_text

        self.setFixedSize(64, 64)
        self.setIcon(QIcon(self.icon_path_0))
        self.setIconSize(QSize(48, 48))
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(self.default_style())

    def enterEvent(self, event):
        self.setIcon(QIcon(self.icon_path_1))
        self.setStyleSheet(self.hover_style())
        self.hovered.emit(self.hover_text)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(QIcon(self.icon_path_0))
        self.setStyleSheet(self.default_style())
        self.unhovered.emit()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.setStyleSheet(self.pressed_style())
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.setStyleSheet(self.hover_style())
        super().mouseReleaseEvent(event)

    def default_style(self):
        return """
        QPushButton {
            background-color: #eee;
            border: 2px solid #aaa;
            border-radius: 10px;
        }
        """

    def hover_style(self):
        return """
        QPushButton {
            background-color: #ddd;
            border: 2px solid #888;
            border-radius: 10px;
        }
        """

    def pressed_style(self):
        return """
        QPushButton {
            background-color: #bbb;
            border: 2px solid #666;
            border-radius: 10px;
        }
        """
