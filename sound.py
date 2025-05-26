from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtCore import QUrl

def initialize_sounds(self):
    self.pickup_sounds = []
    for i in range(4):
        sound = QSoundEffect()
        sound.setSource(QUrl.fromLocalFile(f"assets/sound/pick{i}.wav"))
        sound.setVolume(self.sound_volume)
        self.pickup_sounds.append(sound)
    self.last_pickup_sound_time = 0
    self.pickup_sound_cooldown = 500
    self.last_played_sound = None
    self.play_lvl_up_sound = QSoundEffect()
    self.play_lvl_up_sound.setSource(QUrl.fromLocalFile("assets/sound/meh.wav"))
    self.play_lvl_up_sound.setVolume(self.sound_volume)
    self.poop_sound = QSoundEffect()
    self.poop_sound.setSource(QUrl.fromLocalFile("assets/sound/poop.wav"))
    self.poop_sound.setVolume(self.sound_volume)
    self.eat_sound = QSoundEffect()
    self.eat_sound.setSource(QUrl.fromLocalFile("assets/sound/eat.wav"))
    self.eat_sound.setVolume(self.sound_volume)