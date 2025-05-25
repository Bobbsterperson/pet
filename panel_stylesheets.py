panel =("""
        QWidget {
            background-color: transparent;
            color: white;
            font-family: 'Comic Sans MS', 'Arial', sans-serif;
        }
        QLabel {
            background-color: transparent;
            color: white;
        }
        QPushButton {
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            border: 1px solid white;
            border-radius: 5px;
            padding: 4px;
        }
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 0.2);
        }
        QProgressBar {
            background-color: rgba(255, 255, 255, 0.1);
            border: 1px solid white;
            border-radius: 5px;
            text-align: center;
            color: white;
        }
        QProgressBar::chunk {
            background-color: rgba(0, 255, 255, 0.5);
        }
    """)
info_bar = ("""
            QLabel {
                font-size: 24px;  /* Slightly smaller if you expect lots of lines */
                color: #ffffff;
                background-color: rgba(0, 0, 0, 0.5);
                border: 2px dashed #ff66cc;
                border-radius: 8px;
                padding: 6px;
            }
        """)
bladder_bar = ("""
            QProgressBar {
                border: 2px solid #ffffff;
                border-radius: 10px;
                text-align: center;
                font-weight: bold;
                font-size: 18px;
                color: #ff00ff;
                height: 45px;
                background-color: rgba(0, 0, 0, 0.3);
            }
            QProgressBar::chunk {
                background-color: #39ff14;
                border-radius: 10px;
            }
        """)
xp_bar = ("""
            QProgressBar {
                border: 2px solid #ffffff;
                border-radius: 10px;
                text-align: center;
                font-weight: bold;
                font-size: 18px;
                height: 45px;
                background-color: rgba(0, 0, 0, 0.3);
            }
            QProgressBar::chunk {
                background-color: #00bfff;
                border-radius: 10px;
            }
        """)
poop_btn = ("""
            QPushButton {
                background-color: #ff1493;
                color: white;
                font-size: 20px;
                font-weight: bold;
                border: 3px double white;
                border-radius: 15px;
                padding: 10px;

            }
            QPushButton:hover {
                background-color: #ff69b4;
            }
            QPushButton:pressed {
                background-color: #c71585;
            }
        """)
def get_upgrade_btn(self):
    return [
            {
                "icon_0": "assets/reg_butt0.png",
                "icon_1": "assets/reg_butt1.png",
                "text_func": lambda: f"Bladder auto refills. Refill amount per interval: {self.pet.poo_units_refil_time_value}. \nCurrent cost: {self.pet.auto_poo_refill_upgrade_cost}",
                "callback": self.upgrades.reg_button,
            },
            {
                "icon_0": "assets/reg_time_butt0.png",
                "icon_1": "assets/reg_time_butt1.png",
                "text_func": lambda: f"Bladder regen speed. New bladder refill time intreval: {self.pet.bladder_refil_timer / 1000:.1f}s. \nCurrent cost: {self.pet.bladder_regen_speed_cost}",
                "callback": self.upgrades.reg_button_time,
            },
            {
                "icon_0": "assets/bladextend_butt0.png",
                "icon_1": "assets/bladextend_butt1.png",
                "text_func": lambda: f"More bladder storage \nCurrent cost: {self.pet.bladder_extend_cost}",
                "callback": self.upgrades.extend_bladder_capacity,
            },
            {
                "icon_0": "assets/less_bladder_use_to_poop_butt0.png",
                "icon_1": "assets/less_bladder_use_to_poop_butt1.png",
                "text_func": lambda: (
                    f"Less bladder used when pooping. bladder value decrease per use for each poo type: "
                    f"{self.pet.bladder_value_decrease_units}. \n"
                    f"Current cost: {self.pet.less_bladder_use_cost}"
                ),
                "callback": self.upgrades.less_bladder_use,
            },
            {
                "icon_0": "assets/nutrition_up0.png",
                "icon_1": "assets/nutrition_up1.png",
                "text_func": lambda: (
                    f"Poop is more nutritious. bladder value return per poo eaten: "
                    f"{self.pet.bladder_value_increases_units}. \n"
                    f"Current cost: {self.pet.poo_return_more_bladder_cost}"
                ),
                "callback": self.upgrades.poo_return_more_bladder,
            },
            {
                "icon_0": "assets/auto_poop_time0.png",
                "icon_1": "assets/auto_poop_time1.png",
                "text_func": lambda: f"Pet poops on its own every {self.pet.auto_poop_interval / 1000:.1f}s. \nCurrent cost: {self.pet.auto_poop_cost}",
                "callback": self.upgrades.upgrade_auto_poop_timer,
            },
        ]
