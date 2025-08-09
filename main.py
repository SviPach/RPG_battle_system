from classes import *


# Creating some magic spells ->
spell_Fire = Spell("Fire", 8, 16, "Elemental")
spell_Thunder = Spell("Thunder", 10, 20, "Elemental")
spell_Ice = Spell("Ice", 5, 10, "Elemental")
spell_Cure = Spell("Cure", 5, 20, "Holy")

# Adding recently created magic to the list ->
magic = [spell_Fire, spell_Thunder, spell_Ice, spell_Cure]

# Creating player and first enemy ->
player = Person("Player", 100, 20, 10, 20, magic, 20, 10, 1.4)
enemy = Person("Enemy", 100, 0, 8, 15, None, 15, 10, 1.4)

# Creating a health potion ->
health_potion = Potion("Health potion", "health", "Heals a player by 50HP", 50)

# Adding 3 potions to the player's inventory.
for i in range(3):
    player.potion_obtain(health_potion)

# Our battlefield ->
print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)
running_battlefield = True
while running_battlefield:
    print(bcolors.HEADER + bcolors.BOLD + "======================================== Next turn! ========================================" + bcolors.ENDC)

    # Short info about player and enemy at the start of every turn ->
    print(enemy.info_short())
    print(player.info_short())

    # Player's turn ->
    running_player = True
    while running_player:
        choice = player.choose_action()
        if choice == "Attack":
            print(bcolors.FAIL + "========================= Attack time! =========================" + bcolors.ENDC)
            player.perform_attack(enemy)
            running_player = False
        elif choice == "Magic":
            spell = player.choose_magic()
            print(bcolors.FAIL + "========================= Attack time! =========================" + bcolors.ENDC)
            player.perform_attack(enemy, spell)
            running_player = False
        elif choice == "Dodge":
            print(bcolors.FAIL + "========================= Attack time! =========================" + bcolors.ENDC)
            player.try_dodge()
            running_player = False
        elif choice == "Use potion":
            player.potion_choose()
        elif choice == "Inspect":
            player.inspect(enemy)
        elif choice == "Leave":
            print(bcolors.FAIL + "==================================================" + bcolors.ENDC)
            print(bcolors.FAIL + bcolors.BOLD + "You've left the battlefield!" + bcolors.ENDC)
            print(bcolors.FAIL + "==================================================" + bcolors.ENDC)
            running_player = False
            running_battlefield = False

    # If player have left the battlefield ->
    if not running_battlefield:
        break

    # If enemy has been defeated ->
    if enemy.get_hp() == 0:
        print(bcolors.OKGREEN + bcolors.BOLD + "You won!" + bcolors.ENDC)
        print(bcolors.FAIL + "==================================================" + bcolors.ENDC)

        print(bcolors.HEADER + bcolors.BOLD + "================================================================================" + bcolors.ENDC)
        # Creating a new enemy ->
        print(bcolors.FAIL + bcolors.BOLD + "Next enemy is attacking!" + bcolors.ENDC)
        enemy = Person("Enemy", enemy.get_hp_max()+5, 0, enemy.get_atk() + 5, enemy.get_df() + 5,
                       None, enemy.get_dodge() + 5, enemy.get_crit_chance()+5, enemy.get_crit_multiplier()+0.1)
        enemy.info()
        print(bcolors.HEADER + bcolors.BOLD + "================================================================================" + bcolors.ENDC)
        print(f"{bcolors.OKGREEN}You have recovered!{bcolors.ENDC}")
        player.heal_full()
        player.restore_mana_full()
        continue

    # Enemy's turn ->
    print(bcolors.FAIL + "==============================" + bcolors.ENDC)
    enemy.perform_attack(player)

    # If player has been defeated ->
    if player.get_hp() == 0:
        print(bcolors.FAIL + bcolors.BOLD + "You lost!" + bcolors.ENDC)
        print(bcolors.FAIL + "==================================================" + bcolors.ENDC)
        running_battlefield = False
    else:
        print(bcolors.FAIL + "==================================================" + bcolors.ENDC)