from dataclasses import replace
from poo import POO_TYPES
from PyQt5.QtCore import QTimer

def lvl_up(panel):
    if panel.xp_bar.value() < panel.pet.max_xp:
        panel.info_label.setText("XP not full! Cannot level up.")
        return
    old_max = panel.pet.max_xp
    new_max = int(old_max * 1.45)
    panel.set_max_xp(new_max)
    panel.xp_bar.setValue(0)
    panel.increase_xp(panel.pet.stored_overflow_xp)
    panel.pet.stored_overflow_xp = 0
    panel.info_label.setText(f"Level Up! Max XP increased to {panel.pet.max_xp}.")

def reg_button(self):
    current_xp = self.xp_bar.value()
    if current_xp >= self.pet.auto_poo_refill_upgrade_cost:
        self.xp_bar.setValue(current_xp - self.pet.auto_poo_refill_upgrade_cost)
        self.pet.poo_units_refil_time_value += 1
        self.pet.auto_poo_refill_upgrade_cost *= 50
        self.info_label.setText(f"Upgrade success! Next cost: {self.pet.auto_poo_refill_upgrade_cost} XP")
    else:
        self.info_label.setText(f"Need {self.pet.auto_poo_refill_upgrade_cost} XP! You have {current_xp}.")

def reg_button_time(self):
    current_xp = self.xp_bar.value()
    if current_xp >= self.pet.bladder_regen_speed_cost:
        self.xp_bar.setValue(current_xp - self.pet.bladder_regen_speed_cost)
        self.pet.bladder_refil_timer -= 100
        self.pet.bladder_regen_speed_cost *= 30
        self.info_label.setText(f"Upgrade success! Next cost: {self.pet.bladder_regen_speed_cost} XP")
    else:
        self.info_label.setText(f"Need {self.pet.bladder_regen_speed_cost} XP! You have {current_xp}.")

def extend_bladder_capacity(self):
    current_xp = self.xp_bar.value()
    if current_xp >= self.pet.bladder_extend_cost:
        self.xp_bar.setValue(current_xp - self.pet.bladder_extend_cost)   
        old_cap = self.pet.bladder_bar_cap
        new_cap = int(old_cap * 1.1)
        self.set_max_bladder(new_cap)
        self.pet.bladder_extend_cost *= 30
        self.info_label.setText(f"Bladder extended to {new_cap}. Next upgrade: {self.pet.bladder_extend_cost} XP")
    else:
        self.info_label.setText(f"Need {self.pet.bladder_extend_cost} XP! You have {current_xp}.")

def less_bladder_use(self):
    current_xp = self.xp_bar.value()
    if current_xp >= self.pet.less_bladder_use_cost:
        self.xp_bar.setValue(current_xp - self.pet.less_bladder_use_cost)
        normal_poo = POO_TYPES["normal"]
        new_decrese_value = max(normal_poo.bladder_value_decrese - 1, 0)
        POO_TYPES["normal"] = replace(normal_poo, bladder_value_decrese=new_decrese_value)
        self.pet.less_bladder_use_cost *= 50
        self.info_label.setText(f"Upgrade success! Next cost: {self.pet.less_bladder_use_cost} XP")
    else:
        self.info_label.setText(f"Need {self.pet.less_bladder_use_cost} XP! You have {current_xp}.")

def poo_return_more_bladder(self):
    current_xp = self.xp_bar.value()
    if current_xp >= self.pet.poo_return_more_bladder_cost:
        self.xp_bar.setValue(current_xp - self.pet.poo_return_more_bladder_cost)
        normal_poo = POO_TYPES["normal"]
        new_return_value = normal_poo.bladder_value_return + 1
        POO_TYPES["normal"] = replace(normal_poo, bladder_value_return=new_return_value)
        self.pet.poo_return_more_bladder_cost *= 50
        self.info_label.setText(f"Upgrade success! Next cost: {self.pet.poo_return_more_bladder_cost} XP")
    else:
        self.info_label.setText(f"Need {self.pet.poo_return_more_bladder_cost} XP! You have {current_xp}.")

def auto_poop(self):
    current_xp = self.xp_bar.value()
    if current_xp >= self.pet.auto_poop_cost:
        self.xp_bar.setValue(current_xp - self.pet.auto_poop_cost)
        if not self.pet.poop_auto_timer.isActive():
            self.pet.poop_auto_timer.start(self.pet.auto_poop_interval)
        else:
            self.auto_poop_interval = max(2500, self.pet.auto_poop_interval - 100)
            self.pet.poop_auto_timer.start(self.pet.auto_poop_interval)
        self.pet.auto_poop_cost *= 50
        self.info_label.setText(f"Upgrade success! Next cost: {self.pet.auto_poop_cost} XP")
    else:
        self.info_label.setText(f"Need {self.pet.auto_poop_cost} XP! You have {current_xp}.")

def try_to_poop(self):
    if self.pet.gravity_timer.isActive() or self.pet.is_dragging:
        self.poop_button.setText("Can't poop in air")
        self.poop_button.setEnabled(False)
        QTimer.singleShot(1500, self.reset_button_text)
        return
    if self.poop_button.isEnabled():
        if self.poop_bar.value() >= POO_TYPES["normal"].bladder_value_decrese:
            self.poop_bar.setValue(self.poop_bar.value() - POO_TYPES["normal"].bladder_value_decrese)
            self.pet.poop()
            self.lock_button(1000)
        else:
            self.poop_button.setText("Too tired to poop")
            self.poop_button.setEnabled(False)
            QTimer.singleShot(1500, self.reset_button_text)