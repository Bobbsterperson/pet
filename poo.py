from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QTimer, QDateTime, QPoint
import sip
from dataclasses import dataclass

@dataclass
class PooType:
    name: str
    sprites: list
    expiration_time: int
    bladder_value_decrese: int
    bladder_value_return: int
    xp_value: int
    size: float

POO_TYPES = {
    "normal": PooType("normal", [], 60000, 30, 10, 100, 0.5),
    "golden": PooType("golden", [], 90000, 20, 25, 20, 0.5),
    "spoiled": PooType("spoiled", [], 30000, 20, -5, 2, 0.5),
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
        self.update_stage_timer = QTimer()
        self.update_stage_timer.timeout.connect(self.update_expiration_stage)
        self.update_stage_timer.start(self.poo_type.expiration_time // 4)
        self.expiration_timer = QTimer()
        self.expiration_timer.setSingleShot(True)
        self.expiration_timer.timeout.connect(self.deleteLater)
        self.expiration_timer.start(self.poo_type.expiration_time)

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


    def update_expiration_stage(self):
        if not self.is_valid():
            return
        self.label.setPixmap(self.sprites[self.current_stage])

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