def get_menu_btn(self):
    return [
            {
                "icon_0": "assets/upgrades0.png",
                "icon_1": "assets/upgrades1.png",
                "text_func": lambda: "Upgrades",
                "callback": self.hide_upgrades
            },
            {
                "icon_0": "assets/skill0.png",
                "icon_1": "assets/skill1.png",
                "text_func": lambda: "Skills",
                "callback": self.hide_skills
            },
            {
                "icon_0": "assets/bars0.png",
                "icon_1": "assets/bars1.png",
                "text_func": lambda: "Hide upgrade, skill and info bars",
                "callback": self.hide_bars
            },
            {
                "icon_0": "assets/achivements0.png",
                "icon_1": "assets/achivements1.png",
                "text_func": lambda: "achievements",
                "callback": self.hide_achievements
            },
            {
                "icon_0": "assets/on_top0.png",
                "icon_1": "assets/on_top1.png",
                "text_func": lambda: "Panel always on top",
                "callback": self.panel_always_on_top
            },
            {
                "icon_0": "assets/minimize0.png",
                "icon_1": "assets/minimize1.png",
                "text_func": lambda: "minimise_panel",
                "callback": self.minimise_panel
            },
            {
                "icon_0": "assets/save_exit0.png",
                "icon_1": "assets/save_exit1.png",
                "text_func": lambda: "Save and exit",
                "callback": self.save_exit
            },
        ]
def get_skill_btn(self):
    return [
            {
                "icon_0": "assets/auto_poop_up0.png",
                "icon_1": "assets/auto_poop_up1.png",
                "text_func": lambda: f"Pet starts to poop on its own. \nCurrent cost: {self.pet.self_poop_skill_cost}",
                "callback": self.upgrades.auto_poop,
            },
            {
                "icon_0": "assets/double_poop_up1.png",
                "icon_1": "assets/double_poop_up0.png",
                "text_func": lambda: "Pet produces double the poop",
                "callback": self.double_poop_production
            },
        ]


def get_achievement_btn(self):
    buttons = []
    current_level = self.current_level

    def make_callback(poo_key):
        return lambda: self.achievement_stats(poo_key)

    def make_text_func(poo_key):
        return lambda: f"You unlocked {self.pet.POO_TYPES[poo_key].name.capitalize()} poop"

    for key, poo in self.pet.POO_TYPES.items():
        buttons.append({
            "icon_0": f"assets/poo/{key}_0.png",
            "icon_1": f"assets/poo/{key}_1.png",
            "text_func": make_text_func(key),
            "callback": make_callback(key),
            "enabled": current_level >= poo.min_level,
            "visible": current_level >= poo.min_level,
        })
    extra_buttons = [
        {
            "icon_0": "assets/pet/walk00.png",
            "icon_1": "assets/pet/idle00.png",
            "text_func": lambda: "You unlocked walk00",
            "callback": self.weak_achievement,
            "enabled": True,
            "visible": True,
        },
        {
            "icon_0": "assets/pet/walk10.png",
            "icon_1": "assets/pet/idle10.png",
            "text_func": lambda: "You unlocked walk10",
            "callback": self.weak_achievement,
            "enabled": True,
            "visible": True,
        },
    ]

    return buttons + extra_buttons



