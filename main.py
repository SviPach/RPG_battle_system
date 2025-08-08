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
enemy = Person("Enemy", 100, 0, 8, 15, magic, 15, 10, 1.4)

# Creating a health potion ->
health_potion = Potion("Health potion", "health", "Heals a player by 50HP", 50)

# Adding 3 potions to the player's inventory.
for i in range(3):
    player.potion_obtain(health_potion)

# Our battlefield ->
print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)
running_battlefield = True
while running_battlefield:
    print(bcolors.HEADER + bcolors.BOLD + "================================================================================" + bcolors.ENDC)

    # Short info about player and enemy at the start of every turn ->
    print(bcolors.OKBLUE + "=== Enemy: " + bcolors.ENDC)
    enemy.info_short()
    print(bcolors.OKBLUE + "=== Player: " + bcolors.ENDC)
    player.info_short()

    # Player's turn ->
    print(bcolors.FAIL + "==================================================" + bcolors.ENDC)
    running_player = True
    while running_player:
        choice = player.choose_action()
        if choice == "Attack":
            player.perform_attack(enemy)
            running_player = False
        elif choice == "Magic":
            spell = player.choose_magic()
            player.perform_attack(enemy, spell)
            running_player = False
        elif choice == "Dodge":
            player.try_dodge()
            running_player = False
        elif choice == "Use potion":
            player.potion_choose()
        elif choice == "Leave":
            print(bcolors.FAIL + bcolors.BOLD + "You've left the battlefield!" + bcolors.ENDC)
            print(bcolors.FAIL + "==================================================" + bcolors.ENDC)
            running_battlefield = False

    # If enemy has been defeated ->
    if enemy.get_hp() == 0:
        print(bcolors.OKGREEN + bcolors.BOLD + "You won!" + bcolors.ENDC)
        print(bcolors.FAIL + "==================================================" + bcolors.ENDC)
        running_battlefield = False

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