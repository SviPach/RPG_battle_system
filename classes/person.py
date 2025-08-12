import random
import math
from classes import bc, get_choice


class Person:
    def __init__(
            self,
            name,
            hp,
            mp,
            atk,
            df,
            magic,
            dodge,
            crit_chance,
            crit_multiplier
    ):
        # Name
        self.name = name
        # Level
        self.level = 1
        # Kill count
        self.kill_count = 0
        # Experience points
        self.exp = 0                    # Current
        self.exp_needed = self.level    # For level-up

        # Health points
        self.hp_max = hp                # Maximum
        self.hp = hp                    # Current
        self.hp_critical = hp * 0.2       # Critical value

        # Mana points
        self.mp_max = mp                # Maximum
        self.mp = mp                    # Current
        self.mp_critical = mp * 0.2     # Critical value

        # Attack damage
        self.atk = atk                              # Default value
        self.atk_low = math.ceil(atk - atk * 0.4)   # Smallest
        self.atk_high = math.ceil(atk + atk * 0.4)  # Highest

        self.df = df                                # Defence
        self.dodge = dodge                          # Dodge chance
        self.magic = magic                          # List of magic spells

        # Critical hit
        self.crit_chance = crit_chance              # Chance
        self.crit_multiplier = crit_multiplier      # Damage multiplier (/10)

        # Switches for action states
        # --------------------------
        self.dodge_active = False           # "Dodge" action
        self.counterattack_active = False   # "Counterattack" action
        self.guard_active = False           # "Defensive stance"

        self.inventory = []     # Inventory of the player.

        # Possible actions
        # ----------------
        self.actions = [
            "Attack",
            "Magic",
            "Dodge",
            "Use potion",
            "Inspect",
            "Guard",
            "Command",
            "Leave"
        ]

        # Equipment
        # ---------
        # Head armor
        self.equipment_head = None
        # Torso armor
        self.equipment_torso = None
        # Legs armor
        self.equipment_legs = None
        # Feet armor
        self.equipment_feet = None
        # Weapon
        self.equipment_weapon = None

        # For allies
        # ----------
        self.recover_active = False

        # Attributes' levels
        # ------------------
        # Health capacity levels
        self.level_hp = 0           # Current
        self.level_hp_max = 10      # Maximum

        # Mana capacity levels
        self.level_mp = 0           # Current
        self.level_mp_max = 6       # Maximum

        # Attack levels
        self.level_atk = 0          # Current
        self.level_atk_max = 5      # Maximum

        # Defence levels
        self.level_df = 0           # Current
        self.level_df_max = 6       # Maximum

        # Dodge levels
        self.level_dodge = 0        # Current
        self.level_dodge_max = 9    # Maximum

        # Critical hit chance levels
        self.level_crit_chance = 0              # Current
        self.level_crit_chance_max = 12         # Maximum

        # Critical hit multiplier levels
        self.level_crit_multiplier = 0          # Current
        self.level_crit_multiplier_max = 6      # Maximum

    def generate_damage(self, spell=None):
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
            dmg = random.randrange(
                start=spell.get_damage()[0],
                stop=spell.get_damage()[1]
            )

        # Chance to perform a critical hit ->
        if (
                random.random() < self.crit_chance / 100
                or self.counterattack_active is True
        ):
            dmg = math.ceil(dmg * (self.crit_multiplier / 10))
            print(
                f"{bc.WARNING}{bc.UNDERLINE}{self.name} "
                f"makes a critical hit!{bc.ENDC}"
            )
            self.counterattack_active = False
            return dmg

        # Deactivate a counterattack and return damage to deal ->
        self.counterattack_active = False
        return dmg

    def take_damage(self, dmg):
        """
        Take damage by the player.

        Parameters
        ----------
        dmg : int
            Damage to take by this person.
        """
        # If incoming damage is more than 0 ->
        if dmg > 0:
            # Chance to dodge the attack ->
            if random.random() < self.dodge / 100:
                print(
                    f"{bc.WARNING}{bc.UNDERLINE}{self.name} dodged!{bc.ENDC}"
                )

                # If dodging is active ->
                if self.dodge_active:
                    self.dodge -= 30
                    self.dodge_active = False
                    self.counterattack_active = True
                    print(
                        f"{bc.WARNING}{bc.UNDERLINE}{self.name} "
                        f"is about to perform a counterattack!{bc.ENDC}"
                    )
                return

            # If dodging was active but did not dodge ->
            if self.dodge_active:
                self.dodge -= 30
                self.dodge_active = False

            # Damage to take ->
            dmg_taken = math.ceil(dmg * (100 - self.df) / 100)
            self.hp -= dmg_taken
            if self.hp < 0:
                self.hp = 0

            return
        else:
            # If dodging was active but did not dodge ->
            if self.dodge_active:
                self.dodge -= 30
                self.dodge_active = False

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

    def is_guard_active(self):
        """ Check if the guard is active. """
        return self.guard_active

    def equipment_obtain(self, equipment):
        """ Give the player equipment. """
        # Check slot where to assign this equipment ->
        slot = equipment.get_slot()
        match slot:
            case "head":
                self.equipment_head = equipment
            case "torso":
                self.equipment_torso = equipment
            case "legs":
                self.equipment_legs = equipment
            case "feet":
                self.equipment_feet = equipment
            case "weapon":
                self.equipment_weapon = equipment

        # String for print() function ->
        output = (
            f"{bc.OKBLUE}{bc.UNDERLINE}{self.name}{bc.ENDC} "
            f"equipped {bc.WARNING}{equipment.get_name()}{bc.ENDC}: "
            f"{bc.OKBLUE}+{equipment.get_prop()}"
        )

        # Check the attribute this equipment improves ->
        prop_type = equipment.get_prop_type()
        match prop_type:
            case "atk":
                self.atk += equipment.get_prop()
                self.atk_low = math.ceil(self.atk - self.atk * 0.4)
                self.atk_high = math.ceil(self.atk + self.atk * 0.4)
                output += f"DMG{bc.ENDC}"
            case "df":
                self.df += equipment.get_prop()
                output += f" defence{bc.ENDC}"
            case "dodge":
                self.dodge += equipment.get_prop()
                output += f"% dodge{bc.ENDC}"

        print(output)

    def potion_obtain(self, potion):
        """ Get the potion. """
        print(f"You have obtained: {bc.WARNING}{potion.get_name()}{bc.ENDC}.")
        self.inventory.append(potion)

    def potion_choose(self):
        """ Choose a potion. """
        print(bc.OKBLUE + "-------------------------" + bc.ENDC)
        print(bc.OKBLUE + "Choose the potion to use:" + bc.ENDC)
        # List of potions ->
        for i in range(len(self.inventory)):
            print(
                f"{i + 1}. {bc.WARNING}{self.inventory[i].get_name()}{bc.ENDC}"
                f" - {self.inventory[i].get_description()}."
            )

        # If player don't wat to choose a potion ->
        print("0 - Cancel.")

        # Choosing the potion ->
        choice = get_choice(
            amount_of_choices_to_clear=len(self.inventory) + 1,
            min_choice_possible=-1,
            max_choice_possible=len(self.inventory) - 1
        )

        # If canceled ->
        if choice == -1:
            print(
                f"You {bc.OKBLUE}{bc.UNDERLINE}"
                f"did not choose{bc.ENDC} a potion."
            )
            return

        # Potion use ->
        print(
            f"You chose "
            f"{bc.WARNING}{bc.UNDERLINE}"
            f"{self.inventory[choice].get_name()}{bc.ENDC}."
        )
        self.potion_use(self.inventory[choice])

    def potion_use(self, potion):
        """ Use the potion. """
        # Check type of the potion ->
        if potion.get_type() == "health":
            # If it's a healing potion ->
            print(
                f"You have healed yourself by "
                f"{bc.OKGREEN}{potion.get_prop()}{bc.ENDC}HP "
                f"with {bc.WARNING}{potion.get_name()}{bc.ENDC}."
            )
            self.heal(potion.get_prop())
            print(
                f"{bc.UNDERLINE}{bc.OKBLUE}{self.name}{bc.ENDC}: "
                f"{self.info_short()}"
            )

            # Removing the used potion from player's inventory ->
            self.inventory.remove(potion)
        elif potion.get_type() == "mana":
            # If it's a mana potion ->
            print(
                f"You have restored your MP by "
                f"{bc.OKBLUE}{potion.get_prop()}{bc.ENDC}MP "
                f"with {bc.WARNING}{potion.get_name()}{bc.ENDC}."
            )
            self.restore_mana(potion.get_prop())
            print(
                f"{bc.UNDERLINE}{bc.OKBLUE}{self.name}{bc.ENDC}: "
                f"{self.info_short()}"
            )

            # Removing the used potion from player's inventory ->
            self.inventory.remove(potion)

    def choose_action(self):
        """ Chooses an action. """
        print(bc.OKBLUE + "-------------------------" + bc.ENDC)
        print(bc.OKBLUE + "Choose an action:" + bc.ENDC)
        # List of actions ->
        for i in range(len(self.actions)):
            print(f"{i + 1}. {self.actions[i]}")

        # Choosing an action ->
        choice = get_choice(
            amount_of_choices_to_clear=len(self.actions),
            min_choice_possible=0,
            max_choice_possible=len(self.actions) - 1
        )

        print(
            f"You chose "
            f"{bc.OKBLUE}{bc.UNDERLINE}{self.actions[choice]}{bc.ENDC}."
        )
        return self.actions[choice]

    def get_name(self):
        """ Get the name of the player. """
        return self.name

    def heal(self, hp):
        """ Heal the player. """
        hp_old = self.hp
        self.hp += hp
        if self.hp > self.hp_max:
            self.hp = self.hp_max
        hp_new = self.hp
        print(
            f"{bc.UNDERLINE}{bc.OKBLUE}{self.name}{bc.ENDC}: "
            f"{bc.OKGREEN}+{hp}HP{bc.ENDC} "
            f"({bc.OKGREEN}+{hp_new - hp_old}{bc.ENDC})"
        )

    def heal_full(self):
        """ Fully heal the player. """
        hp_gain = self.hp_max - self.hp
        print(
            f"{bc.UNDERLINE}{bc.OKBLUE}{self.name}{bc.ENDC}: "
            f"{bc.OKGREEN}+{hp_gain}HP{bc.ENDC}"
        )
        self.hp = self.hp_max

    def restore_mana(self, mp):
        """ Restore player's mana. """
        mp_old = self.mp
        self.mp += mp
        if self.mp > self.mp_max:
            self.mp = self.mp_max
        mp_new = self.mp
        print(
            f"{bc.UNDERLINE}{bc.OKBLUE}{self.name}{bc.ENDC}: "
            f"{bc.OKBLUE}+{mp}MP{bc.ENDC} "
            f"({bc.OKBLUE}+{mp_new - mp_old}{bc.ENDC})"
        )

    def restore_mana_full(self):
        """ Fully restore player's mana. """
        mp_gain = self.mp_max - self.mp
        print(
            f"{bc.UNDERLINE}{bc.OKBLUE}{self.name}{bc.ENDC}: "
            f"{bc.OKBLUE}+{mp_gain}MP{bc.ENDC}"
        )
        self.mp = self.mp_max

    def choose_magic(self):
        """ Chooses a magic spell. """
        print(bc.OKBLUE + "-------------------------" + bc.ENDC)
        print(bc.OKBLUE + "Choose a spell: \n(dmg, cost)" + bc.ENDC)
        # List of the magic spells ->
        for i in range(len(self.magic)):
            spell = self.magic[i]
            dmg_low = spell.get_damage()[0]
            dmg_high = spell.get_damage()[1]
            print(
                f"{i + 1}. [{bc.WARNING}{spell.get_name()}{bc.ENDC}]  --  "
                f"({bc.FAIL}{dmg_low}-{dmg_high}{bc.ENDC}, "
                f"{bc.OKBLUE}{spell.get_cost()}{bc.ENDC})  --  "
                f"{spell.get_description()}"
            )

        # In case if player doesn't want to attack with magic ->
        print(f"0 - Attack with {bc.WARNING}physical damage{bc.ENDC} instead.")

        # Player's choice ->
        choice = get_choice(len(self.magic) + 2, -1, len(self.magic) - 1)

        # If player chose a physical attack instead of magic ->
        if choice == -1:
            print(
                f"You chose "
                f"{bc.WARNING}{bc.UNDERLINE}Physical attack{bc.ENDC} "
                f"instead of magic spell."
            )
            return None

        # If player doesn't have enough MP ->
        if self.magic[choice].get_cost() > self.mp:
            print(f"{bc.FAIL}{bc.UNDERLINE}Not enough MP!{bc.ENDC}")
            return -1
        else:
            print(
                f"You chose "
                f"{bc.WARNING}{bc.UNDERLINE}"
                f"{self.magic[choice].get_name()}{bc.ENDC}."
            )
            return self.magic[choice]

    def perform_attack(self, enemy, spell=None, party_leader=None):
        """
        Perform the attack by the player.

        Parameters
        ----------
        enemy : Person
            The enemy to attack.
        spell : Spell
            The spell to perform attack with.
        party_leader : Person
            Leader of this player's party.
        """
        # If attack is performed by magic ->
        if spell is not None:
            spell_cost = spell.get_cost()
            self.reduce_mp(spell_cost)

            # If the magic spell has a "Holy" type ->
            if spell.get_type() == "Holy":
                hp = spell.get_damage()[2]
                # The healing result ->
                print(
                    f"You've healed yourself by "
                    f"{bc.OKGREEN}{hp}{bc.ENDC}HP "
                    f"with {bc.WARNING}{spell.get_name()}{bc.ENDC}."
                )
                self.heal(hp)
                return
            elif spell.get_type() == "Holy_support":
                hp = spell.get_damage()[2]
                # The healing result ->
                print(
                    f"{bc.UNDERLINE}{bc.OKBLUE}{self.name}{bc.ENDC} healed "
                    f"{bc.UNDERLINE}{bc.OKBLUE}"
                    f"{party_leader.get_name()}{bc.ENDC} "
                    f"by {bc.OKGREEN}{hp}{bc.ENDC}HP "
                    f"with {bc.WARNING}{spell.get_name()}{bc.ENDC}."
                )
                party_leader.heal(hp)
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
        print(
            f"{bc.UNDERLINE}{bc.OKBLUE}{self.name}{bc.ENDC} "
            f"attacking for {bc.WARNING}{dmg}{bc.ENDC}HP "
            f"with {bc.WARNING}{spell_name}{bc.ENDC}."
        )

        # Dealing damage to the enemy and printing out the result ->
        enemy_hp_old = enemy.hp
        enemy.take_damage(dmg)
        enemy_hp_new = enemy.hp
        print(
            f"--> {bc.UNDERLINE}{bc.OKBLUE}{enemy.get_name()}{bc.ENDC} "
            f"took damage: "
            f"{bc.WARNING}-{enemy_hp_old - enemy_hp_new}HP.{bc.ENDC}"
        )

    def try_dodge(self):
        """ Try to dodge the next attack. """
        self.dodge += 30
        self.dodge_active = True
        print(
            f"{bc.UNDERLINE}{bc.OKBLUE}{self.name}{bc.ENDC} "
            f"tries to {bc.WARNING}dodge{bc.ENDC}!"
        )

    def guard_activate(self):
        """ Enter the defensive stance to reduce incoming damage. """
        self.df += 40
        self.guard_active = True
        print(
            f"{bc.UNDERLINE}{bc.OKBLUE}{self.name}{bc.ENDC} "
            f"enters a {bc.WARNING}defensive state{bc.ENDC}!"
        )

    def guard_deactivate(self):
        """ Quit the defensive stance. """
        self.df -= 40
        self.guard_active = False

    def inspect(self, entities):
        """ Inspect yourself or the enemy. """
        print(bc.OKBLUE + "-------------------------" + bc.ENDC)
        print(bc.OKBLUE + "Choose who to inspect: " + bc.ENDC)
        # List of actions ->
        i = 1
        for entity in entities:
            print(
                f"{i}. {bc.UNDERLINE}{bc.OKBLUE}"
                f"{entity.get_name()}{bc.ENDC}"
            )
            i += 1
        print("0. Cancel")

        # Player's choice ->
        choice = get_choice(
            amount_of_choices_to_clear=len(entities) + 1,
            min_choice_possible=-1,
            max_choice_possible=len(entities) - 1
        )

        # If player doesn't want to inspect anybody ->
        if choice == -1:
            print(
                f"You {bc.OKBLUE}{bc.UNDERLINE}"
                f"did not inspect{bc.ENDC} anybody."
            )
            return

        # Check if there is such an entity to inspect ->
        print(
            f"You inspect {bc.OKBLUE}{bc.UNDERLINE}"
            f"{entities[choice].name}{bc.ENDC}."
        )
        entities[choice].info()

    def command(self, player_party):
        """ Command a member of the player's party. """
        if len(player_party) > 1:
            print(bc.OKBLUE + "-------------------------" + bc.ENDC)
            print(bc.OKBLUE + "Choose who to command: " + bc.ENDC)
            # List of allies in player's party ->
            i = 1
            for person in player_party[1:]:
                print(
                    f"{i}. {bc.UNDERLINE}{bc.OKBLUE}"
                    f"{person.get_name()}{bc.ENDC}"
                )
                i += 1
            print("0. Cancel")

            # Player's choice ->
            choice = get_choice(
                amount_of_choices_to_clear=(player_party[:1]) + 1,
                min_choice_possible=-1,
                max_choice_possible=len(player_party[:1]) - 1
            )

            # If player doesn't want to command anybody ->
            if choice == -1:
                print(f"You {bc.OKBLUE}{bc.UNDERLINE}"
                      f"did not command{bc.ENDC} anybody.")
                return

            # Check if there is such an option ->
            player_party[choice + 1].recover_switch()
        else:
            print(
                bc.FAIL + bc.UNDERLINE
                + "You're alone in your party!"
                + bc.ENDC
            )

    def recover_switch(self):
        """ Switch the recover state. """
        if not self.recover_active:
            print(f"{bc.UNDERLINE}{bc.OKBLUE}{self.name}{bc.ENDC} "
                  f"is now {bc.WARNING}recovering{bc.ENDC}!")
            self.recover_active = True
        else:
            print(f"{bc.UNDERLINE}{bc.OKBLUE}{self.name}{bc.ENDC} "
                  f"is now {bc.WARNING}fighting{bc.ENDC}!")
            self.recover_active = False

    def is_recover_active(self):
        """ Gets the recovery state of the npc. """
        return self.recover_active

    def kill_count_increase(self):
        """ Increase the count of kills and exp by 1. """
        self.kill_count += 1
        self.exp += 1
        print(f"{bc.UNDERLINE}{bc.OKBLUE}{self.name}{bc.ENDC}: "
              f"{bc.HEADER}+1EXP{bc.ENDC}")

    def level_up(self):
        """ Level up the player. """
        if self.exp == self.exp_needed:
            print(f"{bc.HEADER}{bc.UNDERLINE}===== LEVEL UP! ====={bc.ENDC}")
            # Cleaning before leveling up ->
            self.guard_active = False
            self.dodge_active = False
            self.counterattack_active = False

            # Level-up requirements update ->
            self.level += 1
            self.exp = 0
            self.exp_needed = self.level

            # Level-up bonus ->
            self.heal_full()
            self.restore_mana_full()

            # List of all possible attributes ->
            attributes = []
            if self.level_hp < self.level_hp_max:
                attributes.append("HP")
            if self.level_mp < self.level_mp_max:
                attributes.append("MP")
            if self.level_atk < self.level_atk_max:
                attributes.append("Atk")
            if self.level_df < self.level_df_max:
                attributes.append("Df")
            if self.level_dodge < self.level_dodge_max:
                attributes.append("Dodge")
            if self.level_crit_chance < self.level_crit_chance_max:
                attributes.append("Crit_chance")
            if self.level_crit_multiplier < self.level_crit_multiplier_max:
                attributes.append("Crit_mult")

            # If all the attributes have maximum level ->
            if len(attributes) == 0:
                print(
                    bc.HEADER + bc.UNDERLINE
                    + "ALL THE ATTRIBUTES ARE UPGRADED!"
                    + bc.ENDC
                )
                return
            else:
                # Choosing 3 random attributes ->
                attributes_available = []
                for i in range(3):
                    item = random.choice(attributes)
                    attributes_available.append(item)
                    attributes.remove(item)
                    if len(attributes) == 0:
                        break

            print(f"{bc.HEADER}{bc.UNDERLINE}=== CHOOSE A REWARD:{bc.ENDC}")
            # Show the attributes player can upgrade ->
            i = 1
            for item in attributes_available:
                match item:
                    case "HP":
                        print(
                            f"{i}. {bc.OKBLUE}{bc.UNDERLINE}{item}{bc.ENDC}: "
                            f"Increase your "
                            f"{bc.WARNING}maximum HP{bc.ENDC} "
                            f"by {bc.OKGREEN}10{bc.ENDC}.")
                    case "MP":
                        print(
                            f"{i}. {bc.OKBLUE}{bc.UNDERLINE}{item}{bc.ENDC}: "
                            f"Increase your "
                            f"{bc.WARNING}maximum MP{bc.ENDC} "
                            f"by {bc.OKGREEN}5{bc.ENDC}."
                        )
                    case "Atk":
                        print(
                            f"{i}. {bc.OKBLUE}{bc.UNDERLINE}{item}{bc.ENDC}: "
                            f"Increase your "
                            f"{bc.WARNING}base attack{bc.ENDC} "
                            f"by {bc.OKGREEN}2{bc.ENDC}."
                        )
                    case "Df":
                        print(
                            f"{i}. {bc.OKBLUE}{bc.UNDERLINE}{item}{bc.ENDC}: "
                            f"Increase your "
                            f"{bc.WARNING}defence{bc.ENDC} "
                            f"by {bc.OKGREEN}5{bc.ENDC}."
                        )
                    case "Dodge":
                        print(
                            f"{i}. {bc.OKBLUE}{bc.UNDERLINE}{item}{bc.ENDC}: "
                            f"Increase your "
                            f"{bc.WARNING}dodge chance{bc.ENDC} "
                            f"by {bc.OKGREEN}5%{bc.ENDC}."
                        )
                    case "Crit_chance":
                        print(
                            f"{i}. {bc.OKBLUE}{bc.UNDERLINE}{item}{bc.ENDC}: "
                            f"Increase your "
                            f"{bc.WARNING}critical hit chance{bc.ENDC} "
                            f"by {bc.OKGREEN}4%{bc.ENDC}."
                        )
                    case "Crit_mult":
                        print(
                            f"{i}. {bc.OKBLUE}{bc.UNDERLINE}{item}{bc.ENDC}: "
                            f"Increase your "
                            f"{bc.WARNING}critical hit multiplier{bc.ENDC} "
                            f"by {bc.OKGREEN}0.2{bc.ENDC}."
                        )
                i += 1

            # Choosing the attribute to upgrade ->
            choice = get_choice(
                amount_of_choices_to_clear=len(attributes_available),
                min_choice_possible=0,
                max_choice_possible=len(attributes_available) - 1
            )

            # Check if there is such a choice ->
            chosen_attribute = attributes_available[choice]

            # Upgrading the player, depending on his choice ->
            match chosen_attribute:
                case "HP":
                    print(
                        f"{bc.OKBLUE}{bc.UNDERLINE}You chose{bc.ENDC}: "
                        f"{bc.OKGREEN}+10 maximum HP{bc.ENDC}!"
                    )
                    self.hp_max += 10
                    self.hp = self.hp_max
                case "MP":
                    print(
                        f"{bc.OKBLUE}{bc.UNDERLINE}You chose{bc.ENDC}: "
                        f"{bc.OKGREEN}+5 maximum MP{bc.ENDC}!"
                    )
                    self.mp_max += 5
                    self.mp = self.mp_max
                case "Atk":
                    print(
                        f"{bc.OKBLUE}{bc.UNDERLINE}You chose{bc.ENDC}: "
                        f"{bc.OKGREEN}+2 base attack{bc.ENDC}!"
                    )
                    self.atk += 2
                    self.atk_low = math.ceil(self.atk - self.atk * 0.4)
                    self.atk_high = math.ceil(self.atk + self.atk * 0.4)
                case "Df":
                    print(
                        f"{bc.OKBLUE}{bc.UNDERLINE}You chose{bc.ENDC}: "
                        f"{bc.OKGREEN}+5 defence{bc.ENDC}!"
                    )
                    self.df += 5
                case "Dodge":
                    print(
                        f"{bc.OKBLUE}{bc.UNDERLINE}You chose{bc.ENDC}: "
                        f"{bc.OKGREEN}+5% dodge chance{bc.ENDC}!"
                    )
                    self.dodge += 5
                case "Crit_chance":
                    print(
                        f"{bc.OKBLUE}{bc.UNDERLINE}You chose{bc.ENDC}: "
                        f"{bc.OKGREEN}+4% critical hit chance{bc.ENDC}!"
                    )
                    self.crit_chance += 4
                case "Crit_mult":
                    print(
                        f"{bc.OKBLUE}{bc.UNDERLINE}You chose{bc.ENDC}: "
                        f"{bc.OKGREEN}+0.2 critical hit multiplier{bc.ENDC}!"
                    )
                    self.crit_multiplier += 2

    def info(self):
        """ Full information about the player. """
        print(bc.OKBLUE + "-------------------------" + bc.ENDC)
        print(
            f"{bc.OKBLUE}==============={bc.ENDC}"
            f" Full info about "
            f"{bc.UNDERLINE}{bc.OKBLUE}{self.name}{bc.ENDC}:"
        )

        # Name ->
        print(
            f"\t"
            f"{bc.OKBLUE}Level{bc.ENDC}: {self.level}"
        )

        # EXP ->
        print(
            f"\t"
            f"{bc.OKBLUE}Experience{bc.ENDC}: {self.exp}/{self.exp_needed}"
        )

        # HP ->
        print(
            f"\t"
            f"{bc.OKBLUE}HP{bc.ENDC}: {self.hp}/{self.hp_max}"
        )

        # MP ->
        print(
            f"\t"
            f"{bc.OKBLUE}MP{bc.ENDC}: {self.mp}/{self.mp_max}"
        )

        # Attack damage ->
        print(
            f"\t"
            f"{bc.OKBLUE}Atk dmg{bc.ENDC}: {self.atk_low}-{self.atk_high}"
        )

        # Attack damage (base) ->
        print(
            f"\t"
            f"{bc.OKBLUE}Atk dmg (base){bc.ENDC}: "
            f"{self.atk}"
        )

        # Defence ->
        print(
            f"\t"
            f"{bc.OKBLUE}Def{bc.ENDC}: "
            f"{self.df}"
        )

        # Dodge ->
        print(
            f"\t"
            f"{bc.OKBLUE}Dodge chance{bc.ENDC}: "
            f"{self.dodge}%"
        )

        # Critical hit chance ->
        print(
            f"\t"
            f"{bc.OKBLUE}Critical hit chance{bc.ENDC}: "
            f"{self.crit_chance}%"
        )

        # Critical hit multiplier ->
        print(
            f"\t"
            f"{bc.OKBLUE}Critical hit multiplier{bc.ENDC}: "
            f"x{self.crit_multiplier / 10}"
        )

        # Inventory ->
        inventory = []
        for item in self.inventory:
            inventory.append(item.get_name())
        print(f"\t{bc.OKBLUE}Inventory{bc.ENDC}: {inventory}")

        # Kill count ->
        print(f"\t{bc.OKBLUE}Kill count{bc.ENDC}: {self.kill_count}")

    def info_short(self):
        """ Short information about the player. """
        # HP ->
        info = ""
        if self.health_critical():
            info += (
                f"{bc.FAIL}"
                f"{self.get_hp()}"
                f"{bc.ENDC}{bc.OKGREEN}"
                f"/{self.get_hp_max()}"
                f"{bc.ENDC}"
                f"HP, "
            )
        else:
            info += (
                f"{bc.OKGREEN}"
                f"{self.get_hp()}/{self.get_hp_max()}"
                f"{bc.ENDC}"
                f"HP, "
            )

        # MP ->
        if self.mana_critical():
            info += (
                f"{bc.FAIL}"
                f"{self.get_mp()}"
                f"{bc.ENDC}{bc.OKBLUE}"
                f"/{self.get_mp_max()}"
                f"{bc.ENDC}"
                f"MP"
            )
        else:
            info += (
                f"{bc.OKBLUE}"
                f"{self.get_mp()}/{self.get_mp_max()}"
                f"{bc.ENDC}"
                f"MP"
            )
        return info
