from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QProgressBar, QLabel, QHBoxLayout, QGridLayout, QShortcut, QApplication
from PyQt5.QtCore import Qt, QTimer
from info_icon_button import InfoIconButton
from PyQt5.QtGui import QKeySequence
from pet_upgrade_manager import PetUpgradeManager
from poo import POO_TYPES

class PetControlPanel(QWidget):
    def __init__(self, pet):
        super().__init__()
        self.pet = pet
        self.upgrades = PetUpgradeManager(self)
        self.setWindowTitle("Control Panel")
        self.setFixedSize(1000, 600)
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
        self.setAttribute(Qt.WA_TranslucentBackground, True) # toggle transparent background for the control panel
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.space_shortcut = QShortcut(QKeySequence("Space"), self)
        self.space_shortcut.activated.connect(self.try_to_poop)
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Menu buttons
        menu_layout = QHBoxLayout()
        self.add_menu_buttons(menu_layout)
        layout.addLayout(menu_layout)

        # Bladder bar and XP bar
        self.poop_bar = self.create_bladder_bar()
        layout.addWidget(self.poop_bar)

        self.xp_bar = self.create_xp_bar()
        layout.addWidget(self.xp_bar)

        # Info label
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
        layout.addWidget(self.info_label)


        # Upgrade buttons at the top
        icons_layout = QHBoxLayout()
        self.add_upgrade_buttons(icons_layout)
        layout.addLayout(icons_layout)



        # Poop button
        self.poop_button = self.create_poop_button()
        layout.addWidget(self.poop_button)

        # Set the layout
        self.setLayout(layout)


        self.poop_refill_timer = QTimer(self)
        self.poop_refill_timer.timeout.connect(self.refill_poop_bar_in_time)
        self.poop_refill_timer.start(self.pet.bladder_refil_timer)
        self._drag_pos = None

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

    def add_upgrade_buttons(self, parent_layout):
        grid_layout = QGridLayout()
        buttons_info = [
            {
                "icon_0": "assets/lvl_butt1.png",
                "icon_1": "assets/lvl_butt0.png",
                "text_func": lambda: f"Level up Button: extend XP bar\nCurrent cost: {self.pet.max_xp}",
                "callback":self.upgrades.lvl_up,
            },
            {
                "icon_0": "assets/reg_butt0.png",
                "icon_1": "assets/reg_butt1.png",
                "text_func": lambda: f"Bladder auto refills \nCurrent cost: {self.pet.auto_poo_refill_upgrade_cost}",
                "callback": self.upgrades.reg_button,
            },
            {
                "icon_0": "assets/reg_time_butt0.png",
                "icon_1": "assets/reg_time_butt1.png",
                "text_func": lambda: f"Bladder regen speed \nCurrent cost: {self.pet.bladder_regen_speed_cost}",
                "callback": self.upgrades.reg_button_time,
            },
            {
                "icon_0": "assets/bladextend_butt0.png",
                "icon_1": "assets/bladextend_butt1.png",
                "text_func": lambda: f"More bladder storage \nCurrent cost: {self.pet.bladder_extend_cost}",
                "callback": self.upgrades.extend_bladder_capacity,
            },
            {
                "icon_0": "assets/less_bladder_use_to_poop_butt0.png",
                "icon_1": "assets/less_bladder_use_to_poop_butt1.png",
                "text_func": lambda: f"Less bladder used when pooping \nCurrent cost: {self.pet.less_bladder_use_cost}",
                "callback": self.upgrades.less_bladder_use,
            },
            {
                "icon_0": "assets/nutrition_up0.png",
                "icon_1": "assets/nutrition_up1.png",
                "text_func": lambda: f"Poop is more nutritious \nCurrent cost: {self.pet.poo_return_more_bladder_cost}",
                "callback": self.upgrades.poo_return_more_bladder,
            },
            {
                "icon_0": "assets/auto_poop_up0.png",
                "icon_1": "assets/auto_poop_up1.png",
                "text_func": lambda: f"Pet poops on its own \nCurrent cost: {self.pet.auto_poop_cost}",
                "callback": self.upgrades.auto_poop,
            },
            {
                "icon_0": "assets/double_poop_up1.png",
                "icon_1": "assets/double_poop_up0.png",
                "text_func": lambda: "Pet produces double the poop",
                "callback": self.double_poop_production
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
            row = index // 8
            col = index % 8
            grid_layout.addWidget(button, row, col)
        parent_layout.addLayout(grid_layout)



    def add_menu_buttons(self, parent_layout):
        outer_layout = QHBoxLayout()
        outer_layout.addStretch()
        grid_layout = QGridLayout()
        buttons_info = [
            {
                "icon_0": "assets/on_top0.png",
                "icon_1": "assets/on_top1.png",
                "text_func": lambda: "Panel always on top",
                "callback": self.panel_always_on_top
            },
            {
                "icon_0": "assets/minimize0.png",
                "icon_1": "assets/minimize1.png",
                "text_func": lambda: "minimise_panel",
                "callback": self.minimise_panel
            },
            {
                "icon_0": "assets/save_exit0.png",
                "icon_1": "assets/save_exit1.png",
                "text_func": lambda: "Save",
                "callback": self.save_exit
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
            row = index // 3
            col = index % 3
            grid_layout.addWidget(button, row, col)
        outer_layout.addLayout(grid_layout)
        parent_layout.addLayout(outer_layout)

    def minimise_panel(self):
        self.showMinimized()

    def panel_always_on_top(self):
        if not self.pet.always_on_top:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self.pet.always_on_top = True
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self.pet.always_on_top = False
        self.show()

    def double_poop_production(self):
        pass

    def save_exit(self):
        QApplication.quit()

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

    def reset_button_text(self):
        self.poop_button.setText("Poop")
        self.poop_button.setEnabled(True)

    def lock_button(self, duration_ms):
        self.poop_button.setEnabled(False)
        QTimer.singleShot(duration_ms, lambda: self.poop_button.setEnabled(True))

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