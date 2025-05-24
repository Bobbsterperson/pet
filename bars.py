from PyQt5.QtWidgets import QProgressBar, QPushButton
from PyQt5.QtCore import Qt
from panel_stylesheets import bladder_bar, xp_bar, poop_btn

def create_bladder_bar(pet):
    bar = QProgressBar()
    bar.setRange(0, pet.bladder_bar_cap)
    bar.setValue(100)
    bar.setTextVisible(True)
    bar.setFormat("Bladder: %v/%m")
    bar.setStyleSheet(bladder_bar)

    def update_format(value):
        bar.setFormat(f"Bladder: {value}/{bar.maximum()}")

    bar.valueChanged.connect(update_format)
    return bar

def create_xp_bar(current_level, max_xp):
    bar = QProgressBar()
    bar.setRange(0, max_xp)
    bar.setValue(0)
    bar.setTextVisible(True)
    bar.setFormat(f"Level {current_level} | XP: %v/%m")
    bar.setStyleSheet(xp_bar)
    return bar

def create_poop_button(callback):
    button = QPushButton("Poop")
    button.setCursor(Qt.PointingHandCursor)
    button.clicked.connect(callback)
    button.setStyleSheet(poop_btn)
    return button
