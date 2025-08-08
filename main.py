from classes import Person, bcolors
from classes import Spell


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

# Our battlefield ->
print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)
while True:
    print(bcolors.HEADER + bcolors.BOLD + "================================================================================" + bcolors.ENDC)

    # Short info about player and enemy at the start of every turn ->
    print(bcolors.OKBLUE + "=== Enemy: " + bcolors.ENDC)
    enemy.info_short()
    print(bcolors.OKBLUE + "=== Player: " + bcolors.ENDC)
    player.info_short()

    # Player's turn ->
    choice = player.choose_action()
    print(bcolors.FAIL + "==================================================" + bcolors.ENDC)
    if choice == "Attack":
        player.perform_attack(enemy)
    elif choice == "Magic":
        spell = player.choose_magic()
        player.perform_attack(enemy, spell)
    elif choice == "Dodge":
        player.try_dodge()
    elif choice == "Leave":
        print(bcolors.FAIL + bcolors.BOLD + "You've left the battlefield!" + bcolors.ENDC)
        print(bcolors.FAIL + "==================================================" + bcolors.ENDC)
        break

    # If enemy has been defeated ->
    if enemy.get_hp() == 0:
        print(bcolors.OKGREEN + bcolors.BOLD + "You won!" + bcolors.ENDC)
        print(bcolors.FAIL + "==================================================" + bcolors.ENDC)
        break

    # Enemy's turn ->
    print(bcolors.FAIL + "==============================" + bcolors.ENDC)
    enemy.perform_attack(player)

    # If player has been defeated ->
    if player.get_hp() == 0:
        print(bcolors.FAIL + bcolors.BOLD + "You lost!" + bcolors.ENDC)
        print(bcolors.FAIL + "==================================================" + bcolors.ENDC)
        break
    else:
        print(bcolors.FAIL + "==================================================" + bcolors.ENDC)