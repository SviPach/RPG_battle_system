import random
import math
from classes import bc, erase_lines


class Person:
    def __init__(self, name, hp, mp, atk, df, magic, dodge, crit_chance, crit_multiplier):
        self.name = name                # Name.
        self.hp_max = hp                # Maximum value of health points.
        self.hp = hp                    # Current health points.
        self.hp_critical = hp*0.2       # Critical value of health points.
        self.mp_max = mp                # Maximum value of mana points.
        self.mp = mp                    # Current mana points.
        self.mp_critical = mp * 0.2                 # Critical value of mana points.
        self.atk = atk                              # Default attack value.
        self.atk_low = math.ceil(atk - atk*0.4)     # Weakest physical damage.
        self.atk_high = math.ceil(atk + atk*0.4)    # Strongest physical damage.
        self.df = df                                # Defence.
        self.magic = magic                          # List of magic spells.
        self.dodge = dodge                          # Dodge chance.
        self.dodge_active = False                   # If dodge action is active.
        self.crit_chance = crit_chance              # Critical hit chance.
        self.crit_multiplier = crit_multiplier      # Critical hit damage multiplier.
        self.counterattack_active = False           # If counterattack is active.
        self.inventory = []                         # Inventory of the player.
        # Possible actions ->
        self.actions = ["Attack", "Magic", "Dodge", "Use potion", "Inspect", "Leave"]

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
            dmg = random.randrange(spell.get_damage()[0], spell.get_damage()[1])

        # Chance to perform a critical hit ->
        if random.randrange(100) in range(self.crit_chance) or self.counterattack_active is True:
            dmg = math.ceil(dmg * self.crit_multiplier)
            print(f"{bc.WARNING}{bc.UNDERLINE}{self.name} makes a critical hit!{bc.ENDC}")
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
            print(f"{bc.WARNING}{bc.UNDERLINE}{self.name} dodged!{bc.ENDC}")
            # If dodging is active ->
            if self.dodge_active:
                self.dodge -= 30
                self.dodge_active = False
                self.counterattack_active = True
                print(f"{bc.WARNING}{bc.UNDERLINE}{self.name} is about to perform a counterattack!{bc.ENDC}")
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

    def get_atk(self):
        """ Get the player's default attack value. """
        return self.atk

    def get_df(self):
        """ Get the player's defence value. '"""
        return self.df

    def get_dodge(self):
        """ Get the player's dodge chance. """
        return self.dodge

    def get_crit_chance(self):
        """ Get the player's critical chance. """
        return self.crit_chance

    def get_crit_multiplier(self):
        """ Get the player's critical multiplier. """
        return self.crit_multiplier

    def reduce_mp(self, cost):
        """ Reduce player's MP. """
        self.mp -= cost

    def potion_obtain(self, potion):
        """ Get the potion. """
        print(f"You have obtained: {bc.WARNING}{potion.get_name()}{bc.ENDC}.")
        self.inventory.append(potion)

    def potion_choose(self):
        """ Choose a potion. """
        while True:
            print(bc.OKBLUE + "-------------------------")
            print(bc.OKBLUE + "Choose the potion to use:" + bc.ENDC)
            # List of potions ->
            for i in range(len(self.inventory)):
                print(f"{i+1}. {bc.WARNING}{self.inventory[i].get_name()}{bc.ENDC} - {self.inventory[i].get_description()}.")
            # If player don't wat to choose a potion ->
            print("0 - Cancel.")
            # Choosing the potion ->
            try:
                choice = int(input(f"{bc.UNDERLINE}Your choice:{bc.ENDC} ")) - 1
                erase_lines(len(self.inventory) + 2)
            except ValueError:
                erase_lines(len(self.inventory) + 2)
                print(f"{bc.FAIL}{bc.UNDERLINE}Please enter the number!{bc.ENDC}")
                continue
            # If canceled ->
            if choice == -1:
                print(f"You {bc.OKBLUE}{bc.UNDERLINE}did not choose{bc.ENDC} a potion.")
                break
            # Checking if there is such a potion ->
            if choice in range(len(self.inventory)):
                print(f"You chose {bc.WARNING}{bc.UNDERLINE}{self.inventory[choice].get_name()}{bc.ENDC}.")
                self.potion_use(self.inventory[choice])
                break
            else:
                print(f"{bc.FAIL}{bc.UNDERLINE}There is no such a potion!{bc.ENDC}")

    def potion_use(self, potion):
        """ Use the potion. """
        if potion.get_type() == "health":
            print(f"You have healed yourself by {bc.OKGREEN}{potion.get_prop()}{bc.ENDC}HP "
                  f"with {bc.WARNING}{potion.get_name()}{bc.ENDC}.")
            self.heal(potion.get_prop())
            print(f"{bc.UNDERLINE}{bc.OKBLUE}{self.name}{bc.ENDC}: {self.info_short()}")
            self.inventory.remove(potion)
        elif potion.get_type() == "mana":
            print(f"You have restored your MP by {bc.OKBLUE}{potion.get_prop()}{bc.ENDC}MP "
                  f"with {bc.WARNING}{potion.get_name()}{bc.ENDC}.")
            self.restore_mana(potion.get_prop())
            print(f"{bc.UNDERLINE}{bc.OKBLUE}{self.name}{bc.ENDC}: {self.info_short()}")
            self.inventory.remove(potion)


    def choose_action(self):
        """ Chooses an action. """
        while True:
            print(bc.OKBLUE + "-------------------------")
            print(bc.OKBLUE + "Choose an action:" + bc.ENDC)
            # List of actions ->
            for i in range(len(self.actions)):
                print(f"{i+1}. {self.actions[i]}")
            # Choosing an action ->
            try:
                choice = int(input(f"{bc.UNDERLINE}Your choice:{bc.ENDC} ")) - 1
                erase_lines(7)
            except ValueError:
                erase_lines(7)
                print(f"{bc.FAIL}{bc.UNDERLINE}Please enter the number!{bc.ENDC}")
                continue
            # Checking if there is such a choice ->
            if choice in range(len(self.actions)):
                print(f"You chose {bc.OKBLUE}{bc.UNDERLINE}{self.actions[choice]}{bc.ENDC}.")
                return self.actions[choice]
            else:
                print(f"{bc.FAIL}{bc.UNDERLINE}There is no such an action!{bc.ENDC}")

    def get_name(self):
        """ Get the name of the player. """
        return self.name

    def heal(self, hp):
        """ Heals the player. """
        print(f"{bc.UNDERLINE}{bc.OKBLUE}{self.name}{bc.ENDC}: {bc.OKGREEN}+{hp}HP{bc.ENDC}")
        self.hp += hp
        if self.hp > self.hp_max:
            self.hp = self.hp_max

    def heal_full(self):
        """ Fully heal the player. """
        hp_gain = self.hp_max - self.hp
        print(f"{bc.UNDERLINE}{bc.OKBLUE}{self.name}{bc.ENDC}: {bc.OKGREEN}+{hp_gain}HP{bc.ENDC}")
        self.hp = self.hp_max

    def restore_mana(self, mp):
        """ Restore mana of the player. """
        print(f"{bc.UNDERLINE}{bc.OKBLUE}{self.name}{bc.ENDC}: {bc.OKBLUE}+{mp}MP{bc.ENDC}")
        self.mp += mp
        if self.mp > self.mp_max:
            self.mp = self.mp_max

    def restore_mana_full(self):
        """ Fully restore mana of the player. """
        mp_gain = self.mp_max - self.mp
        print(f"{bc.UNDERLINE}{bc.OKBLUE}{self.name}{bc.ENDC}: {bc.OKGREEN}+{mp_gain}MP{bc.ENDC}")
        self.mp = self.mp_max

    def choose_magic(self):
        """ Chooses a magic spell. """
        while True:
            print(bc.OKBLUE + "-------------------------")
            print(bc.OKBLUE +  "Choose a spell: \n(dmg, cost)" + bc.ENDC)
            # List of the magic spells ->
            for i in range(len(self.magic)):
                dmg_low = self.magic[i].get_damage()[0]
                dmg_high = self.magic[i].get_damage()[1]
                print(f"{i + 1}. [{bc.WARNING}{self.magic[i].get_name()}{bc.ENDC}]\t "
                      f"({bc.FAIL}{dmg_low}-{dmg_high}{bc.ENDC}, {bc.OKBLUE}{self.magic[i].get_cost()}{bc.ENDC})")

            # In case if player doesn't want to attack with magic ->
            print(f"0 - Attack with {bc.WARNING}physical damage{bc.ENDC} instead.")

            # Player's choice ->
            try:
                choice = int(input(f"{bc.UNDERLINE}Your choice:{bc.ENDC} ")) - 1
                erase_lines(len(self.magic)+3)
            except ValueError:
                erase_lines(len(self.magic)+3)
                print(f"{bc.FAIL}{bc.UNDERLINE}Please enter the number!{bc.ENDC}")
                continue
            # If player chose a physical attack instead of magic ->
            if choice == -1:
                print(f"You chose {bc.WARNING}{bc.UNDERLINE}Physical attack{bc.ENDC} instead of magic spell.")
                return None

            # Checking if there is such a choice ->
            if choice in range(len(self.magic)):
                # If player doesn't have enough MP ->
                if self.magic[choice].get_cost() > self.mp:
                    print(f"{bc.FAIL}{bc.UNDERLINE}Not enough MP!{bc.ENDC}")
                    continue
                else:
                    print(f"You chose {bc.WARNING}{bc.UNDERLINE}{self.magic[choice].get_name()}{bc.ENDC}.")
                    return self.magic[choice]
            else:
                print(bc.FAIL + bc.UNDERLINE + "There is no such a spell!" + bc.ENDC)
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
            spell_cost = spell.get_cost()
            self.reduce_mp(spell_cost)

            # If the magic spell has a "Holy" type ->
            if spell.get_type() == "Holy":
                hp = spell.get_damage()[2]
                # The healing result ->
                print(f"You've healed yourself by {bc.OKGREEN}{hp}{bc.ENDC}HP with {bc.WARNING}{spell.get_name()}{bc.ENDC}.")
                self.heal(hp)
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
            spell_name = spell.get_name()
        print(f"{bc.OKBLUE}{self.name}{bc.ENDC} attacking for {bc.WARNING}{dmg}{bc.ENDC}HP with {bc.WARNING}{spell_name}{bc.ENDC}.")

        # Dealing damage to the enemy and printing out the result ->
        enemy_hp_old = enemy.hp
        enemy.take_damage(dmg)
        enemy_hp_new = enemy.hp
        print(f"--> {bc.OKBLUE}{enemy.get_name()}{bc.ENDC} took damage: {bc.WARNING}-{enemy_hp_old - enemy_hp_new}HP.{bc.ENDC}")

    def try_dodge(self):
        """ Try to dodge the next attack. """
        self.dodge += 30
        self.dodge_active = True
        print(f"{bc.OKBLUE}{self.name}{bc.ENDC} tries to {bc.WARNING}dodge{bc.ENDC}!")

    def inspect(self, enemy):
        """ Inspect yourself or the enemy. """
        while True:
            print(bc.OKBLUE + "-------------------------")
            print(bc.OKBLUE + "Choose who to inspect: " + bc.ENDC)
            print(f"1. Yourself\n2. Enemy\n3. Cancel")
            choice = input(f"{bc.UNDERLINE}Your choice:{bc.ENDC} ")
            erase_lines(4)
            if choice == '1':
                print(f"You inspect {bc.OKBLUE}{bc.UNDERLINE}{self.name}{bc.ENDC}.")
                self.info()
                break
            elif choice == '2':
                print(f"You inspect {bc.OKBLUE}{bc.UNDERLINE}{enemy.get_name()}{bc.ENDC}.")
                enemy.info()
                break
            elif choice == '3':
                print(f"You inspect {bc.OKBLUE}{bc.UNDERLINE}no one{bc.ENDC}.")
            else:
                print(bc.FAIL + bc.UNDERLINE + "There is no such a choice" + bc.ENDC)
                continue

    def info(self):
        """ Full information about the player. """
        print(bc.OKBLUE + "-------------------------")
        print(f"{bc.OKBLUE}==============={bc.ENDC} Full info about {bc.OKBLUE}{self.name}{bc.ENDC}:")
        print(f"{bc.OKBLUE}HP{bc.ENDC}: {self.hp}/{self.hp_max}")
        print(f"{bc.OKBLUE}MP{bc.ENDC}: {self.mp}/{self.mp_max}")
        print(f"{bc.OKBLUE}Atk dmg{bc.ENDC}: {self.atk_low}-{self.atk_high}")
        print(f"{bc.OKBLUE}Atk dmg (base){bc.ENDC}: {self.atk}")
        print(f"{bc.OKBLUE}Def{bc.ENDC}: {self.df}")
        print(f"{bc.OKBLUE}Dodge chance{bc.ENDC}: {self.dodge}%")
        print(f"{bc.OKBLUE}Critical hit chance{bc.ENDC}: {self.crit_chance}%")
        print(f"{bc.OKBLUE}Critical hit multiplier{bc.ENDC}: x{self.crit_multiplier}")
        inventory = []
        for item in self.inventory:
            inventory.append(item.get_name())
        print(f"{bc.OKBLUE}Inventory{bc.ENDC}: {inventory}")

    def info_short(self):
        """ Short information about the player. """
        info = f""
        if self.health_critical():
            info += f"{bc.FAIL}{self.get_hp()}{bc.ENDC}{bc.OKGREEN}/{self.get_hp_max()}{bc.ENDC}HP, "
        else:
            info += f"{bc.OKGREEN}{self.get_hp()}/{self.get_hp_max()}{bc.ENDC}HP, "

        if self.mana_critical():
            info += f"{bc.FAIL}{self.get_mp()}{bc.ENDC}{bc.OKBLUE}/{self.get_mp_max()}{bc.ENDC}MP"
        else:
            info += f"{bc.OKBLUE}{self.get_mp()}/{self.get_mp_max()}{bc.ENDC}MP"
        return info