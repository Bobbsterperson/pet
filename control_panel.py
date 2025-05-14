from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QProgressBar
from PyQt5.QtCore import Qt, QTimer

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

        self.setLayout(layout)

        # Timer to refill bar
        self.poop_timer = QTimer(self)
        self.poop_timer.timeout.connect(self.refill_poop_bar)
        self.poop_timer.start(1000)  # every second

    def refill_poop_bar(self):
        current = self.poop_bar.value()
        if current < 100:
            self.poop_bar.setValue(current + 1)

    def try_to_poop(self):
        if self.poop_button.isEnabled():  # ensure it's not already locked
            if self.poop_bar.value() >= 15:
                self.poop_bar.setValue(self.poop_bar.value() - 15)
                self.pet.poop()
                self.lock_button(1000)  # lock button for 1 second
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
