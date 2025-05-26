from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
import random
from poo import get_poo_types

def initialize_sprites(self):
    if not hasattr(self, 'label'):
        self.label = QLabel(self)
        self.label.show()

    POO_TYPES = get_poo_types()

    self.sprites = {}

    actions = ["walk", "idle", "shiv", "poop", "eat", "achievement"]
    for action in actions:
        self.sprites[action] = [
            QPixmap(f"assets/pet/{action}{self.sprite_variant}{i}.png") for i in range(4)
        ]

    self.label.setPixmap(self.sprites["idle"][0])
    self.label.resize(self.label.pixmap().size())  # <-- Add this
    self.resize(self.label.size())                  # <-- And this, to fit the label

    for name, poo_type in POO_TYPES.items():
        poo_type.sprites = [QPixmap(f"assets/poo/{name}_{i}.png") for i in range(4)]

    self.poo_type = POO_TYPES["normal"]

    self.direction = random.choice(["left", "right"])
    self.frame = 0
    self.is_walking = True
    self.is_dragging = False
    self.old_pos = None
    self.velocity_y = 0

    if not hasattr(self, 'spawned_poo'):
        self.spawned_poo = []
