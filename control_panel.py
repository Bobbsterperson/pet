from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QProgressBar, QLabel, QHBoxLayout, QGridLayout
from PyQt5.QtCore import Qt, QTimer
from poo import POO_TYPES
from info_icon_button import InfoIconButton

class PetControlPanel(QWidget):
    def __init__(self, pet):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                background-color: #ffe5b4;  /* Light pastel blue-gray */
            }
        """)
        self.pet = pet
        self.setWindowTitle("Control Panel")
        self.setFixedSize(400, 800)
        self.poo_refill_upgrade_cost = 20
        self.max_xp = 100
        self.stored_overflow_xp = 0

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        self.poop_bar = self.create_bladder_bar()
        self.xp_bar = self.create_xp_bar()

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

        icons_layout = QHBoxLayout()
        self.add_icon_buttons(icons_layout)
        layout.addLayout(icons_layout)

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

    def add_icon_buttons(self, parent_layout):
        grid_layout = QGridLayout()
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
                "text": "Bladder auto reffils",
                "callback": self.reg_button
            },
            {
                "icon_0": "assets/reg_time_butt0.png",
                "icon_1": "assets/reg_time_butt1.png",
                "text": "Bladder regen faster",
                "callback": self.reg_button_time
            },
            {
                "icon_0": "assets/bladextend_butt0.png",
                "icon_1": "assets/bladextend_butt1.png",
                "text": "More bladder storage",
                "callback": self.estend_bladder_capacity
            },
            {
                "icon_0": "assets/less_bladder_use_to_poop_butt0.png",
                "icon_1": "assets/less_bladder_use_to_poop_butt1.png",
                "text": "Less bladder used when pooping",
                "callback": self.less_bladder_use
            },
            {
                "icon_0": "assets/nutrition_up0.png",
                "icon_1": "assets/nutrition_up1.png",
                "text": "Poop is more nutritious",
                "callback": self.poo_return_more_bladder
            },
            {
                "icon_0": "assets/auto_poop_up0.png",
                "icon_1": "assets/auto_poop_up1.png",
                "text": "Pet poops on its own",
                "callback": self.auto_poop
            },
            {
                "icon_0": "assets/double_poop_up0.png",
                "icon_1": "assets/double_poop_up1.png",
                "text": "Pet produces double the poop",
                "callback": self.double_poop_production
            },
            # {
            #     "icon_0": "assets/reg_butt0.png",
            #     "icon_1": "assets/reg_butt1.png",
            #     "text": "test increse XP 120",
            #     "callback": self.test_xpup
            # },

        ]
        for index, info in enumerate(buttons_info):
            button = InfoIconButton(info["icon_0"], info["icon_1"], info["text"])
            button.hovered.connect(self.update_info)
            button.unhovered.connect(self.clear_info)
            button.clicked.connect(info["callback"])

            row = index // 4
            col = index % 4
            grid_layout.addWidget(button, row, col)

        parent_layout.addLayout(grid_layout)

    # def test_xpup(self):
    #     overflow = self.increase_xp(120)
    #     if overflow > 0:
    #         self.stored_overflow_xp += overflow
    #         print(f"Overflow XP stored: {self.stored_overflow_xp}")

    def reg_button_time(self):
        pass
    def estend_bladder_capacity(self):
        pass
    def less_bladder_use(self):
        pass
    def poo_return_more_bladder(self):
        pass
    def auto_poop(self):
        pass
    def double_poop_production(self):
        pass

    def lvl_up(self):
        if self.xp_bar.value() < self.max_xp:
            self.info_label.setText("XP not full! Cannot level up.")
            return
        old_max = self.max_xp
        increased_max = int(old_max * 1.25) + self.stored_overflow_xp
        self.set_max_xp(increased_max)
        self.xp_bar.setValue(0)
        overflow_to_add = self.stored_overflow_xp
        self.stored_overflow_xp = 0
        leftover = self.increase_xp(overflow_to_add)
        if leftover > 0:
            self.stored_overflow_xp += leftover
        self.info_label.setText(f"Level Up! Max XP increased to {self.max_xp}.")

    def can_level_up(self):
        return self.xp_bar.value() >= self.max_xp

    def reg_button(self):
        current_xp = self.xp_bar.value()
        if current_xp >= self.poo_refill_upgrade_cost:
            self.xp_bar.setValue(current_xp - self.poo_refill_upgrade_cost)
            self.pet.poo_refil_time_value += 1
            print(f"Refill rate increased to {self.pet.poo_refil_time_value}")
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
            self.xp_bar.setValue(self.max_xp)
            return overflow
        else:
            self.xp_bar.setValue(total_xp)
            return 0

    def set_max_xp(self, new_max):
        self.max_xp = new_max
        self.xp_bar.setRange(0, new_max)
        if self.xp_bar.value() > new_max:
            self.xp_bar.setValue(new_max)
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
