from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QProgressBar
from PyQt5.QtCore import Qt, QTimer 
from poo import Poo, POO_TYPES

class PetControlPanel(QWidget):
    def __init__(self, pet):
        super().__init__()
        self.pet = pet
        self.setWindowTitle("Control Panel")
        self.setFixedSize(400, 800)

        # Layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Poop Button
        self.poop_button = QPushButton("Poop")
        self.poop_button.setCursor(Qt.PointingHandCursor)
        self.poop_button.clicked.connect(self.try_to_poop)
        self.poop_button.setStyleSheet("""
            QPushButton {
                background-color: #FFB347;
                color: #333;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                border-radius: 12px;
                border: 2px solid #e69500;
            }
            QPushButton:hover {
                background-color: #FFD580;
            }
            QPushButton:pressed {
                background-color: #e69500;
            }
        """)
        layout.addWidget(self.poop_button)

        # Poop Energy Bar
        self.poop_bar = QProgressBar()
        self.poop_bar.setRange(0, 100)
        self.poop_bar.setValue(100)
        self.poop_bar.setTextVisible(True)
        self.poop_bar.setFormat("Bladder: %p%")
        self.poop_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #ccc;
                border-radius: 10px;
                text-align: center;
                font-weight: bold;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #76c893;
                border-radius: 10px;
            }
        """)
        layout.addWidget(self.poop_bar)
        self.poop_refill_timer = QTimer(self)
        self.poop_refill_timer.timeout.connect(self.refill_poop_bar_in_time) # not used yet
        self.poop_refill_timer.start(self.pet.bladder_refil_timer) 

        self.xp_bar = QProgressBar()
        self.xp_bar.setRange(0, 100)
        self.xp_bar.setValue(0)
        self.xp_bar.setTextVisible(True)
        self.xp_bar.setFormat("XP: %p%")
        self.xp_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #ccc;
                border-radius: 10px;
                text-align: center;
                font-weight: bold;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #4682B4;
                border-radius: 10px;
            }
        """)
        layout.addWidget(self.xp_bar)

        self.setLayout(layout)

    def refill_poop_bar_in_time(self):  # not used yet
        current = self.poop_bar.value()
        if current < 100:
            self.poop_bar.setValue(current + self.pet.poo_refil_time_value)

    def refill_poop_bar(self, amount):
        current = self.poop_bar.value()
        new_value = current + amount
        if new_value > 100:
            new_value = 100
        self.poop_bar.setValue(new_value)

    def increase_xp(self, amount):
        """
        This function increases the XP bar by a specified amount.
        :param amount: The amount to increase the XP by (1 to 100).
        """
        current_xp = self.xp_bar.value()
        new_xp = current_xp + amount
        if new_xp > 100:
            new_xp = 100
        self.xp_bar.setValue(new_xp)

    def try_to_poop(self):
        if self.pet.gravity_timer.isActive() or self.pet.is_dragging:
            self.poop_button.setText("Can't poop in air")
            self.poop_button.setEnabled(False)
            QTimer.singleShot(1500, self.reset_button_text)
            return
        if self.poop_button.isEnabled():
            if self.poop_bar.value() >= POO_TYPES["normal"].bladder_value_decrese:
                self.poop_bar.setValue(self.poop_bar.value() - POO_TYPES["normal"].bladder_value_decrese)
                self.pet.poop()
                self.lock_button(1000)
            else:
                self.poop_button.setText("Too tired to poop")
                self.poop_button.setEnabled(False)
                QTimer.singleShot(1500, self.reset_button_text)

    def reset_button_text(self):
        self.poop_button.setText("Poop")
        self.poop_button.setEnabled(True)

    def lock_button(self, duration_ms):
        self.poop_button.setEnabled(False)
        QTimer.singleShot(duration_ms, lambda: self.poop_button.setEnabled(True))
