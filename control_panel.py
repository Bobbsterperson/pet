from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QProgressBar, QLabel, QHBoxLayout, QGridLayout, QShortcut, QApplication, QDesktopWidget
from PyQt5.QtCore import Qt, QTimer
from info_icon_button import InfoIconButton
from PyQt5.QtGui import QKeySequence, QPixmap
from pet_upgrade_manager import PetUpgradeManager
from poo import get_poo_types
from PyQt5.QtWidgets import QSizePolicy
from sound import initialize_sounds
import random
from panel_stylesheets import panel, info_bar, bladder_bar, xp_bar, poop_btn, get_upgrade_btn, get_menu_btn, get_skill_btn, get_achievement_btn
from pet_cage import PetHabitatWidget

class PetControlPanel(QWidget):
    def __init__(self, pet):
        super().__init__()
        self.pet = pet
        self.upgrades = PetUpgradeManager(self)
        self.pet.sprite_changed.connect(self.update_pet_frame)
        self.current_level = 0
        self.POO_TYPES = get_poo_types()

        self.setWindowTitle("Pet stuff")
        self.setFixedSize(1000, 460)
        # self.setMinimumSize(1000, self.sizeHint().height())
        self.setStyleSheet(panel)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

        self.space_shortcut = QShortcut(QKeySequence("Space"), self)
        self.space_shortcut.activated.connect(self.try_to_poop)

        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Habitat widget — safely initialized and hidden by default
        # self.habitat_widget = PetHabitatWidget(self.pet)
        # self.habitat_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # self.habitat_widget.setMinimumHeight(160)
        # self.habitat_widget.setVisible(False)
        # layout.addWidget(self.habitat_widget)

        # Colored label widget
        # self.colored_label = QLabel("This is a colored label", self)
        # self.setMinimumSize(1000, self.sizeHint().height())
        # self.colored_label.setStyleSheet("background-color: #4682B4; color: white; font-size: 16px;")
        # self.colored_label.setAlignment(Qt.AlignCenter)
        # # self.colored_label.setVisible(False)
        # layout.addWidget(self.colored_label)

        # Menu buttons
        self.menu_buttons_widget = QWidget()
        menu_layout = QHBoxLayout(self.menu_buttons_widget)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.setSpacing(10)
        self.add_menu_buttons(menu_layout)
        layout.addWidget(self.menu_buttons_widget)

        # Insert bars container
        self.bars_container = QVBoxLayout()
        self.poop_bar = self.create_bladder_bar()
        self.bars_container.addWidget(self.poop_bar)
        self.xp_bar = self.create_xp_bar()
        self.bars_container.addWidget(self.xp_bar)
        layout.insertLayout(2, self.bars_container)

        # Upgrade buttons
        self.upgrades_widget = QWidget()
        upgrades_layout = QHBoxLayout(self.upgrades_widget)
        upgrades_layout.setContentsMargins(0, 0, 0, 0)
        upgrades_layout.setSpacing(10)
        self.add_upgrade_buttons(upgrades_layout)
        layout.addWidget(self.upgrades_widget)

        # Skills
        self.skills_widget = QWidget()
        skills_layout = QHBoxLayout(self.skills_widget)
        skills_layout.setContentsMargins(0, 0, 0, 0)
        skills_layout.setSpacing(10)
        self.add_skill_buttons(skills_layout)
        layout.addWidget(self.skills_widget)

        # Achievements
        self.achievements_widget = QWidget()
        self.achievements_layout = QHBoxLayout(self.achievements_widget)
        self.achievements_layout.setContentsMargins(0, 0, 0, 0)
        self.achievements_layout.setSpacing(10)
        self.add_achievements_buttons(self.achievements_layout)
        layout.addWidget(self.achievements_widget)

        self.achievements_widget.setVisible(False)
        self.skills_widget.setVisible(False)
        self.upgrades_widget.setVisible(False)

        # Info label
        self.info_label = QLabel("")
        self.info_label.setWordWrap(True)
        self.info_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.info_label.setMinimumHeight(self.pet.text_bar_size_min)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet(info_bar)
        layout.addWidget(self.info_label)

        # Poop button
        self.poop_button = self.create_poop_button()
        layout.addWidget(self.poop_button)

        # Finalize layout
        self.setLayout(layout)

        self.poop_refill_timer = QTimer(self)
        self.poop_refill_timer.timeout.connect(self.refill_poop_bar_in_time)
        self.poop_refill_timer.start(self.pet.bladder_refil_timer)

        self._drag_pos = None

        # Safely connect habitat update
        # self.pet.sprite_changed.connect(self.habitat_widget.update_pet_sprite)

    def create_bladder_bar(self):
        bar = QProgressBar()
        bar.setRange(0, self.pet.bladder_bar_cap)
        bar.setValue(100)
        bar.setTextVisible(True)
        bar.setFormat("Bladder: %v/%m")
        bar.setStyleSheet(bladder_bar)
        def update_format(value):
            bar.setFormat(f"Bladder: {value}/{bar.maximum()}")
        bar.valueChanged.connect(update_format)
        return bar

    def create_xp_bar(self):
        bar = QProgressBar()
        bar.setRange(0, self.pet.max_xp)
        bar.setValue(0)
        bar.setTextVisible(True)
        bar.setFormat(f"Level {self.current_level} | XP: %v/%m")
        bar.setStyleSheet(xp_bar)
        return bar

    def create_poop_button(self):
        button = QPushButton("Poop")
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(self.try_to_poop)
        button.setStyleSheet(poop_btn)
        return button

    def add_upgrade_buttons(self, parent_layout):
        buttons_info = get_upgrade_btn(self)
        self.add_buttons(parent_layout, buttons_info)

    def add_skill_buttons(self, parent_layout):
        buttons_info = get_skill_btn(self)
        self.add_buttons(parent_layout, buttons_info)

    def add_achievements_buttons(self, parent_layout):
        buttons_info = get_achievement_btn(self)
        self.add_buttons(parent_layout, buttons_info)

    def add_menu_buttons(self, parent_layout):
        buttons_info = get_menu_btn(self)
        self.pet_frame_label = QLabel()
        label_height = 114
        self.pet_frame_label.setFixedHeight(label_height)
        pet_pixmap = self.pet.get_current_pixmap()
        if pet_pixmap.isNull() or pet_pixmap.height() == 0:
            aspect_ratio = 1.0
            pet_pixmap = QPixmap(100, 100)  # placeholder empty pixmap of 100x100
        else:
            aspect_ratio = pet_pixmap.width() / pet_pixmap.height()
        label_width = int(label_height * aspect_ratio)
        self.pet_frame_label.setFixedWidth(label_width)
        self.pet_frame_label.setPixmap(pet_pixmap)
        self.pet_frame_label.setScaledContents(True)
        # Use a horizontal layout for spacing + grid layout + pet label
        extra_layout = QHBoxLayout()
        extra_layout.addSpacing(15)
        grid_layout = QGridLayout()
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
            row = index // 10
            col = index % 10
            grid_layout.addWidget(button, row, col)
        extra_layout.addLayout(grid_layout)
        extra_layout.addWidget(self.pet_frame_label)
        # Pass extra_layout to add_buttons
        self.add_buttons(parent_layout, [], add_extra_widget=extra_layout)

    def double_poop_production(self):
        pass

    def mute_sound(self):
        if self.pet.sound_volume == 0.0:
            self.pet.sound_volume = 0.2
        else:
            self.pet.sound_volume = 0.0
        initialize_sounds(self.pet)

    def hide_achievements(self):
        if hasattr(self, "achievements_widget"):
            is_visible = self.achievements_widget.isVisible()
            self.achievements_widget.setVisible(not is_visible)
            self.update_panel_size()
    
    def hide_skills(self):
        if hasattr(self, "skills_widget"):
            is_visible = self.skills_widget.isVisible()
            self.skills_widget.setVisible(not is_visible)
            self.update_panel_size()
    
    def hide_bars(self):
        visible = self.poop_bar.isVisible()
        self.poop_bar.setVisible(not visible)
        self.xp_bar.setVisible(not visible)
        self.info_label.setVisible(not visible)
        self.update_panel_size()

    def hide_upgrades(self):
        if hasattr(self, "upgrades_widget"):
            is_visible = self.upgrades_widget.isVisible()
            self.upgrades_widget.setVisible(not is_visible)
            self.update_panel_size()

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

    def save_exit(self):
        QApplication.quit()

    def update_info(self, text):
        self.info_label.setText(text)
        self.info_label.adjustSize()
        self.update_panel_size()  # if you want the whole panel to resize as well

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
        while amount > 0:
            current_xp = self.xp_bar.value()
            max_xp = self.pet.max_xp
            space_left = max_xp - current_xp
            if amount >= space_left:
                self.xp_bar.setValue(max_xp)
                amount -= space_left
                self.upgrades.lvl_up()  # this should update self.pet.current_level internally
                self.pet.change_pet_variant_on_level()  # update variant immediately after level up
            else:
                self.xp_bar.setValue(current_xp + amount)
                amount = 0

    def set_max_xp(self, new_max):
        self.pet.max_xp = new_max
        self.xp_bar.setRange(0, new_max)
        if self.xp_bar.value() > new_max:
            self.xp_bar.setValue(new_max)
        self.xp_bar.setFormat(f"Level {self.current_level} | XP: %v/{new_max}")

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

    def try_to_poop(self, poo_type=None):
        if self.pet.gravity_timer.isActive() or self.pet.is_dragging:
            self.poop_button.setText("Can't poop in air")
            self.poop_button.setEnabled(False)
            QTimer.singleShot(1500, self.reset_button_text)
            return
        elif self.pet.is_pooping or self.pet.is_eating:
            self.poop_button.setText("Can't poop right now")
            self.poop_button.setEnabled(False)
            QTimer.singleShot(1500, self.reset_button_text)
            return
        # elif self.pet.is_hidden:
        #     self.poop_button.setText("Can't poop in cage")
        #     self.poop_button.setEnabled(False)
        #     QTimer.singleShot(1500, self.reset_button_text)
        #     return
        if self.poop_button.isEnabled():
            poo_type = self.get_random_poo_type()
            if self.poop_bar.value() >= poo_type.bladder_value_decrease:
                self.poop_bar.setValue(int(self.poop_bar.value() - poo_type.bladder_value_decrease))
                self.pet.poop(poo_type)
                self.lock_button(1000)
            else:
                self.poop_button.setText("Too tired to poop")
                self.poop_button.setEnabled(False)

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

    def update_panel_size(self):
        base_width = 1000
        total_height = 0
        layout = self.layout()
        spacing = layout.spacing()
        margins = layout.contentsMargins()
        total_height += margins.top() + margins.bottom()
        def add_widget_height(widget, is_first=False):
            nonlocal total_height
            if widget and widget.isVisible():
                if not is_first:
                    total_height += spacing
                total_height += widget.sizeHint().height()
        widgets_in_order = [
            self.menu_buttons_widget if hasattr(self, 'menu_buttons_widget') else None,
            self.poop_bar,
            self.xp_bar,
            self.info_label,
            self.upgrades_widget if hasattr(self, 'upgrades_widget') else None,
            self.skills_widget if hasattr(self, 'skills_widget') else None,
            self.achievements_widget if hasattr(self, 'achievements_widget') else None,
            # self.habitat_widget if hasattr(self, 'habitat_widget') else None,
            self.poop_button
        ]
        first_visible_found = False
        for w in widgets_in_order:
            if w and w.isVisible():
                # print(f"Widget {w} sizeHint: {w.sizeHint()}")
                add_widget_height(w, is_first=not first_visible_found)
                first_visible_found = True
        # Enforce minimum/maximum height limits if necessary
        min_height = 200
        screen_height = self.get_screen_height()
        max_height = int(screen_height * 0.95)
        frame_height_margin = 40

        final_height = max(min_height, min(total_height + frame_height_margin, max_height))

        self.setMinimumSize(base_width, final_height)
        self.resize(base_width, final_height)  # explicitly resize after setting minimum

    def update_pet_frame(self):
        pet_pixmap = self.pet.get_current_pixmap()
        if pet_pixmap and not pet_pixmap.isNull() and pet_pixmap.height() > 0:
            label_height = self.pet_frame_label.height()
            aspect_ratio = pet_pixmap.width() / pet_pixmap.height()
            label_width = int(label_height * aspect_ratio)
            self.pet_frame_label.setFixedWidth(label_width)
            scaled_pixmap = pet_pixmap.scaled(
                label_width, label_height, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.pet_frame_label.setPixmap(scaled_pixmap)



    def add_buttons(self, parent_layout, buttons_info, add_extra_widget=None):
        outer_layout = QHBoxLayout()
        outer_layout.addStretch()
        grid_layout = QGridLayout()
        self.upgrade_buttons = []
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
            self.upgrade_buttons.append((button, text_func))
            row = index // 10
            col = index % 10
            grid_layout.addWidget(button, row, col)
        outer_layout.addLayout(grid_layout)
        if add_extra_widget:
            outer_layout.addLayout(add_extra_widget)
        parent_layout.addLayout(outer_layout)

    def refresh_upgrade_texts(self):
        for button, text_func in getattr(self, 'upgrade_buttons', []):
            if text_func:
                button.setText(text_func())

    def get_random_poo_type(self):
        eligible_poo_types = {
            key: poo for key, poo in self.POO_TYPES.items()
            if self.current_level >= poo.min_level
        }
        adjusted_chances = {
            key: poo.spawn_chance + poo.spawn_chance_grow_per_level
            for key, poo in eligible_poo_types.items()
        }
        total = sum(adjusted_chances.values())
        if total == 0:
            return self.POO_TYPES["normal"]
        r = random.uniform(0, total)
        upto = 0
        for key, chance in adjusted_chances.items():
            upto += chance
            if r <= upto:
                return self.POO_TYPES[key]
        return self.POO_TYPES["normal"]


    def weak_achievement(self):
        if not hasattr(self, "achievements_widget"):
            return
        self.update_info("Weak achievement unlocked! Keep going!")

    def achievement_stats(self, poo_type_key):
        if not hasattr(self, "achievements_widget"):
            return
        poo_types = self.pet.POO_TYPES
        if poo_type_key not in poo_types:
            self.update_info("Unknown achievement")
            return
        poo = poo_types[poo_type_key]
        stats = (
            f"Name: {poo.name}                                          Size: {poo.size}\n"
            f"Spawn Chance: {poo.spawn_chance} >>>----------->>> per lvl: {poo.spawn_chance_grow_per_level}\n"
            f"Bladder Decrease: {poo.bladder_value_decrease}              Bladder Return: {poo.bladder_value_return}\n"
            f"XP Value: {poo.xp_value}                           Minimum Level: {poo.min_level}"
        )
        self.update_info(stats)
        self.info_label.adjustSize()

    def clear_achievement_buttons(self):
        self.pet.achievement_get() #maybe it wont be here
        self.clear_layout(self.achievements_layout)

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                    widget.deleteLater()
                elif item.layout():
                    self.clear_layout(item.layout())

    @staticmethod
    def get_screen_height():
        screen = QDesktopWidget().availableGeometry()
        return screen.height()

