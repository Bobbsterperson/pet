from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from info_icon_button import InfoIconButton
from panel_stylesheets import get_upgrade_btn, get_skill_btn, get_achievement_btn, get_menu_btn

def add_buttons(target_widget, buttons_info, update_info_callback, clear_info_callback, add_extra_widget=None):
    from PyQt5.QtWidgets import QHBoxLayout, QGridLayout

    outer_layout = QHBoxLayout()
    outer_layout.addStretch()
    grid_layout = QGridLayout()

    upgrade_buttons = []

    for index, info in enumerate(buttons_info):
        initial_text = info.get("text", "")
        button = InfoIconButton(info["icon_0"], info["icon_1"], initial_text)
        text_func = info.get("text_func")

        if text_func:
            button.hovered.connect(lambda _, f=text_func: update_info_callback(f()))
        else:
            button.hovered.connect(lambda _, t=initial_text: update_info_callback(t))

        button.unhovered.connect(clear_info_callback)
        button.clicked.connect(info["callback"])

        upgrade_buttons.append((button, text_func))

        row = index // 10
        col = index % 10
        grid_layout.addWidget(button, row, col)

    outer_layout.addLayout(grid_layout)

    if add_extra_widget:
        outer_layout.addLayout(add_extra_widget)

    target_widget.addLayout(outer_layout)

    return upgrade_buttons


def add_upgrade_buttons(panel, parent_layout):
    buttons_info = get_upgrade_btn(panel)
    panel.upgrade_buttons = add_buttons(parent_layout, buttons_info, panel.update_info, panel.clear_info)


def add_skill_buttons(panel, parent_layout):
    buttons_info = get_skill_btn(panel)
    add_buttons(parent_layout, buttons_info, panel.update_info, panel.clear_info)


def add_achievements_buttons(panel, parent_layout):
    buttons_info = get_achievement_btn(panel)
    add_buttons(parent_layout, buttons_info, panel.update_info, panel.clear_info)


def add_menu_buttons(panel, parent_layout):
    buttons_info = get_menu_btn(panel)
    pet_frame_label = QLabel()
    panel.pet_frame_label = pet_frame_label
    label_height = 114
    pet_frame_label.setFixedHeight(label_height)

    pet_pixmap = panel.pet.get_current_pixmap()
    if pet_pixmap.isNull() or pet_pixmap.height() == 0:
        pet_pixmap = QPixmap(100, 100)
        aspect_ratio = 1.0
    else:
        aspect_ratio = pet_pixmap.width() / pet_pixmap.height()

    label_width = int(label_height * aspect_ratio)
    pet_frame_label.setFixedWidth(label_width)
    pet_frame_label.setPixmap(pet_pixmap)
    pet_frame_label.setScaledContents(True)

    extra_layout = QHBoxLayout()
    extra_layout.addSpacing(15)
    grid_layout = QGridLayout()

    for index, info in enumerate(buttons_info):
        initial_text = info.get("text", "")
        button = InfoIconButton(info["icon_0"], info["icon_1"], initial_text)
        text_func = info.get("text_func")
        if text_func:
            button.hovered.connect(lambda _, f=text_func: panel.update_info(f()))
        else:
            button.hovered.connect(lambda _, t=initial_text: panel.update_info(t))
        button.unhovered.connect(panel.clear_info)
        button.clicked.connect(info["callback"])

        row = index // 10
        col = index % 10
        grid_layout.addWidget(button, row, col)

    extra_layout.addLayout(grid_layout)
    extra_layout.addWidget(pet_frame_label)

    add_buttons(parent_layout, [], panel.update_info, panel.clear_info, add_extra_widget=extra_layout)
