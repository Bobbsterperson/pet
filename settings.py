def initialize_settings(self):
    self.animation_interval = 100
    self.sound_volume = 0.2
    self.walk_speed = 30
    self.pickup_counter = 0
    self.volume_set_max = False
    self.eat_animation_timer = None
    self.is_pooping = False  
    self.is_eating = False     
    self.target_poo = None 
    self.can_be_picked_up = True

    self.approach_speed = 10
    self.time_before_poo_is_edible = 2000

    self.bladder_refil_timer = 10000
    self.poo_units_refil_time_value = 0

    self.auto_poop_interval = 3500

    self.max_xp = 100
    self.auto_poo_refill_upgrade_cost = 50
    self.bladder_regen_speed_cost = 20
    self.bladder_extend_cost = 30
    self.less_bladder_use_cost = 50
    self.poo_return_more_bladder_cost = 50
    self.auto_poop_cost = 70

    self.stored_overflow_xp = 0
    self.bladder_bar_cap = 100

    self.text_bar_size = 80

    self.always_on_top = False