from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QProgressBar, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from poo import POO_TYPES
from info_icon_button import InfoIconButton

class PetControlPanel(QWidget):
    def __init__(self, pet):
        super().__init__()
        self.pet = pet
        self.setWindowTitle("Control Panel")
        self.setFixedSize(400, 800)
        self.poo_refill_upgrade_cost = 20
        self.max_xp = 100
        self.stored_overflow_xp = 0

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # XP + Bladder Bars
        self.poop_bar = self.create_bladder_bar()
        self.xp_bar = self.create_xp_bar()

        # Info Label
        self.info_label = QLabel("")
        self.info_label.setFixedHeight(60)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #444;
                background-color: #f5f5f5;
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 4px;
            }
        """)
        layout.addWidget(self.poop_bar)
        layout.addWidget(self.xp_bar)
        layout.addWidget(self.info_label)

        # Icon Buttons Layout
        icons_layout = QHBoxLayout()
        self.add_icon_buttons(icons_layout)
        layout.addLayout(icons_layout)

        # Poop Button
        self.poop_button = self.create_poop_button()
        layout.addWidget(self.poop_button)

        self.setLayout(layout)

        self.poop_refill_timer = QTimer(self)
        self.poop_refill_timer.timeout.connect(self.refill_poop_bar_in_time)
        self.poop_refill_timer.start(self.pet.bladder_refil_timer)

    def create_bladder_bar(self):
        bar = QProgressBar()
        bar.setRange(0, 100)
        bar.setValue(100)
        bar.setTextVisible(True)
        bar.setFormat("Bladder: %p%")
        bar.setStyleSheet("""
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
        return bar

    def create_xp_bar(self):
        bar = QProgressBar()
        bar.setRange(0, self.max_xp)
        bar.setValue(0)
        bar.setTextVisible(True)
        bar.setFormat(f"XP: %v/%m")
        bar.setStyleSheet("""
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
        return bar


    def create_poop_button(self):
        button = QPushButton("Poop")
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(self.try_to_poop)
        button.setStyleSheet("""
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
        return button

    def add_icon_buttons(self, layout):
        buttons_info = [
            {
                "icon_0": "assets/lvl_butt1.png",
                "icon_1": "assets/lvl_butt0.png",
                "text": "level up Button: extend XP bar",
                "callback": self.lvl_up
            },
            {
                "icon_0": "assets/reg_butt0.png",
                "icon_1": "assets/reg_butt1.png",
                "text": "Bladder regen Button: Convert XP into bladder refill units",
                "callback": self.reg_button
            },
            {
                "icon_0": "assets/reg_butt0.png",
                "icon_1": "assets/reg_butt1.png",
                "text": "test increse XP 120",
                "callback": self.test_xpup
            },
            # Add more buttons here
        ]
        for info in buttons_info:
            button = InfoIconButton(info["icon_0"], info["icon_1"], info["text"])
            button.hovered.connect(self.update_info)
            button.unhovered.connect(self.clear_info)
            button.clicked.connect(info["callback"])
            layout.addWidget(button)

    def test_xpup(self):
        overflow = self.increase_xp(120)
        if overflow > 0:
            self.stored_overflow_xp += overflow
            print(f"Overflow XP stored: {self.stored_overflow_xp}")

    def lvl_up(self):
        if self.xp_bar.value() < self.max_xp:
            self.info_label.setText("XP not full! Cannot level up.")
            return

        old_max = self.max_xp
        print(f"Stored overflow XP before level up: {self.stored_overflow_xp}")
        print(f"Old max XP: {old_max}")

        # Increase max XP by 25%
        increased_max = int(old_max * 1.25) + self.stored_overflow_xp
        self.set_max_xp(increased_max)

        # Reset XP bar
        self.xp_bar.setValue(0)

        # Add stored overflow XP to the now-empty XP bar with new max
        overflow_to_add = self.stored_overflow_xp
        self.stored_overflow_xp = 0

        # Add overflow XP back to XP bar, store any further overflow
        leftover = self.increase_xp(overflow_to_add)
        if leftover > 0:
            self.stored_overflow_xp += leftover

        self.info_label.setText(f"Level Up! Max XP increased to {self.max_xp}.")
        print(f"Stored overflow XP after level up: {self.stored_overflow_xp}")
        print(f"Old max XP: {old_max}, New max XP: {self.max_xp}")



    def can_level_up(self):
        return self.xp_bar.value() >= self.max_xp

    def reg_button(self):
        current_xp = self.xp_bar.value()
        if current_xp >= self.poo_refill_upgrade_cost:
            self.xp_bar.setValue(current_xp - self.poo_refill_upgrade_cost)
            self.pet.poo_refil_time_value += 1  # Upgrade the refill rate
            print(f"Refill rate increased to {self.pet.poo_refil_time_value}")
            # Increase the cost exponentially or linearly (e.g., ×10 for next)
            self.poo_refill_upgrade_cost *= 50
            self.info_label.setText(f"Upgrade success! Next cost: {self.poo_refill_upgrade_cost} XP")
        else:
            self.info_label.setText(f"Need {self.poo_refill_upgrade_cost} XP! You have {current_xp}.")

    def update_info(self, text):
        self.info_label.setText(text)

    def clear_info(self):
        self.info_label.setText("")

    def refill_poop_bar_in_time(self):
        current = self.poop_bar.value()
        if current < 100:
            self.poop_bar.setValue(current + self.pet.poo_refil_time_value)

    def refill_poop_bar(self, amount):
        current = self.poop_bar.value()
        new_value = min(current + amount, 100)
        self.poop_bar.setValue(new_value)

    def increase_xp(self, amount):
        current_xp = self.xp_bar.value()
        total_xp = current_xp + amount

        if total_xp > self.max_xp:
            overflow = total_xp - self.max_xp
            self.xp_bar.setValue(self.max_xp)  # fill XP bar
            return overflow
        else:
            self.xp_bar.setValue(total_xp)
            return 0



    def set_max_xp(self, new_max):
        self.max_xp = new_max
        self.xp_bar.setRange(0, new_max)
        # Optionally reset current XP if it’s above the new max
        if self.xp_bar.value() > new_max:
            self.xp_bar.setValue(new_max)
        # Update format again if needed
        self.xp_bar.setFormat(f"XP: %v/{new_max}")

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
