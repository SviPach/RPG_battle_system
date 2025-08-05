import random
import math


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Person:
    def __init__(self, hp, mp, atk, df, magic):
        self.hp_max = hp
        self.hp = hp
        self.hp_critical = hp*0.2
        self.mp_max = mp
        self.mp = mp
        self.mp_critical = mp * 0.2
        self.atk_low = atk-10
        self.atk_high = atk+10
        self.df = df
        self.magic = magic
        self.actions = ["Attack", "Magic"]

    def generate_damage(self):
        return random.randrange(self.atk_low, self.atk_high)

    def generate_spell_damage(self, spell):
        if spell == "Physical attack":
            return self.generate_damage()

        for item in self.magic:
            if item["name"] == spell:
                self.reduce_mp(item["cost"])

                return random.randrange(item["dmg"] - 5, item["dmg"] + 5)

    def take_damage(self, dmg):
        dmg_taken = math.ceil(dmg * (1 - self.df/100))
        self.hp -= dmg_taken
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def get_hp(self):
        return self.hp

    def get_hp_max(self):
        return self.hp_max

    def get_mp(self):
        return self.mp

    def get_mp_max(self):
        return self.mp_max

    def reduce_mp(self, cost):
        self.mp -= cost

    def choose_action(self):
        print("Choose an action:")
        for i in range(len(self.actions)):
            print(f"{i+1}. {self.actions[i]}")

        choice = int(input("Your choice: ")) - 1
        if choice in range(len(self.actions)):
            return self.actions[choice]

    def choose_magic(self):
        print("Choose a spell:"
              "\n(dmg, cost)")
        for i in range(len(self.magic)):
            dmg = self.magic[i]["dmg"]
            print(f"{i + 1}. [{self.magic[i]["name"]}]\t ({dmg-5}-{dmg+5}, {self.magic[i]["cost"]})")

        print("0 - Attack with physical damage instead.")

        choice = int(input("Your choice: ")) - 1

        if choice == -1:
            return "Physical attack"

        if choice in range(len(self.magic)):
            return self.magic[choice]["name"]

    def info(self):
        print("Info:")
        print(f"HP: {self.hp}/{self.hp_max}")
        print(f"MP: {self.mp}/{self.mp_max}")
        print(f"Atk: {self.atk_low}-{self.atk_high}")
        print(f"Def: {self.df}")
