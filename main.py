import sys, random
from PyQt5.QtCore import Qt, QTimer, QPoint, QUrl, QDateTime
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QDesktopWidget
from PyQt5.QtMultimedia import QSoundEffect

class Pet(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # Settings
        self.animation_interval = 100  # milliseconds between frames
        self.sound_volume = 0.2       # range: 0.0 (mute) to 1.0 (max)
        self.walk_speed = 30  # pixels per step (initial speed)
        self.pickup_counter = 0
        self.volume_set_max = False

        self.label = QLabel(self)
        self.sprites = {
            "walk": [QPixmap(f"assets/walk{i}.png") for i in range(4)],
            "idle": [QPixmap(f"assets/idle{i}.png") for i in range(4)],
            "drag": [QPixmap(f"assets/shiv{i}.png") for i in range(4)],
        }

        self.direction = random.choice(["left", "right"])
        self.frame = 0
        self.is_walking = True
        self.is_dragging = False
        self.old_pos = None
        self.velocity_y = 0

        self.screen = QDesktopWidget().availableGeometry()
        self.label.setPixmap(self.sprites["idle"][0])
        self.resize(self.label.pixmap().size())
        self.move(self.screen.width() // 2, self.screen.height() - self.height())

        # Pickup sounds
        self.pickup_sounds = []
        for i in range(4):
            sound = QSoundEffect()
            sound.setSource(QUrl.fromLocalFile(f"assets/pick{i}.wav"))
            sound.setVolume(self.sound_volume)
            self.pickup_sounds.append(sound)

        # Cooldown for pickup sounds
        self.last_pickup_sound_time = 0
        self.pickup_sound_cooldown = 500  # ms

        # Keep track of last played sound index
        self.last_played_sound = None

        # "meh" sound
        self.meh_sound = QSoundEffect()
        self.meh_sound.setSource(QUrl.fromLocalFile("assets/meh.wav"))
        self.meh_sound.setVolume(self.sound_volume)

        # Animation timer
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_sprite)
        self.animation_timer.start(self.animation_interval)

        # Movement logic timer
        self.move_timer = QTimer(self)
        self.move_timer.timeout.connect(self.move_pet)
        self.move_timer.start(50)

        # Random movement speed timer
        self.speed_timer = QTimer(self)
        self.speed_timer.timeout.connect(self.set_random_movement_speed)
        self.speed_timer.start(random.randint(1000, 3000))

        # State change timer
        self.state_timer = QTimer(self)
        self.state_timer.timeout.connect(self.toggle_walking)
        self.set_random_state_timer()

        # Gravity
        self.gravity_timer = QTimer(self)
        self.gravity_timer.timeout.connect(self.apply_gravity)

        # Reset pickup counter
        self.pickup_reset_timer = QTimer(self)
        self.pickup_reset_timer.timeout.connect(self.reset_pickup_counter)
        self.pickup_reset_timer.start(2000)

        # Random "meh" sound
        self.meh_timer = QTimer(self)
        self.meh_timer.timeout.connect(self.play_meh_sound)
        self.set_random_meh_timer()

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
        print(f"New walk speed: {self.walk_speed}")
        self.speed_timer.start(random.randint(1000, 3000))

    def reset_pickup_counter(self):
        self.pickup_counter = 0

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos() - self.pos()
            self.velocity_y = 0
            self.gravity_timer.stop()
            self.is_dragging = True

            # Play a random pickup sound if not already playing and cooldown passed
            now = QDateTime.currentMSecsSinceEpoch()
            if now - self.last_pickup_sound_time > self.pickup_sound_cooldown:
                # Choose a random sound that is not the last played sound
                available_sounds = [sound for i, sound in enumerate(self.pickup_sounds) if i != self.last_played_sound]
                sound_to_play = random.choice(available_sounds)
                if not sound_to_play.isPlaying():
                    sound_to_play.play()
                    self.last_played_sound = self.pickup_sounds.index(sound_to_play)  # Store the index of the last played sound
                    self.last_pickup_sound_time = now

            self.pickup_counter += 1
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
        print("Volume set to maximum (1.0) due to multiple pickups.")

    def reset_volume(self):
        for sound in self.pickup_sounds:
            sound.setVolume(0.2)
        self.volume_set_max = False
        print("Volume reset to 0.2.")

    def play_meh_sound(self):
        self.meh_sound.setVolume(1.0)
        self.meh_sound.play()
        print("Playing 'meh' sound at max volume.")
        self.set_random_meh_timer()

    def set_random_meh_timer(self):
        random_interval = random.randint(3600, 10800)
        self.meh_timer.start(random_interval * 1000)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = Pet()
    pet.show()
    sys.exit(app.exec_())
