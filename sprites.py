from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
import random
from poo import POO_TYPES

def initialize_sprites(self):
    self.label = QLabel(self)
    self.sprites = {
        "walk": [QPixmap(f"assets/walk{i}.png") for i in range(4)],
        "idle": [QPixmap(f"assets/idle{i}.png") for i in range(4)],
        "shiv": [QPixmap(f"assets/shiv{i}.png") for i in range(4)],
        "poop": [QPixmap(f"assets/poop{i}.png") for i in range(4)],
        "eat": [QPixmap(f"assets/eat{i}.png") for i in range(4)]
    }
    normal_sprites = [QPixmap(f"assets/normal_{i}.png") for i in range(4)]
    # golden_sprites = [QPixmap(f"sprites/golden_{i}.png") for i in range(4)]
    # spoiled_sprites = [QPixmap(f"sprites/spoiled_{i}.png") for i in range(4)]

    POO_TYPES["normal"].sprites = normal_sprites
    # POO_TYPES["golden"].sprites = golden_sprites
    # POO_TYPES["spoiled"].sprites = spoiled_sprites

    self.poo_type = POO_TYPES["normal"]  # you can change this later dynamically if needed

    self.direction = random.choice(["left", "right"])
    self.frame = 0
    self.is_walking = True
    self.is_dragging = False
    self.old_pos = None
    self.velocity_y = 0
    self.spawned_poo = []