from PyQt5.QtCore import QTimer
import random

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
    self.pickup_reset_timer.start(3000)

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
