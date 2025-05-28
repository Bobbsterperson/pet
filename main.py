import sys, random
from PyQt5.QtCore import Qt, QTimer, QDateTime, pyqtSignal
from PyQt5.QtGui import QTransform
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from control_panel import PetControlPanel
from poo import get_poo_types, Poo
from PyQt5.QtGui import QPixmap
from timers import setup_timers
from sound import initialize_sounds
from settings import initialize_settings
from sprites import initialize_sprites

class Pet(QWidget):
    sprite_changed = pyqtSignal(QPixmap)
    def __init__(self):
        super().__init__()
        self.setup_window()
        initialize_settings(self)
        self.sprite_variant = 00
        self.POO_TYPES = get_poo_types()
        initialize_sprites(self)
        initialize_sounds(self)
        setup_timers(self)
        self.setup_position() 
        self.spawned_poo = []   

    def setup_window(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

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
        
        if self.is_hidden:
            # Cycle cage animation frames
            pix = self.get_current_pixmap()
            self.label.setPixmap(pix)
            self.current_pixmap = pix
            self.sprite_changed.emit(pix)
            self.frame += 1
            return

        # Existing logic for normal sprites
        if self.is_dragging:
            pix = self.sprites["shiv"][self.frame % 4]
        elif self.is_walking:
            pix = self.sprites["walk"][self.frame % 4]
        else:
            pix = self.sprites["idle"][self.frame % 4]

        if self.direction == "left" and not self.is_dragging:
            pix = pix.transformed(QTransform().scale(-1, 1))

        self.label.setPixmap(pix)
        self.current_pixmap = pix
        self.sprite_changed.emit(pix)
        self.frame += 1


    def get_current_pixmap(self):
        if self.is_hidden:
            frame_index = self.frame % len(self.cage_sprites)
            return self.cage_sprites[frame_index]
        else:
            pixmap = getattr(self, "current_pixmap", QPixmap("assets/pet/idle00.png"))
            if pixmap.isNull():
                print("Warning: get_current_pixmap() returned a null QPixmap.")
            return pixmap

    def move_pet(self):
        if self.old_pos is not None or self.gravity_timer.isActive() or self.is_hidden:
            return
        if self.target_poo:
            if self.target_poo.is_deleted or not self.target_poo.label:
                self.target_poo = None
            else:
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
            self.start_shivering(event)
            self.play_pickup_sound()
            self.handle_pickup_counter()
            self.adjust_volume()

    def start_shivering(self, event):
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
        self.control_panel.refill_poop_bar(1)
        self.pickup_counter += 1

    def adjust_volume(self):
        if 4 <= self.pickup_counter <= 8 and not self.volume_set_max:
            if self.sound_volume == 0.0:
                return
            else:
                self.set_volume_max()
        elif self.volume_set_max:
            if self.sound_volume == 0.0:
                return
            else:
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
        if self.is_hidden:
            return
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

    def play_lvl_up_sound_f(self):
        self.play_lvl_up_sound.setVolume(self.sound_volume)
        self.play_lvl_up_sound.play()

    def poop(self, poo_type):
        if self.gravity_timer.isActive() or self.is_pooping or self.is_eating: #or self.is_hidden
            return
        self.is_pooping = True
        self.is_walking = False
        self.frame = 0
        self.current_action = "poop"
        self.current_poo_type = poo_type  # Save for use in animation
        self.animation_timer.stop()
        self.poop_animation_timer = QTimer(self)
        self.poop_animation_timer.timeout.connect(self.poop_animation)
        self.poop_animation_timer.start(self.animation_interval)

    def achievement_get(self):
        if self.gravity_timer.isActive() or self.is_pooping or self.is_eating:
            return
        self.achievement_sound.setVolume(self.sound_volume)
        self.achievement_sound.play()
        self.is_pooping = False
        self.is_walking = False
        self.frame = 0
        self.current_action = "achievement_animation"
        self.animation_timer.stop()
        if hasattr(self, 'achievement_animation_timer'):
            self.achievement_animation_timer.stop()
            self.achievement_animation_timer.deleteLater()
            del self.achievement_animation_timer
        self.achievement_animation_timer = QTimer(self)
        self.achievement_animation_timer.timeout.connect(self.animation_achievement)
        self.achievement_animation_timer.start(self.animation_interval)

    def animation_achievement(self):
        achievement_frames = self.sprites["achievement"]

        if self.frame >= len(achievement_frames):
            if hasattr(self, 'achievement_animation_timer'):
                self.achievement_animation_timer.stop()
                self.achievement_animation_timer.deleteLater()
                del self.achievement_animation_timer

            self.is_pooping = False
            self.is_walking = True
            self.current_action = None
            self.animation_timer.start(self.animation_interval)
            self.frame = 0
            return

        pix = achievement_frames[self.frame]
        if self.direction == "left":
            pix = pix.transformed(QTransform().scale(-1, 1))
        self.label.setPixmap(pix)
        self.frame += 1



    def auto_poop_action(self):
        poo_type = self.control_panel.get_random_poo_type()
        self.control_panel.try_to_poop(poo_type)

    def poop_animation(self):
        if self.frame >= 4:
            self.poop_animation_timer.stop()
            self.poop_animation_timer.deleteLater()
            del self.poop_animation_timer

            self.spawn_poo(self.current_poo_type)  # Spawn actual poo

            self.is_pooping = False
            self.is_walking = True
            self.current_action = None
            self.animation_timer.start(self.animation_interval)
            self.frame = 0
            return

        # Display pet's poop animation frame
        pix = self.sprites["poop"][self.frame % 4]
        if self.direction == "left":
            pix = pix.transformed(QTransform().scale(-1, 1))
        self.label.setPixmap(pix)
        self.frame += 1

    def spawn_poo(self, poo_type):
        self.poop_sound.play()       
        scale_factor = poo_type.size
        sprite = poo_type.sprites[0]

        # Calculate position to center poop under pet
        x = max(0, min(
            self.x() + self.width() // 2 - int(sprite.width() * scale_factor) // 2,
            self.screen.width() - int(sprite.width() * scale_factor)
        ))
        y = self.screen.height() - int(sprite.height() * scale_factor)

        poo = Poo(self, poo_type, x, y)
        self.spawned_poo.append(poo)


    def cleanup_poop(self):
        if self.is_hidden:
            return
        now = QDateTime.currentMSecsSinceEpoch()
        pet_center = self.get_pet_center()       
        for poo in self.spawned_poo:
            if self.should_ignore_poo(poo, now):
                continue           
            if self.is_poo_within_reach(poo, pet_center):
                if self.can_consume_poo(poo):
                    self.initiate_poo_consumption(poo)
                    break

    def get_pet_center(self):
        return self.x() + self.width() // 2

    def should_ignore_poo(self, poo, current_time):
        return poo.is_deleted or current_time - poo.spawn_time < self.time_before_poo_is_edible or not poo.is_valid()

    def is_poo_within_reach(self, poo, pet_center):
        poo_center = poo.label.x() + poo.label.width() // 2
        return abs(pet_center - poo_center) <= 200

    def can_consume_poo(self, poo):
        current_pooping = self.control_panel.poop_bar.value()
        refill_amount = poo.poo_type.bladder_value_return
        return current_pooping + refill_amount <= 100

    def initiate_poo_consumption(self, poo):
        if self.target_poo is None or self.target_poo.is_deleted or not self.target_poo.label:
            self.target_poo = poo
            self.is_walking = False
            self.animation_timer.start(self.animation_interval)

    def handle_eat_animation(self, poo):
        if self.is_hidden:
            return
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
        if self.gravity_timer.isActive() or self.is_pooping:
            return
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
            if poo and poo in self.spawned_poo:
                bladder_value, xp = poo.consume()
                self.spawned_poo.remove(poo)
                self.control_panel.refill_poop_bar(bladder_value)
                self.control_panel.increase_xp(xp)
            # Clear the target poo after it's been consumed
            if poo == self.target_poo:
                self.target_poo = None
            return
        self.label.setPixmap(eat_frames[self.frame])
        self.frame += 1

    def change_pet_variant_on_level(self):
        if self.control_panel.current_level >= 5:
            self.set_sprite_variant("1")
        else:
            self.set_sprite_variant("0")

    def set_sprite_variant(self, variant):
        self.sprite_variant = variant
        initialize_sprites(self)
        self.label.setPixmap(self.sprites["idle"][0])
        self.label.resize(self.label.pixmap().size())  # resize again here
        self.resize(self.label.size())
        self.label.update()



    def hide_pet_and_poop(self):
        self.is_hidden = True  # Set the flag first
        self.sprite_changed.emit(self.get_current_pixmap())
        cage_pixmap = self.get_current_pixmap()  # Now this uses is_hidden=True
        if cage_pixmap and not cage_pixmap.isNull():
            self.label.setPixmap(cage_pixmap)
        self.hide()
        for poo in self.spawned_poo:
            if poo.label:
                poo.label.hide()

    def show_pet_and_poop(self):
        self.is_hidden = False  # Set the flag first
        normal_pixmap = self.get_current_pixmap()  # Now this uses is_hidden=False
        if normal_pixmap and not normal_pixmap.isNull():
            self.label.setPixmap(normal_pixmap)
        self.show()
        for poo in self.spawned_poo:
            if poo.label:
                poo.label.show()

    def toggle_visibility(self):
        self.is_hidden = not self.is_hidden
        if self.is_hidden:
            self.hide_pet_and_poop()
        else:
            self.show_pet_and_poop()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = Pet()
    panel = PetControlPanel(pet) 
    pet.control_panel = panel
    pet.show()
    panel.show()
    sys.exit(app.exec_())
