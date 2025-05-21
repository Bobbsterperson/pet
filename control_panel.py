from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QProgressBar, QLabel, QHBoxLayout, QGridLayout, QShortcut
from PyQt5.QtCore import Qt, QTimer

from poo import POO_TYPES
from info_icon_button import InfoIconButton
from PyQt5.QtGui import QKeySequence
from dataclasses import replace

class PetControlPanel(QWidget):
    def __init__(self, pet):
        super().__init__()
        self.pet = pet
        self.setWindowTitle("Control Panel")
        self.setFixedSize(600, 1000)
        
        self.setStyleSheet("""
            QWidget {
                background-color: transparent;
                color: white;
                font-family: 'Comic Sans MS', 'Arial', sans-serif;
            }

            QLabel {
                background-color: transparent;
                color: white;
            }

            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border: 1px solid white;
                border-radius: 5px;
                padding: 4px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }

            QProgressBar {
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid white;
                border-radius: 5px;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: rgba(0, 255, 255, 0.5);
            }
        """)

        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.space_shortcut = QShortcut(QKeySequence("Space"), self)
        self.space_shortcut.activated.connect(self.try_to_poop)
        layout = QVBoxLayout()
        layout.setSpacing(20)
        self.poop_bar = self.create_bladder_bar()
        self.xp_bar = self.create_xp_bar()
        self.info_label = QLabel("")
        self.info_label.setFixedHeight(self.pet.text_bar_size)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                color: #ffffff;
                background-color: rgba(0, 0, 0, 0.5);
                border: 2px dashed #ff66cc;
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

        self._drag_pos = None  # Store drag start position

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self._drag_pos:
            self.move(event.globalPos() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None
        event.accept()

    def create_bladder_bar(self):
        bar = QProgressBar()
        bar.setRange(0, self.pet.bladder_bar_cap)
        bar.setValue(100)
        bar.setTextVisible(True)
        bar.setFormat("Bladder: %v/%m")
        bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #ffffff;
                border-radius: 10px;
                text-align: center;
                font-weight: bold;
                font-size: 18px;
                color: #ff00ff;
                height: 45px;
                background-color: rgba(0, 0, 0, 0.3);
            }
            QProgressBar::chunk {
                background-color: #39ff14;
                border-radius: 10px;
            }
        """)
        def update_format(value):
            bar.setFormat(f"Bladder: {value}/{bar.maximum()}")
        bar.valueChanged.connect(update_format)
        return bar

    def create_xp_bar(self):
        bar = QProgressBar()
        bar.setRange(0, self.pet.max_xp)
        bar.setValue(0)
        bar.setTextVisible(True)
        bar.setFormat("XP: %v/%m")
        bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #ffffff;
                border-radius: 10px;
                text-align: center;
                font-weight: bold;
                font-size: 18px;
                height: 45px;
                background-color: rgba(0, 0, 0, 0.3);
            }
            QProgressBar::chunk {
                background-color: #00bfff;
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
                background-color: #ff1493;
                color: white;
                font-size: 20px;
                font-weight: bold;
                border: 3px double white;
                border-radius: 15px;
                padding: 10px;

            }
            QPushButton:hover {
                background-color: #ff69b4;
            }
            QPushButton:pressed {
                background-color: #c71585;
            }
        """)
        return button

    def add_icon_buttons(self, parent_layout):
        grid_layout = QGridLayout()
        buttons_info = [
            {
                "icon_0": "assets/lvl_butt1.png",
                "icon_1": "assets/lvl_butt0.png",
                "text_func": lambda: f"Level up Button: extend XP bar\nCurrent cost: {self.pet.max_xp}",
                "callback": self.lvl_up
            },
            {
                "icon_0": "assets/reg_butt0.png",
                "icon_1": "assets/reg_butt1.png",
                "text_func": lambda: f"Bladder auto refills \nCurrent cost: {self.pet.auto_poo_refill_upgrade_cost}",
                "callback": self.reg_button
            },
            {
                "icon_0": "assets/reg_time_butt0.png",
                "icon_1": "assets/reg_time_butt1.png",
                "text_func": lambda: f"Bladder regen speed \nCurrent cost: {self.pet.bladder_regen_speed_cost}",
                "callback": self.reg_button_time
            },
            {
                "icon_0": "assets/bladextend_butt0.png",
                "icon_1": "assets/bladextend_butt1.png",
                "text_func": lambda: f"More bladder storage \nCurrent cost: {self.pet.bladder_extend_cost}",
                "callback": self.extend_bladder_capacity
            },
            {
                "icon_0": "assets/less_bladder_use_to_poop_butt0.png",
                "icon_1": "assets/less_bladder_use_to_poop_butt1.png",
                "text_func": lambda: f"Less bladder used when pooping \nCurrent cost: {self.pet.less_bladder_use_cost}",
                "callback": self.less_bladder_use
            },
            {
                "icon_0": "assets/nutrition_up0.png",
                "icon_1": "assets/nutrition_up1.png",
                "text_func": lambda: f"Poop is more nutritious \nCurrent cost: {self.pet.poo_return_more_bladder_cost}",
                "callback": self.poo_return_more_bladder
            },
            {
                "icon_0": "assets/auto_poop_up0.png",
                "icon_1": "assets/auto_poop_up1.png",
                "text_func": lambda: f"Pet poops on its own \nCurrent cost: {self.pet.auto_poop_cost}",
                "callback": self.auto_poop
            },
            {
                "icon_0": "assets/double_poop_up1.png",
                "icon_1": "assets/double_poop_up0.png",
                "text_func": lambda: "Pet produces double the poop",
                "callback": self.double_poop_production
            },
            {
                "icon_0": "assets/toggle_window0.png",
                "icon_1": "assets/toggle_window1.png",
                "text_func": lambda: "Move pet from screen to island",
                "callback": self.toggle_window
            },
        ]
        for index, info in enumerate(buttons_info):
            initial_text = info.get("text", "")
            button = InfoIconButton(info["icon_0"], info["icon_1"], initial_text)
            text_func = info.get("text_func")
            if text_func:
                button.hovered.connect(lambda _, f=text_func: self.update_info(f()))
            else:
                button.hovered.connect(lambda _, t=initial_text: self.update_info(t))
            button.unhovered.connect(self.clear_info)
            button.clicked.connect(info["callback"])
            row = index // 4
            col = index % 4
            grid_layout.addWidget(button, row, col)
        parent_layout.addLayout(grid_layout)

    def double_poop_production(self):
        pass
    def toggle_window(self):
        pass

    def lvl_up(self):
        if self.xp_bar.value() < self.pet.max_xp:
            self.info_label.setText("XP not full! Cannot level up.")
            return
        old_max = self.pet.max_xp
        new_max = int(old_max * 1.45)
        self.set_max_xp(new_max)
        self.xp_bar.setValue(0)
        self.increase_xp(self.pet.stored_overflow_xp)
        self.pet.stored_overflow_xp = 0
        self.info_label.setText(f"Level Up! Max XP increased to {self.pet.max_xp}.")

    def reg_button(self):
        current_xp = self.xp_bar.value()
        if current_xp >= self.pet.auto_poo_refill_upgrade_cost:
            self.xp_bar.setValue(current_xp - self.pet.auto_poo_refill_upgrade_cost)
            self.pet.poo_units_refil_time_value += 1
            self.pet.auto_poo_refill_upgrade_cost *= 50
            self.info_label.setText(f"Upgrade success! Next cost: {self.pet.auto_poo_refill_upgrade_cost} XP")
        else:
            self.info_label.setText(f"Need {self.pet.auto_poo_refill_upgrade_cost} XP! You have {current_xp}.")

    def reg_button_time(self):
        current_xp = self.xp_bar.value()
        if current_xp >= self.pet.bladder_regen_speed_cost:
            self.xp_bar.setValue(current_xp - self.pet.bladder_regen_speed_cost)
            self.pet.bladder_refil_timer -= 100
            self.pet.bladder_regen_speed_cost *= 30
            self.info_label.setText(f"Upgrade success! Next cost: {self.pet.bladder_regen_speed_cost} XP")
        else:
            self.info_label.setText(f"Need {self.pet.bladder_regen_speed_cost} XP! You have {current_xp}.")

    def extend_bladder_capacity(self):
        current_xp = self.xp_bar.value()
        if current_xp >= self.pet.bladder_extend_cost:
            self.xp_bar.setValue(current_xp - self.pet.bladder_extend_cost)   
            old_cap = self.pet.bladder_bar_cap
            new_cap = int(old_cap * 1.1)
            self.set_max_bladder(new_cap)
            self.pet.bladder_extend_cost *= 30
            self.info_label.setText(f"Bladder extended to {new_cap}. Next upgrade: {self.pet.bladder_extend_cost} XP")
        else:
            self.info_label.setText(f"Need {self.pet.bladder_extend_cost} XP! You have {current_xp}.")

    def less_bladder_use(self):
        current_xp = self.xp_bar.value()
        if current_xp >= self.pet.less_bladder_use_cost:
            self.xp_bar.setValue(current_xp - self.pet.less_bladder_use_cost)
            normal_poo = POO_TYPES["normal"]
            new_decrese_value = max(normal_poo.bladder_value_decrese - 1, 0)
            POO_TYPES["normal"] = replace(normal_poo, bladder_value_decrese=new_decrese_value)
            self.pet.less_bladder_use_cost *= 50
            self.info_label.setText(f"Upgrade success! Next cost: {self.pet.less_bladder_use_cost} XP")
        else:
            self.info_label.setText(f"Need {self.pet.less_bladder_use_cost} XP! You have {current_xp}.")
   
    def poo_return_more_bladder(self):
        current_xp = self.xp_bar.value()
        if current_xp >= self.pet.poo_return_more_bladder_cost:
            self.xp_bar.setValue(current_xp - self.pet.poo_return_more_bladder_cost)
            normal_poo = POO_TYPES["normal"]
            new_return_value = normal_poo.bladder_value_return + 1
            POO_TYPES["normal"] = replace(normal_poo, bladder_value_return=new_return_value)
            self.pet.poo_return_more_bladder_cost *= 50
            self.info_label.setText(f"Upgrade success! Next cost: {self.pet.poo_return_more_bladder_cost} XP")
        else:
            self.info_label.setText(f"Need {self.pet.poo_return_more_bladder_cost} XP! You have {current_xp}.")

    def auto_poop(self):
        current_xp = self.xp_bar.value()
        if current_xp >= self.pet.auto_poop_cost:
            self.xp_bar.setValue(current_xp - self.pet.auto_poop_cost)
            if not self.pet.poop_auto_timer.isActive():
                self.pet.poop_auto_timer.start(self.pet.auto_poop_interval)
            else:
                self.auto_poop_interval = max(2500, self.pet.auto_poop_interval - 100)
                self.pet.poop_auto_timer.start(self.pet.auto_poop_interval)
            self.pet.auto_poop_cost *= 50
            self.info_label.setText(f"Upgrade success! Next cost: {self.pet.auto_poop_cost} XP")
        else:
            self.info_label.setText(f"Need {self.pet.auto_poop_cost} XP! You have {current_xp}.")

    def update_info(self, text):
        self.info_label.setText(text)

    def clear_info(self):
        self.info_label.setText("")

    def refill_poop_bar_in_time(self):
        current = self.poop_bar.value()
        if current < self.pet.bladder_bar_cap:
            self.poop_bar.setValue(current + self.pet.poo_units_refil_time_value)

    def refill_poop_bar(self, amount):
        current = self.poop_bar.value()
        new_value = min(current + amount, 100)
        self.poop_bar.setValue(new_value)

    def increase_xp(self, amount):
        current_xp = self.xp_bar.value()
        total_xp = current_xp + amount

        if total_xp > self.pet.max_xp:
            overflow = total_xp - self.pet.max_xp
            self.xp_bar.setValue(self.pet.max_xp)
            self.pet.stored_overflow_xp += overflow
            return 0
        else:
            self.xp_bar.setValue(total_xp)
            return 0

    def set_max_xp(self, new_max):
        self.pet.max_xp = new_max
        self.xp_bar.setRange(0, new_max)
        if self.xp_bar.value() > new_max:
            self.xp_bar.setValue(new_max)
        self.xp_bar.setFormat(f"XP: %v/{new_max}")

    def set_max_bladder(self, new_max_b):
        self.pet.bladder_bar_cap = new_max_b
        self.poop_bar.setRange(0, new_max_b)
        if self.poop_bar.value() > new_max_b:
            self.poop_bar.setValue(new_max_b)
        self.poop_bar.setFormat(f"Bladder: %v/{new_max_b}")

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
