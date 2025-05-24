from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QTimer, QDateTime, QPoint
import sip
from dataclasses import dataclass
from PyQt5.QtGui import QPixmap

@dataclass
class PooType:
    name: str
    sprite_count: int
    spawn_chance: float
    bladder_value_decrease: float
    bladder_value_return: float
    xp_value: int
    size: float
    growth_rate: float

    def __post_init__(self):
        self.sprites = [QPixmap(f"poo/{self.name}_{i}.png") for i in range(self.sprite_count)]

from dataclasses import dataclass
from PyQt5.QtGui import QPixmap

@dataclass
class PooType:
    name: str
    size: float
    sprites: list
    spawn_chance: float
    growth_rate: float
    bladder_value_decrease: int
    bladder_value_return: int
    xp_value: int
    min_level: int = 0

def get_poo_types():
    def load_sprites(name, count=4):
        return [QPixmap(f"poo/{name}_{i}.png") for i in range(count)]
    return {
        "normal": PooType("normal", 0.5, load_sprites("normal"), spawn_chance=1.0, growth_rate=0.0, bladder_value_decrease=20, bladder_value_return=20, xp_value=250, min_level=0),
        "weak": PooType("weak", 0.7, load_sprites("weak"), spawn_chance=0.5, growth_rate=0.01, bladder_value_decrease=25, bladder_value_return=25, xp_value=250, min_level=1),
        "runny": PooType("runny", 0.4, load_sprites("runny"), spawn_chance=0.3, growth_rate=0.015, bladder_value_decrease=35, bladder_value_return=7, xp_value=250, min_level=2),
        "hard": PooType("hard", 1.0, load_sprites("hard"), spawn_chance=0.25, growth_rate=0.02, bladder_value_decrease=25, bladder_value_return=25, xp_value=250, min_level=3),
        "corny": PooType("corny", 0.6, load_sprites("corny"), spawn_chance=0.2, growth_rate=0.015, bladder_value_decrease=35, bladder_value_return=35, xp_value=250, min_level=4),
        "chilly": PooType("chilly", 0.5, load_sprites("chilly"), spawn_chance=0.15, growth_rate=0.015, bladder_value_decrease=40, bladder_value_return=40, xp_value=250, min_level=5),
        "bloody": PooType("bloody", 0.7, load_sprites("bloody"), spawn_chance=0.12, growth_rate=0.015, bladder_value_decrease=30, bladder_value_return=30, xp_value=250, min_level=6),
        "toxic": PooType("toxic", 1.2, load_sprites("toxic"), spawn_chance=0.1, growth_rate=0.02, bladder_value_decrease=60, bladder_value_return=80, xp_value=250, min_level=7),
        "monster": PooType("monster", 1.5, load_sprites("monster"), spawn_chance=0.07, growth_rate=0.025, bladder_value_decrease=40, bladder_value_return=10, xp_value=250, min_level=8),
        "egg": PooType("egg", 0.8, load_sprites("egg"), spawn_chance=0.06, growth_rate=0.02, bladder_value_decrease=30, bladder_value_return=10, xp_value=14, min_level=250),
        "silver": PooType("silver", 1.1, load_sprites("silver"), spawn_chance=0.05, growth_rate=0.02, bladder_value_decrease=25, bladder_value_return=30, xp_value=250, min_level=10),
        "gold": PooType("gold", 1.3, load_sprites("gold"), spawn_chance=0.03, growth_rate=0.015, bladder_value_decrease=20, bladder_value_return=-10, xp_value=250, min_level=11),
    }

class Poo:
    def __init__(self, parent, poo_type: PooType, x, y):
        self.parent = parent
        self.poo_type = poo_type
        self.label = QLabel(None)
        self.spawn_time = QDateTime.currentMSecsSinceEpoch()
        self.is_deleted = False
        self.gravity_enabled = True
        self.velocity = 0
        self.is_held = False
        scale_factor = self.poo_type.size
        self.sprites = [
            sprite.scaled(
                int(sprite.width() * scale_factor),
                int(sprite.height() * scale_factor),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            for sprite in self.poo_type.sprites
        ]
        self.current_stage = 0
        self.label.setPixmap(self.sprites[self.current_stage])
        self.label.resize(self.sprites[0].size())
        self.label.move(x, y)
        self.label.setAttribute(Qt.WA_TranslucentBackground, True)
        self.label.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.label.show()
        self.idle_animation_timer = QTimer()
        self.idle_animation_timer.timeout.connect(self.update_idle_animation)
        self.idle_animation_timer.start(200)
        self.expiration_timer = QTimer()
        self.expiration_timer.setSingleShot(True)
        self.expiration_timer.timeout.connect(self.deleteLater)

    def update_idle_animation(self):
        if not self.is_valid() or not self.sprites:
            return
        self.current_stage = (self.current_stage + 1) % len(self.sprites)
        self.label.setPixmap(self.sprites[self.current_stage])

    def deleteLater(self):
        if self.label and not sip.isdeleted(self.label):
            if hasattr(self, "idle_animation_timer"):
                self.idle_animation_timer.stop()
            self.label.deleteLater()
            self.is_deleted = True

    def is_valid(self):
        return self.label is not None and not sip.isdeleted(self.label) and not self.is_deleted

    def apply_gravity(self):
        if self.is_held or not self.gravity_enabled or self.is_deleted:
            return
        new_y = self.label.y() + self.velocity
        self.velocity += 1
        ground = self.parent.screen.height() - self.label.height()
        if new_y >= ground:
            new_y = ground
            self.velocity = 0
        self.label.move(self.label.x(), new_y)

    def consume(self):
        if not self.is_deleted:
            self.deleteLater()
            return self.poo_type.bladder_value_return, self.poo_type.xp_value
        return 0, 0

    def intersects(self, pet_rect):
        return self.label.geometry().intersects(pet_rect)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_held = True

    def mouseMoveEvent(self, event):
        if self.is_held:
            self.label.move(event.globalPos() - QPoint(self.label.width() // 2, self.label.height() // 2))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_held = False
            self.velocity = 1

    def update_poo_gravity(self):
        for poo in self.poos:
            if not poo.is_deleted:
                poo.apply_gravity()



