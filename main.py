from classes import *


# Creating some magic spells ->
spell_fire = Spell("Fire", 8, 14, "Elemental")
spell_thunder = Spell("Thunder", 10, 20, "Elemental")
spell_kill = Spell("Instant kill", 0, 1000, "Elemental")
spell_cure = Spell("Cure", 5, 20, "Holy")
spell_healing_light = Spell("Healing Light", 8, 20, "Holy_support")

# Adding recently created magic to the list ->
magic = [spell_fire, spell_thunder, spell_kill, spell_cure]
magic_elf = [spell_fire, spell_healing_light]

# Instantiate entities ->
player = Person("Player", 100, 20, 10, 20, magic, 20, 12, 1.4)
enemy = Person("Enemy", 100, 0, 8, 15, None, 15, 12, 1.4)
elf = Person("Carlos the Elf", 30, 40, 4, 6, magic_elf, 35, 8, 1.4)
elf_found = False

# Player's party ->
player_party = [player]

# All the entities ->
entities_met = [player, enemy]

# Creating a health potion ->
health_potion = Potion("Health potion", "health", f"Heals a player by {bc.OKGREEN}50HP{bc.ENDC}", 50)
mana_potion = Potion("Mana potion", "mana", f"Restores player's MP by {bc.OKBLUE}20MP{bc.ENDC}", 20)

# Adding potions to the player's inventory.
for i in range(3):
    player.potion_obtain(health_potion)
for i in range(3):
    player.potion_obtain(mana_potion)
erase_lines(6)

# Our battlefield ->
print(bc.FAIL + bc.BOLD + "AN ENEMY ATTACKS!" + bc.ENDC)
print(bc.UNDERLINE + bc.HEADER + "TO START THE NEXT TURN -> PRESS ANY KEY" + bc.ENDC)
running_battlefield = True
enemy_dodging = False           # If enemy has it active -> he won't try to dodge again in the next turn
while running_battlefield:
    msvcrt.getch()
    print(bc.HEADER + bc.BOLD + "======================================== Next turn! ========================================" + bc.ENDC)
    # MP passive restoring ->
    for person in player_party:
        if person.get_mp() < person.get_mp_max():
            if person.is_guard_active():
                mp_multiplier = 0.2
            else:
                mp_multiplier = 0.1
            person.restore_mana(math.ceil(person.get_mp_max()*mp_multiplier))

    # Player's guard deactivation ->
    if player.is_guard_active():
        player.guard_deactivate()

    # Short info about player and enemy at the start of every turn ->
    for person in player_party:
        print(bc.HEADER + f"===== {person.get_name()}: " + bc.ENDC)
        print(person.info_short())
    print(bc.HEADER + f"===== {enemy.get_name()}: " + bc.ENDC)
    print(enemy.info_short())

    # Player's turn ->
    running_player = True
    while running_player:
        choice = player.choose_action()
        if choice == "Attack":
            print(bc.FAIL + "========================= Attack time! =========================" + bc.ENDC)
            player.perform_attack(enemy)
            running_player = False
        elif choice == "Magic":
            spell = player.choose_magic()
            print(bc.FAIL + "========================= Attack time! =========================" + bc.ENDC)
            player.perform_attack(enemy, spell)
            running_player = False
        elif choice == "Dodge":
            print(bc.FAIL + "========================= Attack time! =========================" + bc.ENDC)
            player.try_dodge()
            running_player = False
        elif choice == "Use potion":
            player.potion_choose()
        elif choice == "Inspect":
            player.inspect(entities_met)
        elif choice == "Guard":
            print(bc.FAIL + "========================= Attack time! =========================" + bc.ENDC)
            player.guard_activate()
            running_player = False
        elif choice == "Leave":
            print(bc.FAIL + "==================================================" + bc.ENDC)
            print(bc.FAIL + bc.BOLD + "You've left the battlefield!" + bc.ENDC)
            print(bc.FAIL + "==================================================" + bc.ENDC)
            running_player = False
            running_battlefield = False

    # If player have left the battlefield ->
    if not running_battlefield:
        break

    # Player's party members' turn ->
    running_player_party = True
    if len(player_party) > 1:
        for person in player_party[1:]:
            if person.get_name() == "Carlos the Elf":
                print(bc.FAIL + "==============================" + bc.ENDC)
                # Case 1: if Carlos the Elf has enough MP to use magic spells ->
                if person.get_mp() >= 8:
                    # Case 1-1: if player doesn't have full hp ->
                    if player.get_hp() < player.get_hp_max():
                        # Case 1-1-1: 50% chance to cast Fire ->
                        if random.random() < 0.5:
                            person.perform_attack(enemy, person.magic[0])
                        # Case 1-1-2: 50% chance to cast Healing Light ->
                        else:
                            person.perform_attack(enemy, person.magic[1], player)
                    # Case 1-2: if player has full hp ->
                    else:
                        person.perform_attack(enemy, person.magic[0])
                # Case 2: if Carlos the Elf doesn't have enough MP to use magic spells ->
                else:
                    person.perform_attack(enemy)

    # If enemy has been defeated ->
    if enemy.get_hp() == 0:
        print(bc.FAIL + "================================================================" + bc.ENDC)
        print(bc.OKGREEN + bc.BOLD + "You won!" + bc.ENDC)
        player.kill_count_increase()
        player.level_up()
        print(bc.FAIL + "================================================================" + bc.ENDC)
        msvcrt.getch()
        print(bc.HEADER + bc.BOLD + "================================================================================" + bc.ENDC)
        # Creating a new enemy ->
        entities_met.remove(enemy)
        print(bc.FAIL + bc.BOLD + "Next enemy is attacking!" + bc.ENDC)
        enemy = Person("Enemy", enemy.get_hp_max()+5, 0, enemy.get_atk() + 5, enemy.get_df() + 5,
                       None, enemy.get_dodge() + 5, enemy.get_crit_chance()+5, enemy.get_crit_multiplier()+0.1)
        enemy.info()
        entities_met.append(enemy)
        print(bc.OKBLUE + "-------------------------")
        print(bc.HEADER + bc.BOLD + "================================================================================" + bc.ENDC)
        msvcrt.getch()
        # If Carlos the Elf ha snot been found yet ->
        if not elf_found:
            # 20% chance to meet Carlos the Elf ->
            if random.random() < 1:
                print(f"{bc.OKBLUE}{bc.UNDERLINE}You just met{bc.ENDC} {bc.HEADER}{elf.get_name()}{bc.ENDC}!")
                player_party.append(elf)
                elf_found = True
                print(f"{bc.HEADER}{elf.get_name()}{bc.ENDC} can cast {bc.WARNING}Fire{bc.ENDC} and {bc.WARNING}Healing Light{bc.ENDC}.")
                entities_met.append(elf)
        # print(f"{bc.OKGREEN}You have recovered!{bc.ENDC}")
        # player.heal_full()
        # player.restore_mana_full()
        continue

    print(bc.FAIL + "==============================" + bc.ENDC)
    # Enemy's turn ->
    if random.random() < 0.2 and not enemy_dodging:
        # 20% chance that enemy will try to dodge ->
        enemy.try_dodge()
        enemy_dodging = True
    else:
        # 80% chance that enemy will attack ->
        enemy.perform_attack(player)
        enemy_dodging = False

    # If player has been defeated ->
    if player.get_hp() == 0:
        print(bc.FAIL + bc.BOLD + "You lost!" + bc.ENDC)
        print(bc.FAIL + "================================================================" + bc.ENDC)
        running_battlefield = False
    else:
        print(bc.FAIL + "================================================================" + bc.ENDC)