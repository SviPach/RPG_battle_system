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
    def __init__(self, name, hp, mp, atk, df, magic, dodge, crit_chance, crit_multiplier):
        self.name = name                # Name.
        self.hp_max = hp                # Maximum value of health points.
        self.hp = hp                    # Current health points.
        self.hp_critical = hp*0.2       # Critical value of health points.
        self.mp_max = mp                # Maximum value of mana points.
        self.mp = mp                    # Current mana points.
        self.mp_critical = mp * 0.2                 # Critical value of health points.
        self.atk_low = math.ceil(atk - atk*0.4)     # Weakest physical damage.
        self.atk_high = math.ceil(atk + atk*0.4)    # Strongest physical damage.
        self.df = df                                # Defence.
        self.magic = magic                          # List of magic spells.
        self.dodge = dodge                          # Dodge chance.
        self.dodge_active = False                   # If dodge action is active.
        self.critical_chance = crit_chance          # Critical hit chance.
        self.critical_multiplier = crit_multiplier  # Critical hit damage multiplier.
        self.counterattack_active = False           # If counterattack is active.
        self.inventory = []                         # Inventory of the player.
        # Possible actions ->
        self.actions = ["Attack", "Magic", "Dodge", "Use potion", "Leave"]

    def generate_damage(self, spell = None):
        """
        Generate the damage.

        Parameters
        ----------
        spell : Spell
            The spell to calculate damage for.

        Returns
        -------
        int
            Damage to perform by this person.
        """
        # Generating the damage ->
        if spell is None:
            dmg = random.randrange(self.atk_low, self.atk_high)
        else:
            dmg = random.randrange(spell.get_spell_damage()[0], spell.get_spell_damage()[1])

        # Chance to perform a critical hit ->
        if random.randrange(100) in range(self.critical_chance) or self.counterattack_active is True:
            dmg = math.ceil(dmg * self.critical_multiplier)
            print(f"{bcolors.WARNING}{bcolors.UNDERLINE}{self.name} makes a critical hit!{bcolors.ENDC}")
            self.counterattack_active = False
            return dmg

        self.counterattack_active = False
        return dmg

    def take_damage(self, dmg):
        """
        Take damage by the player.

        Parameters
        ----------
        dmg : int
            Damage to take by this person.

        Returns
        -------
        int
            HP of this person after the attack.
        """
        # Chance to dodge the attack ->
        if random.randrange(100) in range(self.dodge):
            print(f"{bcolors.WARNING}{bcolors.UNDERLINE}{self.name} dodged!{bcolors.ENDC}")
            # If dodging is active ->
            if self.dodge_active:
                self.dodge -= 30
                self.dodge_active = False
                self.counterattack_active = True
                print(f"{bcolors.WARNING}{bcolors.UNDERLINE}{self.name} is about to perform a counterattack!{bcolors.ENDC}")
            return self.hp

        # If dodging was active but did not dodge ->
        if self.dodge_active:
            self.dodge -= 30
            self.dodge_active = False

        # Damage to take ->
        dmg_taken = math.ceil(dmg * (100 - self.df)/100)
        self.hp -= dmg_taken
        if self.hp < 0:
            self.hp = 0

        return self.hp

    def get_hp(self):
        """ Get the player's HP. """
        return self.hp

    def get_hp_max(self):
        """ Get the player's maximum HP. '"""
        return self.hp_max

    def health_critical(self):
        """ Check if the player's health is critical. '"""
        return True if self.hp_critical >= self.hp else False

    def get_mp(self):
        """ Get the player's MP. '"""
        return self.mp

    def get_mp_max(self):
        """ Get the player's maximum MP. '"""
        return self.mp_max

    def mana_critical(self):
        """ Check if the player's mana is critical. '"""
        return True if self.mp_critical >= self.mp else False

    def reduce_mp(self, cost):
        """ Reduce player's MP. """
        self.mp -= cost

    def potion_obtain(self, potion):
        """ Get the potion. """
        print(f"You have obtained: {bcolors.WARNING}{potion.get_name()}{bcolors.ENDC}.")
        self.inventory.append(potion)

    def potion_choose(self):
        """ Choose a potion. """
        while True:
            # List of potions ->
            print(bcolors.OKBLUE + "Choose the potion to use:" + bcolors.ENDC)
            for i in range(len(self.inventory)):
                print(f"{i+1}. {self.inventory[i].get_name()} - {self.inventory[i].get_description()}.")
            # Choosing the potion ->
            choice = int(input(f"{bcolors.UNDERLINE}Your choice:{bcolors.ENDC} ")) - 1
            # Checking if there is such a potion ->
            if choice in range(len(self.inventory)):
                self.potion_use(self.inventory[choice])
                break
            else:
                print(f"{bcolors.FAIL}{bcolors.UNDERLINE}There is no such a potion!{bcolors.ENDC}")

    def potion_use(self, potion):
        """ Use the potion. """
        if potion.get_type() == "health":
            self.heal(potion.get_prop())
            print(f"You have healed yourself by {bcolors.OKGREEN}{potion.get_prop()}{bcolors.ENDC}HP "
                  f"with {bcolors.WARNING}{potion.get_name()}{bcolors.ENDC}.")
            if self.hp > self.hp_max:
                self.hp = self.hp_max
            self.inventory.remove(potion)


    def choose_action(self):
        """ Chooses an action. """
        while True:
            # List of actions ->
            print(bcolors.OKBLUE + "Choose an action:" + bcolors.ENDC)
            for i in range(len(self.actions)):
                print(f"{i+1}. {self.actions[i]}")
            # Choosing an action ->
            choice = int(input(f"{bcolors.UNDERLINE}Your choice:{bcolors.ENDC} ")) - 1
            # Checking if there is such a choice ->
            if choice in range(len(self.actions)):
                return self.actions[choice]
            else:
                print(f"{bcolors.FAIL}{bcolors.UNDERLINE}There is no such an action!{bcolors.ENDC}")

    def get_name(self):
        """ Get the name of the player. """
        return self.name

    def heal(self, hp):
        """ Heals the player. """
        self.hp += hp

    def choose_magic(self):
        """ Chooses a magic spell. """
        while True:
            print(bcolors.OKBLUE +  "Choose a spell: \n(dmg, cost)" + bcolors.ENDC)
            # List of the magic spells ->
            for i in range(len(self.magic)):
                dmg_low = self.magic[i].get_spell_damage()[0]
                dmg_high = self.magic[i].get_spell_damage()[1]
                print(f"{i + 1}. [{self.magic[i].get_spell_name()}]\t ({dmg_low}-{dmg_high}, {self.magic[i].get_spell_cost()})")

            # In case if player doesn't want to attack with magic ->
            print("0 - Attack with physical damage instead.")

            # Player's choice ->
            choice = int(input(f"{bcolors.UNDERLINE}Your choice:{bcolors.ENDC} ")) - 1

            # If player chose a physical attack instead of magic ->
            if choice == -1:
                return None

            # Checking if there is such a choice ->
            if choice in range(len(self.magic)):
                # If player doesn't have enough MP ->
                if self.magic[choice].get_spell_cost() > self.mp:
                    print(f"{bcolors.FAIL}{bcolors.UNDERLINE}Not enough MP!{bcolors.ENDC}")
                    continue
                else:
                    return self.magic[choice]
            else:
                print(bcolors.FAIL + bcolors.UNDERLINE + "There is no such a spell!" + bcolors.ENDC)
                continue

    def perform_attack(self, enemy, spell = None):
        """
        Perform the attack by the player.

        Parameters
        ----------
        enemy : Person
            The enemy to attack.
        spell : Spell
            The spell to perform attack with.
        """
        # If attack is performed by magic ->
        if spell is not None:
            spell_cost = spell.get_spell_cost()
            self.reduce_mp(spell_cost)

            # If the magic spell has a "Holy" type ->
            if spell.get_spell_type() == "Holy":
                hp = spell.get_spell_damage()[2]
                self.heal(hp)
                # The healing result ->
                print(f"You've healed yourself by {bcolors.OKGREEN}{hp}{bcolors.ENDC}HP with {bcolors.WARNING}{spell.get_spell_name()}{bcolors.ENDC}.")
                return
            else:
                dmg = self.generate_damage(spell)
        # If attack is performed by physical attack ->
        else:
            dmg = self.generate_damage()

        # The attack result ->
        if spell is None:
            spell_name = "Physical attack"
        else:
            spell_name = spell.get_spell_name()
        print(f"{bcolors.OKBLUE}{self.name}{bcolors.ENDC} attacking for {dmg}HP with {bcolors.WARNING}{spell_name}{bcolors.ENDC}.")

        # Dealing damage to the enemy and printing out the result ->
        enemy_hp_old = enemy.hp
        enemy.take_damage(dmg)
        enemy_hp_new = enemy.hp
        print(f"--> {bcolors.OKBLUE}{enemy.get_name()}{bcolors.ENDC} took damage: {bcolors.WARNING}-{enemy_hp_old - enemy_hp_new}HP.{bcolors.ENDC}")

    def try_dodge(self):
        """ Try to dodge the next attack. """
        self.dodge += 30
        self.dodge_active = True
        print(f"{bcolors.OKBLUE}{self.name}{bcolors.ENDC} tries to dodge!")

    def info(self):
        """ Full information about the player. """
        print("Info:")
        print(f"HP: {self.hp}/{self.hp_max}")
        print(f"MP: {self.mp}/{self.mp_max}")
        print(f"Atk: {self.atk_low}-{self.atk_high}")
        print(f"Def: {self.df}")

    def info_short(self):
        """ Short information about the player. """
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