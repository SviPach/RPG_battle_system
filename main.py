

from classes import *


# Instantiate some magic spells ->
spell_fireball = Spell(
    name="Fireball",
    cost=7,
    dmg=12,
    prop_optional=2,
    type="fire",
    description=f"Cast a fireball dealing {bc.WARNING}12DMG{bc.ENDC}. "
                f"Enemy takes {bc.WARNING}2DMG{bc.ENDC} in the next 3 turns.",
)
spell_thunderbolt = Spell(
    name="Thunderbolt",
    cost=10,
    dmg=18,
    prop_optional=0,
    type="thunder",
    description=f"Cast a thunderbolt dealing {bc.WARNING}18DMG{bc.ENDC}.",
)
spell_ice_storm = Spell(
    name="Ice Storm",
    cost=14,
    dmg=4,
    prop_optional=2,
    type="ice",
    description=f"Cast an ice storm dealing {bc.WARNING}4DMG{bc.ENDC}. "
                f"Freeze the enemy for {bc.WARNING}2 turns{bc.ENDC}",
)
spell_kill = Spell(
    name="Instant kill",
    cost=0,
    dmg=1000,
    prop_optional=0,
    type="thunder",
    description=f"God's power - {bc.WARNING}instant kill{bc.ENDC}. "
                f"(for testing purposes)",
)
spell_cure = Spell(
    name="Cure",
    cost=5,
    dmg=20,
    prop_optional=0,
    type="holy",
    description=f"Heal yourself by {bc.OKGREEN}20HP{bc.ENDC}",
)
spell_healing_light = Spell(
    name="Healing Light",
    cost=8,
    dmg=20,
    prop_optional=0,
    type="holy_support",
    description=f"Heal your party leader by {bc.OKGREEN}20HP{bc.ENDC}",
)

# Adding recently created magic to the list ->
magic = [spell_fireball, spell_thunderbolt, spell_ice_storm, spell_kill, spell_cure]
magic_elf = [spell_fireball, spell_healing_light]

# Instantiate equipment ->
armor_head_1 = Equipment(
    name="Soldier's helmet",
    slot="head",
    prop=5,
    prop_type="df",
    description=f"Soldier's iron helmet. "
                f"Additional head armor: "
                f"{bc.OKBLUE}+5 defence{bc.ENDC}.",
)
armor_torso_1 = Equipment(
    name="Soldier's chest plate",
    slot="torso",
    prop=6,
    prop_type="df",
    description=f"Soldier's iron chest plate. "
                f"Additional torso armor: "
                f"{bc.OKBLUE}+6 defence{bc.ENDC}.",
)
armor_legs_1 = Equipment(
    name="Soldier's legs armor",
    slot="legs",
    prop=4,
    prop_type="df",
    description=f"Soldier's iron legs armor. "
                f"Additional legs armor: "
                f"{bc.OKBLUE}+4 defence{bc.ENDC}.",
)
armor_feet_1 = Equipment(
    name="Work boots",
    slot="feet",
    prop=8,
    prop_type="dodge",
    description=f"Boots from some worker. "
                f"Makes it easier to dodge: "
                f"{bc.OKBLUE}+8% dodge chance{bc.ENDC}.",
)
weapon_1 = Equipment(
    name="Soldier's sword",
    slot="weapon",
    prop=6,
    prop_type="atk",
    description=f"Soldier's iron sword. "
                f"Increases damage: "
                f"{bc.OKBLUE}+6 attack damage{bc.ENDC}.",
)

# Adding equipment to array ->
equipment_available = [
    armor_head_1,
    armor_torso_1,
    armor_legs_1,
    armor_feet_1,
    weapon_1,
]

# Instantiate entities ->
player = Person(
    name="Player",
    hp=100,
    mp=20,
    atk=10,
    df=20,
    magic=magic,
    dodge=20,
    crit_chance=12,
    crit_multiplier=14,
)
enemy = Person(
    name="Enemy",
    hp=100,
    mp=0,
    atk=8,
    df=15,
    magic=None,
    dodge=15,
    crit_chance=12,
    crit_multiplier=14,
)
elf = Person(
    name="Carlos the Elf",
    hp=30,
    mp=40,
    atk=4,
    df=6,
    magic=magic_elf,
    dodge=35,
    crit_chance=8,
    crit_multiplier=14,
)
elf_found = False

# Player's party ->
player_party = [player]

# All the entities ->
entities_met = [player, enemy]

# Instantiate a health and mana potion ->
health_potion = Potion(
    name="Health potion",
    type="health",
    description=f"Heals a player by {bc.OKGREEN}50HP{bc.ENDC}",
    prop=50,
)
mana_potion = Potion(
    name="Mana potion",
    type="mana",
    description=f"Restores player's MP by {bc.OKBLUE}20MP{bc.ENDC}",
    prop=20,
)

