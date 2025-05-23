from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
import random
from poo import get_poo_types

def initialize_sprites(self):
    self.label = QLabel(self)

    POO_TYPES = get_poo_types()

    self.sprites = {}

    actions = ["walk", "idle", "shiv", "poop", "eat"]
    for action in actions:
        self.sprites[action] = [
            QPixmap(f"pet/{action}{self.sprite_variant}{i}.png") for i in range(4)
        ]

    # Now that sprites exist, set pixmap on label
    self.label.setPixmap(self.sprites["idle"][0])  # Ensure something is shown
    self.label.show()  

    for name, poo_type in POO_TYPES.items():
        poo_type.sprites = [QPixmap(f"poo/{name}_{i}.png") for i in range(4)]

    self.poo_type = POO_TYPES["normal"]

    # State defaults
    self.direction = random.choice(["left", "right"])
    self.frame = 0
    self.is_walking = True
    self.is_dragging = False
    self.old_pos = None
    self.velocity_y = 0
    self.spawned_poo = []

def set_sprite_variant(self, variant):
    self.sprite_variant = variant
    initialize_sprites(self)  # Re-initialize with the new variant
