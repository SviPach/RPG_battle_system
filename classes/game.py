import random
import math
from  classes.magic import Spell


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
        self.hp_max = hp                # Maximum value of health points
        self.hp = hp                    # Current health points
        self.hp_critical = hp*0.2       # Critical value of health points
        self.mp_max = mp                # Maximum value of mana points
        self.mp = mp                    # Current mana points
        self.mp_critical = mp * 0.2     # Critical value of health points
        self.atk_low = atk-10           # Weakest physical damage
        self.atk_high = atk+10          # Strongest physical damage
        self.df = df                    # Defence
        self.magic = magic              # List of magic spells
        # Possible actions ->
        self.actions = ["Attack", "Magic", "Leave"]

    def generate_damage(self, spell = None):
        if spell is None:
            return random.randrange(self.atk_low, self.atk_high)
        else:
            dmg = spell.get_spell_damage()
            return random.randrange(dmg - 5, dmg + 5)

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

    def health_critical(self):
        return True if self.hp_critical >= self.hp else False

    def get_mp(self):
        return self.mp

    def get_mp_max(self):
        return self.mp_max

    def mana_critical(self):
        return True if self.mp_critical >= self.mp else False

    def reduce_mp(self, cost):
        self.mp -= cost

    def choose_action(self):
        while True:
            print(bcolors.OKBLUE + "Choose an action:" + bcolors.ENDC)
            for i in range(len(self.actions)):
                print(f"{i+1}. {self.actions[i]}")

            choice = int(input(f"{bcolors.UNDERLINE}Your choice:{bcolors.ENDC} ")) - 1
            if choice in range(len(self.actions)):
                return self.actions[choice]
            else:
                print(f"{bcolors.FAIL}{bcolors.UNDERLINE}There is no such an action!{bcolors.ENDC}")

    def choose_magic(self):
        while True:
            print(bcolors.OKBLUE +  "Choose a spell: \n(dmg, cost)" + bcolors.ENDC)
            for i in range(len(self.magic)):
                dmg = self.magic[i].get_spell_damage()
                print(f"{i + 1}. [{self.magic[i].get_spell_name()}]\t ({dmg-5}-{dmg+5}, {self.magic[i].get_spell_cost()})")

            print("0 - Attack with physical damage instead.")

            choice = int(input(f"{bcolors.UNDERLINE}Your choice:{bcolors.ENDC} ")) - 1

            if choice == -1:
                return None

            if choice in range(len(self.magic)):
                spell_name = self.magic[choice].get_spell_name()
                if self.magic[choice].get_spell_cost() > self.mp:
                    print(f"{bcolors.FAIL}{bcolors.UNDERLINE}Not enough MP!{bcolors.ENDC}")
                    continue
                else:
                    return self.magic[choice]
            else:
                print(bcolors.FAIL + bcolors.UNDERLINE + "There is no such a spell!" + bcolors.ENDC)
                continue

    def perform_attack(self, enemy, spell = None):
        if spell is not None:
            spell_cost = spell.get_spell_cost()
            self.reduce_mp(spell_cost)

            if spell.get_spell_type() == "Holy":
                heal = spell.get_spell_damage()
                self.hp += heal
                print(f"You've healed yourself by {bcolors.OKGREEN}{heal}{bcolors.ENDC}HP with {bcolors.WARNING}Physical attack{bcolors.ENDC}.")
                return
            else:
                dmg = self.generate_damage(spell)
        else:
            dmg = self.generate_damage()

        enemy_hp_old = enemy.hp
        enemy.take_damage(dmg)
        enemy_hp_new = enemy.hp

        if spell is None:
            spell_name = "Physical attack"
        else:
            spell_name = spell.get_spell_name()

        print(f"You are attacking for {dmg}HP with {bcolors.WARNING}{spell_name}{bcolors.ENDC}.")
        print(f"Enemy took damage: {bcolors.WARNING}-{enemy_hp_old - enemy_hp_new}HP.{bcolors.ENDC}")

    def info(self):
        print("Info:")
        print(f"HP: {self.hp}/{self.hp_max}")
        print(f"MP: {self.mp}/{self.mp_max}")
        print(f"Atk: {self.atk_low}-{self.atk_high}")
        print(f"Def: {self.df}")

    def info_short(self):
        info = f""
        if self.health_critical():
            info += f"{bcolors.FAIL}{self.get_hp()}{bcolors.ENDC}/{self.get_hp_max()}HP, "
        else:
            info += f"{self.get_hp()}/{self.get_hp_max()}HP, "

        if self.mana_critical():
            info += f"{bcolors.FAIL}{self.get_mp()}{bcolors.ENDC}/{self.get_mp_max()}MP"
        else:
            info += f"{self.get_mp()}/{self.get_mp_max()}MP"
        print(info)