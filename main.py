from classes.game import Person, bcolors
from classes.magic import Spell


spell_Fire = Spell("Fire", 8, 16, "Elemental")
spell_Thunder = Spell("Thunder", 10, 20, "Elemental")
spell_Ice = Spell("Ice", 5, 10, "Elemental")
spell_Cure = Spell("Cure", 5, 20, "Holy")

magic = [spell_Fire, spell_Thunder, spell_Ice, spell_Cure]

player = Person("Player", 100, 20, 10, 20, magic, 20)
enemy = Person("Enemy", 100, 0, 8, 15, magic, 15)

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while True:
    print("================================================================================")

    print(bcolors.OKBLUE + "=== Enemy: " + bcolors.ENDC)
    enemy.info_short()

    print(bcolors.OKBLUE + "=== Player: " + bcolors.ENDC)
    player.info_short()

    choice = player.choose_action()
    if choice == "Attack":
        player.perform_attack(enemy)
    elif choice == "Magic":
        spell = player.choose_magic()
        player.perform_attack(enemy, spell)
    elif choice == "Dodge":
        player.try_dodge()
    elif choice == "Leave":
        print(bcolors.FAIL + bcolors.BOLD + "You've left the battlefield!" + bcolors.ENDC)
        break

    if enemy.get_hp() == 0:
        print(bcolors.OKGREEN + bcolors.BOLD + "You won!" + bcolors.ENDC)
        break

    player_hp_old = player.get_hp()
    enemy.perform_attack(player)
    # player.take_damage(enemy.generate_damage())
    player_hp_new = player.get_hp()
    # print(f"You got hit by enemy: {bcolors.WARNING}-{player_hp_old - player_hp_new}HP.{bcolors.ENDC}")

    if player.get_hp() == 0:
        print(bcolors.FAIL + bcolors.BOLD + "You lost!" + bcolors.ENDC)
        break