from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
import random
from poo import get_poo_types

def initialize_sprites(self):
    self.label = QLabel(self)
    POO_TYPES = get_poo_types()
    
    # Load pet action sprites
    self.sprites = {
        "walk": [QPixmap(f"pet/walk{i}.png") for i in range(4)],
        "idle": [QPixmap(f"pet/idle{i}.png") for i in range(4)],
        "shiv": [QPixmap(f"pet/shiv{i}.png") for i in range(4)],
        "poop": [QPixmap(f"pet/poop{i}.png") for i in range(4)],
        "eat": [QPixmap(f"pet/eat{i}.png") for i in range(4)]
    }

    # Assign poo sprites to each poo type dynamically
    for name, poo_type in POO_TYPES.items():
        poo_type.sprites = [QPixmap(f"poo/{name}_{i}.png") for i in range(4)]

    self.poo_type = POO_TYPES["normal"]  # Initial poo type

    # Other state variables
    self.direction = random.choice(["left", "right"])
    self.frame = 0
    self.is_walking = True
    self.is_dragging = False
    self.old_pos = None
    self.velocity_y = 0
    self.spawned_poo = []
