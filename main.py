import sys, random
from PyQt5.QtCore import Qt, QTimer, QPoint, QUrl, QDateTime
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QDesktopWidget
from PyQt5.QtMultimedia import QSoundEffect
from control_panel import PetControlPanel
from poo import Poo


class Pet(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.initialize_settings()
        self.initialize_sprites()
        self.initialize_sounds()
        self.setup_timers()
        self.setup_position()

    def initialize_settings(self):
        self.animation_interval = 100
        self.sound_volume = 0.2
        self.walk_speed = 30
        self.pickup_counter = 0
        self.volume_set_max = False
        self.poo_scale_factor = 0.5
        self.bladder_refil_timer = 7500
        self.eat_animation_timer = None
        self.is_pooping = False  
        self.is_eating = False     
        self.target_poo = None 
        self.approach_speed = 10
        self.poo_type_value = 10
        self.poo_refil_time_value = 0
        self.can_be_picked_up = True

    def initialize_sprites(self):
        self.label = QLabel(self)
        self.sprites = {
            "walk": [QPixmap(f"assets/walk{i}.png") for i in range(4)],
            "idle": [QPixmap(f"assets/idle{i}.png") for i in range(4)],
            "drag": [QPixmap(f"assets/shiv{i}.png") for i in range(4)],
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

    def setup_window(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

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
        self.poop_sound = QSoundEffect()
        self.poop_sound.setSource(QUrl.fromLocalFile("assets/poop.wav"))
        self.poop_sound.setVolume(self.sound_volume)
        self.eat_sound = QSoundEffect()
        self.eat_sound.setSource(QUrl.fromLocalFile("assets/eat.wav"))
        self.eat_sound.setVolume(self.sound_volume)

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
        self.pickup_cooldown_timer = QTimer(self)
        self.pickup_cooldown_timer.setInterval(500)
        self.pickup_cooldown_timer.setSingleShot(True)
        self.pickup_cooldown_timer.timeout.connect(self.enable_pickup)
        self.meh_timer = QTimer(self)
        self.meh_timer.timeout.connect(self.play_meh_sound)
        self.set_random_meh_timer()
        self.poop_cleanup_timer = QTimer(self)
        self.poop_cleanup_timer.timeout.connect(self.cleanup_poop)
        self.poop_cleanup_timer.start(1000)

    def enable_pickup(self):
        self.can_be_picked_up = True

    def setup_position(self):
        self.screen = QDesktopWidget().availableGeometry()
        self.label.setPixmap(self.sprites["idle"][0])
        self.resize(self.label.pixmap().size())
        self.move(self.screen.width() // 2, self.screen.height() - self.height())

    def update_sprite(self):
        if self.is_pooping or self.is_eating:
            return
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
        if self.old_pos is not None or self.gravity_timer.isActive():
            return
        if self.target_poo and self.target_poo.is_valid():
            pet_center = self.x() + self.width() // 2
            poo_center = self.target_poo.label.x() + self.target_poo.label.width() // 2
            if abs(pet_center - poo_center) <= 5:
                self.handle_eat_animation(self.target_poo)
                self.target_poo = None
            else:
                self.direction = "right" if pet_center < poo_center else "left"
                dx = self.approach_speed if self.direction == "right" else -self.approach_speed
                new_x = self.x() + dx
                new_x = max(0, min(self.screen.width() - self.width(), new_x))
                self.move(new_x, self.y())
            return
        if not self.is_walking:
            return

        dx = self.walk_speed if self.direction == "right" else -self.walk_speed
        new_x = self.x() + dx
        if 0 <= new_x <= self.screen.width() - self.width():
            self.move(new_x, self.y())
        else:
            self.direction = "left" if self.direction == "right" else "right"

    def toggle_walking(self):
        if self.is_pooping or self.is_eating:
            return
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
        if event.button() == Qt.LeftButton and self.can_be_picked_up:
            self.can_be_picked_up = False
            self.pickup_cooldown_timer.start()
            self.start_dragging(event)
            self.play_pickup_sound()
            self.handle_pickup_counter()
            self.adjust_volume()

    def start_dragging(self, event):
        self.old_pos = event.globalPos() - self.pos()
        self.velocity_y = 0
        self.gravity_timer.stop()
        self.is_dragging = True
        if self.is_pooping:
            self.is_pooping = False
            if hasattr(self, 'poop_animation_timer'):
                self.poop_animation_timer.stop()
                self.poop_animation_timer.deleteLater()
                del self.poop_animation_timer
            self.animation_timer.start(self.animation_interval)

    def play_pickup_sound(self):
        now = QDateTime.currentMSecsSinceEpoch()
        if now - self.last_pickup_sound_time > self.pickup_sound_cooldown:
            available_sounds = [sound for i, sound in enumerate(self.pickup_sounds) if i != self.last_played_sound]
            sound_to_play = random.choice(available_sounds)
            if not sound_to_play.isPlaying():
                sound_to_play.play()
                self.last_played_sound = self.pickup_sounds.index(sound_to_play)
                self.last_pickup_sound_time = now

    def handle_pickup_counter(self):
        self.pickup_counter += 1

    def adjust_volume(self):
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
        x = max(0, min(self.x(), self.screen.width() - self.width()))
        y = min(self.y(), self.screen.height() - self.height())
        self.move(x, y)
        self.gravity_timer.start(30)

    def apply_gravity(self):
        self.velocity_y += 6
        new_y = self.y() + self.velocity_y
        if new_y >= self.screen.height() - self.height():
            new_y = self.screen.height() - self.height()
            self.velocity_y = 0
            self.gravity_timer.stop()
        new_x = min(max(self.x(), 0), self.screen.width() - self.width())
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
        if self.gravity_timer.isActive() or self.is_pooping:
            return
        self.is_pooping = True
        self.is_walking = False
        self.frame = 0
        self.current_action = "poop"
        self.animation_timer.stop()
        self.poop_animation_timer = QTimer(self)
        self.poop_animation_timer.timeout.connect(self.poop_animation)
        self.poop_animation_timer.start(self.animation_interval)

    def poop_animation(self):
        if self.frame >= 4:
            self.poop_animation_timer.stop()
            self.poop_animation_timer.deleteLater()
            del self.poop_animation_timer
            self.spawn_poo()
            self.is_pooping = False
            self.is_walking = True
            self.current_action = None
            self.animation_timer.start(self.animation_interval)
            self.frame = 0
            return
        pix = self.sprites["poop"][self.frame % 4]
        if self.direction == "left":
            pix = pix.transformed(QTransform().scale(-1, 1))
        self.label.setPixmap(pix)
        self.frame += 1

    def spawn_poo(self):
        if self.poo_pixmap.isNull():
            return
        self.poop_sound.play()
        x = max(0, min(self.x() + self.width() // 2 - int(self.poo_pixmap.width() * self.poo_scale_factor) // 2,
                    self.screen.width() - int(self.poo_pixmap.width() * self.poo_scale_factor)))
        y = self.screen.height() - int(self.poo_pixmap.height() * self.poo_scale_factor)
        poo = Poo(self, self.poo_pixmap, x, y, self.poo_scale_factor)
        self.spawned_poo.append(poo)

    def cleanup_poop(self):
        now = QDateTime.currentMSecsSinceEpoch()
        pet_center = self.x() + self.width() // 2

        for poo in self.spawned_poo:
            if poo.is_deleted:
                continue
            if now - poo.spawn_time >= 10000 and poo.is_valid():
                poo_center = poo.label.x() + poo.label.width() // 2
                distance = abs(pet_center - poo_center)
                if distance <= 200:
                    if self.target_poo is None:
                        self.target_poo = poo
                        self.is_walking = False
                        self.animation_timer.start(self.animation_interval)
                    break


    def handle_eat_animation(self, poo):
        poo.label.raise_()
        if self.eat_animation_timer or self.is_eating:
            return
        self.eat_sound.play()
        self.is_eating = True
        self.eat_animation_timer = QTimer(self)
        self.eat_animation_timer.timeout.connect(lambda: self.eat_animation(poo))
        self.is_walking = False
        self.frame = 0
        self.current_action = "eat"
        self.animation_timer.stop()
        self.eat_animation_timer.start(self.animation_interval)

    def eat_animation(self, poo):
        eat_frames = self.sprites["eat"]
        
        if self.frame >= len(eat_frames):
            self.eat_animation_timer.stop()
            self.eat_animation_timer = None
            self.label.setPixmap(self.sprites["idle"][0])
            self.frame = 0
            self.is_eating = False
            self.current_action = None
            self.is_walking = True
            self.animation_timer.start(self.animation_interval)
            if poo and poo in self.spawned_poo and poo.is_valid():
                poo.deleteLater()
                self.spawned_poo.remove(poo)
                self.control_panel.refill_poop_bar()
                self.control_panel.increase_xp(self.poo_type_value)
            return
        self.label.setPixmap(eat_frames[self.frame])
        self.frame += 1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = Pet()
    panel = PetControlPanel(pet) 
    pet.control_panel = panel
    pet.show()
    panel.show()
    sys.exit(app.exec_())