# Adding potions to the player's inventory.
for i in range(3):
    player.potion_obtain(health_potion)
for i in range(3):
    player.potion_obtain(mana_potion)
erase_lines(6)

# Our battlefield ->
print(bc.FAIL + bc.BOLD + "AN ENEMY ATTACKS!" + bc.ENDC)
print(
    bc.UNDERLINE
    + bc.HEADER
    + "TO START THE NEXT TURN -> PRESS ANY KEY"
    + bc.ENDC
)
running_battlefield = True
enemy_dodging = False  # For enemy: to don't dodge after dodge
new_battle = False
while running_battlefield:
    if not new_battle:
        msvcrt.getch()
    else:
        new_battle = False

    # Turn start ->
    print(bc.HEADER + bc.BOLD + "======================================== Next turn! ========================================" + bc.ENDC)  # noqa: E501

    # MP passive restoring ->
    for person in player_party:
        if person.get_mp() < person.get_mp_max():
            if person.is_guard_active():
                mp_multiplier = 0.2
            elif person.is_recover_active():
                mp_multiplier = 0.2
            else:
                mp_multiplier = 0.1
            person.restore_mana(round(person.get_mp_max() * mp_multiplier))

    # HP passive restoring ->
    for person in player_party:
        if person.is_knocked_active():
            person.heal(round(person.get_hp_max() * 0.1))

    # Player's guard deactivation ->
    if player.is_guard_active():
        player.guard_deactivate()

    # Player's turn ->
    running_player = True
    while running_player:
        print("NAME                 HP                        MP         ")
        for person in player_party:
            print(person.info_graphic())
        print(enemy.info_graphic())

        choice = player.choose_action()
        match choice:
            case "Attack":
                print(bc.FAIL + "========================= Attack time! =========================" + bc.ENDC)  # noqa: E501
                player.perform_attack(enemy)
                running_player = False
            case "Magic":
                spell = player.choose_magic()
                if spell == -1:
                    continue
                print(bc.FAIL + "========================= Attack time! =========================" + bc.ENDC)  # noqa: E501
                player.perform_attack(enemy, spell)
                running_player = False
            case "Dodge":
                print(bc.FAIL + "========================= Attack time! =========================" + bc.ENDC)  # noqa: E501
                player.try_dodge()
                running_player = False
            case "Use potion":
                player.potion_choose(player_party)
            case "Inspect":
                player.inspect(entities_met)
            case "Guard":
                print(bc.FAIL + "========================= Attack time! =========================" + bc.ENDC)  # noqa: E501
                player.guard_activate()
                running_player = False
            case "Command":
                player.command(player_party)
            case "Leave":
                print(bc.FAIL + "==================================================" + bc.ENDC)  # noqa: E501
                print(
                    bc.FAIL
                    + bc.BOLD
                    + "You've left the battlefield!"
                    + bc.ENDC
                )
                print(bc.FAIL + "==================================================" + bc.ENDC)  # noqa: E501
                msvcrt.getch()
                running_player = False
                running_battlefield = False

    # If player have left the battlefield ->
    if not running_battlefield:
        break

    # Player's party members' turn ->
    if len(player_party) > 1:
        for person in player_party[1:]:
            # If person is knocked ->
            if person.is_knocked_active():
                print(bc.FAIL + "==============================" + bc.ENDC)
                if person.get_hp() == person.get_hp_max():
                    person.knocked_switch()
                    continue
                print(f"{bc.UNDERLINE}{bc.OKBLUE}{person.name}{bc.ENDC} "
                      f"is {bc.FAIL}knocked{bc.ENDC}!")
                continue

            # If this person is recovering ->
            if person.is_recover_active():
                print(bc.FAIL + "==============================" + bc.ENDC)
                print(f"{bc.OKBLUE}{person.name}{bc.ENDC} "
                      f"is {bc.WARNING}recovering{bc.ENDC}!")
                continue

            # Carlos the Elf's AI ->
            if person.get_name() == "Carlos the Elf":
                print(bc.FAIL + "==============================" + bc.ENDC)
                # Case 1: if Carlos has enough MP to use magic ->
                if person.get_mp() >= 8:
                    # Case 1-1: if player doesn't have full hp ->
                    if player.get_hp() < player.get_hp_max():
                        # Case 1-1-1: 50% chance to cast Fire ->
                        if random.random() < 0.5:
                            person.perform_attack(
                                enemy,
                                person.magic[0],
                            )
                        # Case 1-1-2: 50% chance to cast Healing Light ->
                        else:
                            person.perform_attack(
                                enemy,
                                person.magic[1],
                                player)
                    # Case 1-2: if player has full hp ->
                    else:
                        person.perform_attack(
                            enemy,
                            person.magic[0],
                        )
                # Case 2: if Carlos doesn't have enough MP to use magic ->
                else:
                    person.perform_attack(enemy)

    # If enemy has been defeated ->
    if enemy.get_hp() == 0:
        print(bc.FAIL + "================================================================" + bc.ENDC)  # noqa: E501
        print(bc.OKGREEN + bc.BOLD + "You won!" + bc.ENDC)
        player.kill_count_increase()
        player.level_up()
        print(bc.FAIL + "================================================================" + bc.ENDC)  # noqa: E501

        msvcrt.getch()

        # Creating a new enemy ->
        print(bc.HEADER + bc.BOLD + "================================================================================" + bc.ENDC)  # noqa: E501
        entities_met.remove(enemy)
        print(bc.FAIL + bc.BOLD + "Next enemy is attacking!" + bc.ENDC)
        enemy = Person(
            name="Enemy",
            hp=enemy.get_hp_max() + 5,
            mp=0,
            atk=enemy.get_atk() + 1,
            df=enemy.get_df() + 3,
            magic=None,
            dodge=enemy.get_dodge() + 4,
            crit_chance=enemy.get_crit_chance() + 4,
            crit_multiplier=enemy.get_crit_multiplier() + 1,
        )
        enemy.info()
        entities_met.append(enemy)
        print(bc.OKBLUE + "-------------------------" + bc.ENDC)
        print(bc.HEADER + bc.BOLD + "================================================================================" + bc.ENDC)  # noqa: E501

        msvcrt.getch()

        # 60% chance to find an equipment chest ->
        if random.random() < 0.6 and len(equipment_available) > 0:
            print(bc.OKBLUE + "-------------------------" + bc.ENDC)
            print(f"{bc.HEADER}You found an equipment chest!{bc.ENDC}")
            # 40% chance to get equipment from chest ->
            if random.random() < 0.4:
                equipment = random.choice(equipment_available)
                print(f"You found: {bc.WARNING}{equipment.get_name()}{bc.ENDC} - "
                      f"{equipment.get_description()}")
                equipment_available.remove(equipment)
                player.equipment_obtain(equipment)
            else:
                potion = random.choice([health_potion, mana_potion])
                player.potion_obtain(potion)
            print(bc.OKBLUE + "-------------------------" + bc.ENDC)
            msvcrt.getch()

        # If Carlos the Elf has not been found yet ->
        if not elf_found:
            # 20% chance to meet Carlos the Elf ->
            if random.random() < 0.2:
                print(bc.OKBLUE + "-------------------------" + bc.ENDC)
                print(f"{bc.OKBLUE}{bc.UNDERLINE}You just met{bc.ENDC} "
                      f"{bc.HEADER}{elf.get_name()}{bc.ENDC}!")
                player_party.append(elf)
                elf_found = True
                print(f"{bc.HEADER}{elf.get_name()}{bc.ENDC} can cast "
                      f"{bc.WARNING}Fire{bc.ENDC} and "
                      f"{bc.WARNING}Healing Light{bc.ENDC}.")
                entities_met.append(elf)
                print(bc.OKBLUE + "-------------------------" + bc.ENDC)
                msvcrt.getch()

        # 20% chance to find a campfire ->
        if random.random() < 0.2:
            print(bc.OKBLUE + "-------------------------" + bc.ENDC)
            print(f"{bc.HEADER}You found a campfire!{bc.ENDC}")
            print(f"{bc.OKGREEN}You have recovered!{bc.ENDC}")
            for person in player_party:
                person.heal_full()
                person.restore_mana_full()
            print(bc.OKBLUE + "-------------------------" + bc.ENDC)
            msvcrt.getch()

        # Start a new turn ->
        new_battle = True
        continue

    print(bc.FAIL + "==============================" + bc.ENDC)

    # Enemy's turn ->
    enemy.burn()
    enemy.defrost()
    if not enemy.is_frozen_active():
        if random.random() < 0.2 and not enemy_dodging:
            # 20% chance that enemy will try to dodge ->
            enemy.try_dodge()
            enemy_dodging = True
        else:
            enemy_dodging = False
            # 80% chance that enemy will attack ->
            while True:
                target = random.choice(player_party)
                if not target.is_knocked_active():
                    enemy.perform_attack(target)
                    break

    for person in player_party[1:]:
        if person.get_hp() == 0:
            # If ally's HP is 0 ->
            if person.get_hp() == 0:
                person.knocked_switch()
                continue

    # If player has been defeated ->
    if player.get_hp() == 0:
        print(bc.FAIL + bc.BOLD + "You lost!" + bc.ENDC)
        print(bc.FAIL + "================================================================" + bc.ENDC)  # noqa: E501
        msvcrt.getch()
        running_battlefield = False
    else:
        print(bc.FAIL + "================================================================" + bc.ENDC)  # noqa: E501
