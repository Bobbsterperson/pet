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
    self.time_before_poo_is_edible = 2000