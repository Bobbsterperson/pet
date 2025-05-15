import sip
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QTimer, QDateTime, Qt
from PyQt5.QtGui import QPixmap


class Poo:
    def __init__(self, parent, pixmap, x, y, scale_factor=0.5, depletion_amount=15):
        self.parent = parent
        self.label = QLabel(None)
        self.depletion_amount = depletion_amount
        self.spawn_time = QDateTime.currentMSecsSinceEpoch()
        self.is_deleted = False

        scaled_poo = pixmap.scaled(
            int(pixmap.width() * scale_factor),
            int(pixmap.height() * scale_factor),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.label.setPixmap(scaled_poo)
        self.label.resize(scaled_poo.size())
        self.label.move(x, y)
        self.label.setAttribute(Qt.WA_TranslucentBackground, True)
        self.label.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.label.show()

        QTimer.singleShot(100000, self.deleteLater)

    def is_valid(self):
        return self.label and not sip.isdeleted(self.label)

    def deleteLater(self):
        if self.is_valid():
            self.label.deleteLater()
            self.is_deleted = True

    def intersects(self, pet_rect):
        return self.label.geometry().intersects(pet_rect)
