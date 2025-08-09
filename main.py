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

# Our battlefield ->
print(bc.FAIL + bc.BOLD + "AN ENEMY ATTACKS!" + bc.ENDC)
running_battlefield = True
while running_battlefield:
    print(bc.HEADER + bc.BOLD + "======================================== Next turn! ========================================" + bc.ENDC)

    # Short info about player and enemy at the start of every turn ->
    print(enemy.info_short())
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
        print(bc.FAIL + "==================================================" + bc.ENDC)

        print(bc.HEADER + bc.BOLD + "================================================================================" + bc.ENDC)
        # Creating a new enemy ->
        print(bc.FAIL + bc.BOLD + "Next enemy is attacking!" + bc.ENDC)
        enemy = Person("Enemy", enemy.get_hp_max()+5, 0, enemy.get_atk() + 5, enemy.get_df() + 5,
                       None, enemy.get_dodge() + 5, enemy.get_crit_chance()+5, enemy.get_crit_multiplier()+0.1)
        enemy.info()
        print(bc.HEADER + bc.BOLD + "================================================================================" + bc.ENDC)
        print(f"{bc.OKGREEN}You have recovered!{bc.ENDC}")
        player.heal_full()
        player.restore_mana_full()
        continue

    # Enemy's turn ->
    print(bc.FAIL + "==============================" + bc.ENDC)
    enemy.perform_attack(player)

    # If player has been defeated ->
    if player.get_hp() == 0:
        print(bc.FAIL + bc.BOLD + "You lost!" + bc.ENDC)
        print(bc.FAIL + "==================================================" + bc.ENDC)
        running_battlefield = False
    else:
        print(bc.FAIL + "==================================================" + bc.ENDC)