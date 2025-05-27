from dataclasses import replace
from poo import get_poo_types

class PetUpgradeManager:
    def __init__(self, panel):
        self.panel = panel
        self.POO_TYPES = get_poo_types()

    def lvl_up(self):
        self.panel.current_level += 1
        self.panel.pet.play_lvl_up_sound_f()

        # Update achievement buttons properly:
        # Clear old achievement buttons first, then add new ones
        self.panel.clear_achievement_buttons()  # You need to implement this method
        self.panel.add_achievements_buttons(self.panel.achievements_layout)  # Pass your actual layout

        # self.panel.add_skill_buttons()

        for key, poo in self.panel.pet.POO_TYPES.items():
            if self.panel.current_level >= poo.min_level:
                if key in ("toxic", "monster", "gold"):
                    poo.spawn_chance_grow_per_level = round(poo.spawn_chance_grow_per_level + 0.004, 6)
                else:
                    poo.spawn_chance_grow_per_level = round(poo.spawn_chance_grow_per_level + 0.002, 6)


        old_max = self.panel.pet.max_xp
        new_max = int(old_max * 1.45)
        self.panel.set_max_xp(new_max)
        self.panel.xp_bar.setMaximum(new_max)
        self.panel.xp_bar.setValue(0)
        self.panel.info_label.setText(
            f"🎉 Level Up! Now Level {self.panel.current_level}. New XP cap: {new_max}"
        )



    def reg_button(self):
        xp = self.panel.xp_bar.value()
        cost = self.panel.pet.auto_poo_refill_upgrade_cost
        if xp >= cost:
            self.panel.xp_bar.setValue(xp - cost)
            self.panel.pet.poo_units_refil_time_value += 1
            self.panel.pet.auto_poo_refill_upgrade_cost *= 50
            self.panel.info_label.setText(
                f"Upgrade success! Refill amount: {self.panel.pet.poo_units_refil_time_value}. "
                f"Next cost: {self.panel.pet.auto_poo_refill_upgrade_cost} XP"
            )
        else:
            self.panel.info_label.setText(f"Need {cost} XP! You have {xp}.")

    def reg_button_time(self):
        xp = self.panel.xp_bar.value()
        cost = self.panel.pet.bladder_regen_speed_cost
        if xp >= cost:
            self.panel.xp_bar.setValue(xp - cost)
            self.panel.pet.bladder_refil_timer -= 100
            self.panel.pet.bladder_regen_speed_cost *= 30
            self.panel.info_label.setText(
                f"Upgrade success! New bladder refill time: {self.panel.pet.bladder_refil_timer}ms "
                f"({self.panel.pet.bladder_refil_timer / 1000:.2f}s). "
                f"Next cost: {self.panel.pet.bladder_regen_speed_cost} XP"
            )
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
            for key, poo in self.panel.pet.POO_TYPES.items():
                if self.panel.current_level >= poo.min_level:
                    poo.bladder_value_decrease = max(poo.bladder_value_decrease - 1, 0)
                    # Also update spawned poos
                    for spawned in self.panel.pet.spawned_poo:
                        if spawned.poo_type.name == poo.name:
                            spawned.poo_type.bladder_value_decrease = poo.bladder_value_decrease
            self.panel.pet.less_bladder_use_cost += 50
            self.panel.pet.bladder_value_decrease_units += 1
            self.panel.info_label.setText(
                f"Upgrade success! All unlocked poo types now use less bladder. "
                f"Next cost: {self.panel.pet.less_bladder_use_cost} XP"
            )
        else:
            self.panel.info_label.setText(f"Need {cost} XP! You have {xp}.")

    def poo_return_more_bladder(self):
        xp = self.panel.xp_bar.value()
        cost = self.panel.pet.poo_return_more_bladder_cost
        if xp >= cost:
            self.panel.xp_bar.setValue(xp - cost)

            for key, poo in self.panel.pet.POO_TYPES.items():
                if self.panel.current_level >= poo.min_level:
                    poo.bladder_value_return += 1

                    for spawned in self.panel.pet.spawned_poo:
                        if spawned.poo_type.name == poo.name:
                            spawned.poo_type.bladder_value_return = poo.bladder_value_return

            self.panel.pet.poo_return_more_bladder_cost += 50
            self.panel.pet.bladder_value_increases_units += 1
            self.panel.info_label.setText(
                f"Upgrade success! All unlocked poo types now restore more bladder. "
                f"Next cost: {self.panel.pet.poo_return_more_bladder_cost} XP"
            )
        else:
            self.panel.info_label.setText(f"Need {cost} XP! You have {xp}.")

    def auto_poop(self):
        xp = self.panel.xp_bar.value()
        cost = self.panel.pet.self_poop_skill_cost  # Assuming this is set somewhere in your class

        if self.panel.pet.poop_auto_timer.isActive():
            self.panel.info_label.setText("Auto-poop is already active.")
            return

        if xp < cost:
            self.panel.info_label.setText(f"Need {cost} XP to activate auto-poop. You have {xp}.")
            return

        # Deduct XP and start the timer
        self.panel.xp_bar.setValue(xp - cost)
        self.panel.pet.poop_auto_timer.start(self.panel.pet.auto_poop_interval)
        self.panel.pet.auto_poop_skill_enabled = True
        self.panel.info_label.setText(
            f"Auto-poop activated! Interval: {self.panel.pet.auto_poop_interval / 1000:.1f}s. "
            f"({cost} XP spent)"
        )


    def upgrade_auto_poop_timer(self):
        xp = self.panel.xp_bar.value()
        cost = self.panel.pet.auto_poop_cost

        if not self.panel.pet.poop_auto_timer.isActive():
            self.panel.info_label.setText("Activate auto-poop first.")
            return

        if xp >= cost:
            self.panel.xp_bar.setValue(xp - cost)
            self.panel.pet.auto_poop_interval = max(2500, self.panel.pet.auto_poop_interval - 100)
            self.panel.pet.poop_auto_timer.start(self.panel.pet.auto_poop_interval)

            self.panel.pet.auto_poop_cost *= 50
            self.panel.info_label.setText(
                f"Upgrade success! Interval is now {self.panel.pet.auto_poop_interval / 1000:.1f}s. "
                f"Next cost: {self.panel.pet.auto_poop_cost} XP"
            )
            self.panel.refresh_upgrade_texts()
        else:
            self.panel.info_label.setText(f"Need {cost} XP! You have {xp}.")





