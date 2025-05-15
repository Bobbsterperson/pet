from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
import random

def initialize_sprites(self):
    self.label = QLabel(self)
    self.sprites = {
        "walk": [QPixmap(f"assets/walk{i}.png") for i in range(4)],
        "idle": [QPixmap(f"assets/idle{i}.png") for i in range(4)],
        "shiv": [QPixmap(f"assets/shiv{i}.png") for i in range(4)],
        "poop": [QPixmap(f"assets/poop{i}.png") for i in range(4)],
        "eat": [QPixmap(f"assets/eat{i}.png") for i in range(4)]
    }
    self.direction = random.choice(["left", "right"])
    self.frame = 0
    self.is_walking = True
    self.is_dragging = False
    self.old_pos = None
    self.velocity_y = 0
    self.poo_pixmap = QPixmap("assets/poo.png")
    self.spawned_poo = []