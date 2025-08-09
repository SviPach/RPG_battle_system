from classes import *

# Creating some magic spells ->
spell_Fire = Spell("Fire", 8, 16, "Elemental")
spell_Thunder = Spell("Thunder", 10, 20, "Elemental")
spell_Ice = Spell("Ice", 5, 10, "Elemental")
spell_Cure = Spell("Cure", 5, 20, "Holy")

# Adding recently created magic to the list ->
magic = [spell_Fire, spell_Thunder, spell_Ice, spell_Cure]

# Instantiate player and first enemy ->
player = Person("Player", 100, 20, 10, 20, magic, 20, 10, 1.4)
enemy = Person("Enemy", 100, 0, 8, 15, None, 15, 10, 1.4)

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
enemy_dodging = False
while running_battlefield:
    msvcrt.getch()
    print(bc.HEADER + bc.BOLD + "======================================== Next turn! ========================================" + bc.ENDC)
    # MP passive restoring ->
    if player.get_mp() < player.get_mp_max():
        player.restore_mana(math.ceil(player.get_mp_max()*0.1))

    # Short info about player and enemy at the start of every turn ->
    print(bc.HEADER + f"===== {enemy.get_name()}: " + bc.ENDC)
    print(enemy.info_short())
    print(bc.HEADER + f"===== {player.get_name()}: " + bc.ENDC)
    print(player.info_short())

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
            player.inspect(enemy)
        elif choice == "Leave":
            print(bc.FAIL + "==================================================" + bc.ENDC)
            print(bc.FAIL + bc.BOLD + "You've left the battlefield!" + bc.ENDC)
            print(bc.FAIL + "==================================================" + bc.ENDC)
            running_player = False
            running_battlefield = False

    # If player have left the battlefield ->
    if not running_battlefield:
        break

    # If enemy has been defeated ->
    if enemy.get_hp() == 0:
        print(bc.OKGREEN + bc.BOLD + "You won!" + bc.ENDC)
        print(bc.FAIL + "================================================================" + bc.ENDC)
        msvcrt.getch()
        print(bc.HEADER + bc.BOLD + "================================================================================" + bc.ENDC)
        # Creating a new enemy ->
        print(bc.FAIL + bc.BOLD + "Next enemy is attacking!" + bc.ENDC)
        enemy = Person("Enemy", enemy.get_hp_max()+5, 0, enemy.get_atk() + 5, enemy.get_df() + 5,
                       None, enemy.get_dodge() + 5, enemy.get_crit_chance()+5, enemy.get_crit_multiplier()+0.1)
        enemy.info()
        print(bc.OKBLUE + "-------------------------")
        print(bc.HEADER + bc.BOLD + "================================================================================" + bc.ENDC)
        print(f"{bc.OKGREEN}You have recovered!{bc.ENDC}")
        player.heal_full()
        player.restore_mana_full()
        continue

    print(bc.FAIL + "==============================" + bc.ENDC)
    # Enemy's turn ->
    if random.randrange(100) in range(20) and not enemy_dodging:
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