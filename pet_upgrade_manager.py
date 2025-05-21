from dataclasses import replace
from poo import POO_TYPES

class PetUpgradeManager:
    def __init__(self, panel):
        self.panel = panel

    def lvl_up(self):
        if self.panel.xp_bar.value() < self.panel.pet.max_xp:
            self.panel.info_label.setText("XP not full! Cannot level up.")
            return
        old_max = self.panel.pet.max_xp
        new_max = int(old_max * 1.45)
        self.panel.set_max_xp(new_max)
        self.panel.xp_bar.setValue(0)
        self.panel.increase_xp(self.panel.pet.stored_overflow_xp)
        self.panel.pet.stored_overflow_xp = 0
        self.panel.info_label.setText(f"Level Up! Max XP increased to {self.panel.pet.max_xp}.")

    def reg_button(self):
        xp = self.panel.xp_bar.value()
        cost = self.panel.pet.auto_poo_refill_upgrade_cost
        if xp >= cost:
            self.panel.xp_bar.setValue(xp - cost)
            self.panel.pet.poo_units_refil_time_value += 1
            self.panel.pet.auto_poo_refill_upgrade_cost *= 50
            self.panel.info_label.setText(f"Upgrade success! Next cost: {self.panel.pet.auto_poo_refill_upgrade_cost} XP")
        else:
            self.panel.info_label.setText(f"Need {cost} XP! You have {xp}.")

    def reg_button_time(self):
        xp = self.panel.xp_bar.value()
        cost = self.panel.pet.bladder_regen_speed_cost
        if xp >= cost:
            self.panel.xp_bar.setValue(xp - cost)
            self.panel.pet.bladder_refil_timer -= 100
            self.panel.pet.bladder_regen_speed_cost *= 30
            self.panel.info_label.setText(f"Upgrade success! Next cost: {self.panel.pet.bladder_regen_speed_cost} XP")
        else:
            self.panel.info_label.setText(f"Need {cost} XP! You have {xp}.")

    def extend_bladder_capacity(self):
        xp = self.panel.xp_bar.value()
        cost = self.panel.pet.bladder_extend_cost
        if xp >= cost:
            self.panel.xp_bar.setValue(xp - cost)
            new_cap = int(self.panel.pet.bladder_bar_cap * 1.1)
            self.panel.set_max_bladder(new_cap)
            self.panel.pet.bladder_extend_cost *= 30
            self.panel.info_label.setText(f"Bladder extended to {new_cap}. Next upgrade: {self.panel.pet.bladder_extend_cost} XP")
        else:
            self.panel.info_label.setText(f"Need {cost} XP! You have {xp}.")

    def less_bladder_use(self):
        xp = self.panel.xp_bar.value()
        cost = self.panel.pet.less_bladder_use_cost
        if xp >= cost:
            self.panel.xp_bar.setValue(xp - cost)
            normal_poo = POO_TYPES["normal"]
            new_val = max(normal_poo.bladder_value_decrese - 1, 0)
            POO_TYPES["normal"] = replace(normal_poo, bladder_value_decrese=new_val)
            self.panel.pet.less_bladder_use_cost *= 50
            self.panel.info_label.setText(f"Upgrade success! Next cost: {self.panel.pet.less_bladder_use_cost} XP")
        else:
            self.panel.info_label.setText(f"Need {cost} XP! You have {xp}.")

    def poo_return_more_bladder(self):
        xp = self.panel.xp_bar.value()
        cost = self.panel.pet.poo_return_more_bladder_cost
        if xp >= cost:
            self.panel.xp_bar.setValue(xp - cost)
            normal_poo = POO_TYPES["normal"]
            new_return = normal_poo.bladder_value_return + 1
            POO_TYPES["normal"] = replace(normal_poo, bladder_value_return=new_return)
            self.panel.pet.poo_return_more_bladder_cost *= 50
            self.panel.info_label.setText(f"Upgrade success! Next cost: {self.panel.pet.poo_return_more_bladder_cost} XP")
        else:
            self.panel.info_label.setText(f"Need {cost} XP! You have {xp}.")

    def auto_poop(self):
        xp = self.panel.xp_bar.value()
        cost = self.panel.pet.auto_poop_cost
        if xp >= cost:
            self.panel.xp_bar.setValue(xp - cost)
            if not self.panel.pet.poop_auto_timer.isActive():
                self.panel.pet.poop_auto_timer.start(self.panel.pet.auto_poop_interval)
            else:
                self.panel.pet.auto_poop_interval = max(2500, self.panel.pet.auto_poop_interval - 100)
                self.panel.pet.poop_auto_timer.start(self.panel.pet.auto_poop_interval)
            self.panel.pet.auto_poop_cost *= 50
            self.panel.info_label.setText(f"Upgrade success! Next cost: {self.panel.pet.auto_poop_cost} XP")
        else:
            self.panel.info_label.setText(f"Need {cost} XP! You have {xp}.")
