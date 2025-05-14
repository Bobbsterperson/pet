import sys, random
from PyQt5.QtCore import Qt, QTimer, QPoint, QUrl, QDateTime
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QDesktopWidget
from PyQt5.QtMultimedia import QSoundEffect
from control_panel import PetControlPanel

class Pet(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.initialize_settings()
        self.initialize_sprites()
        self.initialize_sounds()
        self.setup_timers()
        self.setup_position()
        self.eat_animation_timer = None

    def setup_window(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

    def initialize_settings(self):
        self.animation_interval = 100  # milliseconds between frames
        self.sound_volume = 0.2       # range: 0.0 (mute) to 1.0 (max)
        self.walk_speed = 30  # pixels per step (initial speed)
        self.pickup_counter = 0
        self.volume_set_max = False
        self.poo_scale_factor = 0.5

    def initialize_sprites(self):
        self.label = QLabel(self)
        self.sprites = {
            "walk": [QPixmap(f"assets/walk{i}.png") for i in range(4)],
            "idle": [QPixmap(f"assets/idle{i}.png") for i in range(4)],
            "drag": [QPixmap(f"assets/shiv{i}.png") for i in range(4)],
            "poop": [QPixmap(f"assets/poop{i}.png") for i in range(4)],
            "eat": [QPixmap(f"assets/eat{i}.png") for i in range(4)]  # New eat animation sprites
        }
        self.direction = random.choice(["left", "right"])
        self.frame = 0
        self.is_walking = True
        self.is_dragging = False
        self.old_pos = None
        self.velocity_y = 0
        self.poo_pixmap = QPixmap("assets/poo.png")
        self.spawned_poo = []

    def initialize_sounds(self):
        self.pickup_sounds = []
        for i in range(4):
            sound = QSoundEffect()
            sound.setSource(QUrl.fromLocalFile(f"assets/pick{i}.wav"))
            sound.setVolume(self.sound_volume)
            self.pickup_sounds.append(sound)

        self.last_pickup_sound_time = 0
        self.pickup_sound_cooldown = 500
        self.last_played_sound = None

        self.meh_sound = QSoundEffect()
        self.meh_sound.setSource(QUrl.fromLocalFile("assets/meh.wav"))
        self.meh_sound.setVolume(self.sound_volume)

    def setup_timers(self):
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_sprite)
        self.animation_timer.start(self.animation_interval)
        self.move_timer = QTimer(self)
        self.move_timer.timeout.connect(self.move_pet)
        self.move_timer.start(50)
        self.speed_timer = QTimer(self)
        self.speed_timer.timeout.connect(self.set_random_movement_speed)
        self.speed_timer.start(random.randint(1000, 3000))
        self.state_timer = QTimer(self)
        self.state_timer.timeout.connect(self.toggle_walking)
        self.set_random_state_timer()
        self.gravity_timer = QTimer(self)
        self.gravity_timer.timeout.connect(self.apply_gravity)
        self.pickup_reset_timer = QTimer(self)
        self.pickup_reset_timer.timeout.connect(self.reset_pickup_counter)
        self.pickup_reset_timer.start(2000)
        self.meh_timer = QTimer(self)
        self.meh_timer.timeout.connect(self.play_meh_sound)
        self.set_random_meh_timer()

        self.poop_cleanup_timer = QTimer(self)  # Timer to check for poops to delete
        self.poop_cleanup_timer.timeout.connect(self.cleanup_poop)
        self.poop_cleanup_timer.start(1000)  # Check every second

    def setup_position(self):
        self.screen = QDesktopWidget().availableGeometry()
        self.label.setPixmap(self.sprites["idle"][0])
        self.resize(self.label.pixmap().size())
        self.move(self.screen.width() // 2, self.screen.height() - self.height())

    def update_sprite(self):
        if self.is_dragging:
            pix = self.sprites["drag"][self.frame % 4]
        elif self.is_walking:
            pix = self.sprites["walk"][self.frame % 4]
        else:
            pix = self.sprites["idle"][self.frame % 4]
        if self.direction == "left" and not self.is_dragging:
            pix = pix.transformed(QTransform().scale(-1, 1))
        self.label.setPixmap(pix)
        self.frame += 1

    def move_pet(self):
        if not self.is_walking or self.old_pos is not None:
            return
        dx = self.walk_speed if self.direction == "right" else -self.walk_speed
        new_x = self.x() + dx
        if 0 <= new_x <= self.screen.width() - self.width():
            self.move(new_x, self.y())
        else:
            self.direction = "left" if self.direction == "right" else "right"

    def toggle_walking(self):
        self.is_walking = not self.is_walking
        if self.is_walking:
            self.direction = random.choice(["left", "right"])
        self.set_random_state_timer()

    def set_random_state_timer(self):
        interval = random.randint(1000, 6000)
        self.state_timer.start(interval)

    def set_random_movement_speed(self):
        self.walk_speed = random.randint(10, 60)
        self.speed_timer.start(random.randint(1000, 3000))

    def reset_pickup_counter(self):
        self.pickup_counter = 0

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_dragging(event)
            self.play_pickup_sound()
            self.handle_pickup_counter()
            self.adjust_volume()

    def start_dragging(self, event):
        """Handles the dragging initialization."""
        self.old_pos = event.globalPos() - self.pos()
        self.velocity_y = 0
        self.gravity_timer.stop()
        self.is_dragging = True

    def play_pickup_sound(self):
        """Plays a random pickup sound if cooldown is met."""
        now = QDateTime.currentMSecsSinceEpoch()
        if now - self.last_pickup_sound_time > self.pickup_sound_cooldown:
            available_sounds = [sound for i, sound in enumerate(self.pickup_sounds) if i != self.last_played_sound]
            sound_to_play = random.choice(available_sounds)
            if not sound_to_play.isPlaying():
                sound_to_play.play()
                self.last_played_sound = self.pickup_sounds.index(sound_to_play)
                self.last_pickup_sound_time = now

    def handle_pickup_counter(self):
        """Increments the pickup counter and handles state changes."""
        self.pickup_counter += 1

    def adjust_volume(self):
        """Adjusts the volume based on the pickup counter."""
        if 4 <= self.pickup_counter <= 8 and not self.volume_set_max:
            self.set_volume_max()
        elif self.volume_set_max:
            self.reset_volume()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            self.move(event.globalPos() - self.old_pos)

    def mouseReleaseEvent(self, event):
        self.old_pos = None
        self.is_dragging = False
        x = self.x()
        y = self.y()
        if x < 0:
            x = 0
        elif x > self.screen.width() - self.width():
            x = self.screen.width() - self.width()
        if y > self.screen.height() - self.height():
            y = self.screen.height() - self.height()
        self.move(x, y)
        self.gravity_timer.start(30)

    def apply_gravity(self):
        self.velocity_y += 6
        new_y = self.y() + self.velocity_y
        if new_y >= self.screen.height() - self.height():
            new_y = self.screen.height() - self.height()
            self.velocity_y = 0
            self.gravity_timer.stop()
        new_x = self.x()
        if new_x < 0:
            new_x = 0
        elif new_x > self.screen.width() - self.width():
            new_x = self.screen.width() - self.width()

        self.move(new_x, new_y)

    def set_volume_max(self):
        for sound in self.pickup_sounds:
            sound.setVolume(1.0)
        self.volume_set_max = True

    def reset_volume(self):
        for sound in self.pickup_sounds:
            sound.setVolume(0.2)
        self.volume_set_max = False

    def play_meh_sound(self):
        self.meh_sound.setVolume(1.0)
        self.meh_sound.play()
        self.set_random_meh_timer()

    def set_random_meh_timer(self):
        random_interval = random.randint(3600, 10800)
        self.meh_timer.start(random_interval * 1000)

    def poop(self):
        if self.gravity_timer.isActive() or hasattr(self, 'poop_animation_timer') and self.poop_animation_timer.isActive():
            return  # Don't start poop if falling or already pooping
        self.is_walking = False
        self.frame = 0
        self.current_action = "poop"
        self.animation_timer.stop()  # stop normal sprite updates
        self.poop_animation_timer = QTimer(self)
        self.poop_animation_timer.timeout.connect(self.poop_animation)
        self.poop_animation_timer.start(self.animation_interval)

    def poop_animation(self):
        if self.frame >= 4:
            self.poop_animation_timer.stop()
            self.poop_animation_timer.deleteLater()
            del self.poop_animation_timer  # avoid keeping the reference
            self.spawn_poo()
            self.is_walking = True
            self.current_action = None
            self.animation_timer.start(self.animation_interval)  # resume normal animation
            self.frame = 0  # Reset frame counter
            return
        pix = self.sprites["poop"][self.frame % 4]
        if self.direction == "left":
            pix = pix.transformed(QTransform().scale(-1, 1))
        self.label.setPixmap(pix)
        self.frame += 1

    def spawn_poo(self):
        if self.poo_pixmap.isNull():
            return

        poo_label = QLabel(None)
        scaled_poo = self.poo_pixmap.scaled(
            int(self.poo_pixmap.width() * self.poo_scale_factor),
            int(self.poo_pixmap.height() * self.poo_scale_factor),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        poo_label.setPixmap(scaled_poo)
        poo_label.resize(scaled_poo.size())

        x = max(0, min(self.x() + self.width() // 2 - scaled_poo.width() // 2,
                    self.screen.width() - scaled_poo.width()))
        y = self.screen.height() - scaled_poo.height()

        poo_label.move(x, y)
        poo_label.setAttribute(Qt.WA_TranslucentBackground, True)
        poo_label.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        poo_label.show()

        spawn_time = QDateTime.currentMSecsSinceEpoch()  # Store spawn time
        self.spawned_poo.append({"poo_label": poo_label, "spawn_time": spawn_time, "is_deleted": False})  # Added is_deleted flag
        QTimer.singleShot(100000, poo_label.deleteLater)

    def cleanup_poop(self):
        """Check for poops that have existed for 10 seconds and are still on screen."""
        for poo in self.spawned_poo:
            poo_label = poo["poo_label"]

            # Check if the poo label is already marked as deleted
            if poo.get("is_deleted", False):
                continue  # Skip this poop if it has already been marked as deleted

            # If 10 seconds have passed, check if pet is on top of the poo and trigger the eat animation
            if QDateTime.currentMSecsSinceEpoch() - poo["spawn_time"] >= 10000:
                if self.is_on_top_of_poop(poo_label):
                    self.handle_eat_animation(poo_label)

    def is_on_top_of_poop(self, poo_label):
        """Check if the pet's current position overlaps with the poo label's position."""
        pet_rect = self.geometry()
        poo_rect = poo_label.geometry()

        return pet_rect.intersects(poo_rect)

    def handle_eat_animation(self, poo_label):
        """Handle the pet eating the poo animation."""
        # Only initialize the eat_animation_timer if it hasn't been done already
        if not self.eat_animation_timer:
            self.eat_animation_timer = QTimer(self)
            self.eat_animation_timer.timeout.connect(lambda: self.eat_animation(poo_label))

        self.is_walking = False
        self.frame = 0
        self.current_action = "eat"
        self.animation_timer.stop()  # Stop normal sprite updates
        self.eat_animation_timer.start(self.animation_interval)

    def eat_animation(self, poo_label):
        """Animate the pet eating the poo."""
        if self.frame >= 4:
            self.eat_animation_timer.stop()
            self.eat_animation_timer.deleteLater()
            del self.eat_animation_timer  # Avoid keeping the reference
            self.eat_animation_timer = None  # Reset it to None after use

            # Safely delete the poo label only if it hasn't been marked as deleted
            if not poo_label.isHidden() and poo_label.isWindow():
                poo_label.deleteLater()  # Delete the poop after eating

            # Mark the poo as deleted in our spawned_poo list
            for poo in self.spawned_poo:
                if poo["poo_label"] == poo_label:
                    poo["is_deleted"] = True  # Mark as deleted

            self.is_walking = True
            self.current_action = None
            self.animation_timer.start(self.animation_interval)  # Resume normal animation
            self.frame = 0  # Reset frame counter
            return
        pix = self.sprites["eat"][self.frame % 4]
        if self.direction == "left":
            pix = pix.transformed(QTransform().scale(-1, 1))
        self.label.setPixmap(pix)
        self.frame += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = Pet()
    panel = PetControlPanel(pet) 
    pet.show()
    panel.show()
    sys.exit(app.exec_())
