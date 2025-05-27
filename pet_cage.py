from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class PetHabitatWidget(QWidget):
    def __init__(self, pet):
        super().__init__()
        self.pet = pet
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(160, 160)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 30); border: 1px solid gray; border-radius: 8px;")
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.update_pet_sprite(self.pet.get_current_pixmap())

    def update_pet_sprite(self, pixmap: QPixmap):
        if pixmap is not None and not pixmap.isNull():
            scaled = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label.setPixmap(scaled)
        else:
            print("Warning: Tried to update PetHabitatWidget with null QPixmap.")
            self.label.clear()  # Optionally clear if invalid