# def get_achievement_btn(self):
#     return [
#             {
#                 "icon_0": "assets/pet/walk00.png",
#                 "icon_1": "assets/pet/idle00.png",
#                 "text_func": lambda: "you unlocked weak poop",
#                 "callback": self.weak_achievement,
#                 # "enabled": False
#             },
#             {
#                 "icon_0": "assets/pet/walk10.png",
#                 "icon_1": "assets/pet/idle10.png",
#                 "text_func": lambda: "you unlocked weak poop",
#                 "callback": self.weak_achievement,
#                 # "enabled": False
#             },
#             {
#                 "icon_0": "assets/poo/weak_0.png",
#                 "icon_1": "assets/poo/weak_1.png",
#                 "text_func": lambda: "you unlocked weak poop",
#                 "callback": lambda: self.achievement_stats("weak"),
#                 # "enabled": False
#             },
#             {
#                 "icon_0": "assets/poo/normal_0.png",
#                 "icon_1": "assets/poo/normal_1.png",
#                 "text_func": lambda: "you unlocked weak poop",
#                 "callback": lambda: self.achievement_stats("normal"),
#                 # "enabled": False
#             },
#             {
#                 "icon_0": "assets/poo/bloody_0.png",
#                 "icon_1": "assets/poo/bloody_1.png",
#                 "text_func": lambda: "you unlocked weak poop",
#                 "callback": lambda: self.achievement_stats("bloody"),
#                 # "enabled": False
#             },
#             {
#                 "icon_0": "assets/poo/chilly_0.png",
#                 "icon_1": "assets/poo/chilly_1.png",
#                 "text_func": lambda: "you unlocked weak poop",
#                 "callback": lambda: self.achievement_stats("chilly"),
#                 # "enabled": False
#             },
#             {
#                 "icon_0": "assets/poo/corny_0.png",
#                 "icon_1": "assets/poo/corny_1.png",
#                 "text_func": lambda: "you unlocked weak poop",
#                 "callback": lambda: self.achievement_stats("corny"),
#                 # "enabled": False
#             },
#             {
#                 "icon_0": "assets/poo/egg_0.png",
#                 "icon_1": "assets/poo/egg_1.png",
#                 "text_func": lambda: "you unlocked weak poop",
#                 "callback": lambda: self.achievement_stats("egg"),
#                 # "enabled": False
#             },
#             {
#                 "icon_0": "assets/poo/gold_0.png",
#                 "icon_1": "assets/poo/gold_1.png",
#                 "text_func": lambda: "you unlocked weak poop",
#                 "callback": lambda: self.achievement_stats("gold"),
#                 # "enabled": False
#             },
#             {
#                 "icon_0": "assets/poo/hard_0.png",
#                 "icon_1": "assets/poo/hard_1.png",
#                 "text_func": lambda: "you unlocked weak poop",
#                 "callback": lambda: self.achievement_stats("hard"),
#                 # "enabled": False
#             },
#             {
#                 "icon_0": "assets/poo/monster_0.png",
#                 "icon_1": "assets/poo/monster_1.png",
#                 "text_func": lambda: "you unlocked weak poop",
#                 "callback": lambda: self.achievement_stats("monster"),
#                 # "enabled": False
#             },
#             {
#                 "icon_0": "assets/poo/silver_0.png",
#                 "icon_1": "assets/poo/silver_1.png",
#                 "text_func": lambda: "you unlocked weak poop",
#                 "callback": lambda: self.achievement_stats("silver"),
#                 # "enabled": False
#             },
#             {
#                 "icon_0": "assets/poo/toxic_0.png",
#                 "icon_1": "assets/poo/toxic_1.png",
#                 "text_func": lambda: "you unlocked weak poop",
#                 "callback": lambda: self.achievement_stats("toxic"),
#                 # "enabled": False
#             },
#             {
#                 "icon_0": "assets/poo/runny_0.png",
#                 "icon_1": "assets/poo/runny_1.png",
#                 "text_func": lambda: "you unlocked weak poop",
#                 "callback": lambda: self.achievement_stats("runny"),
#                 # "enabled": False
#             },
#         ]

