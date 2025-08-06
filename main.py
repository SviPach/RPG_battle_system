from classes.game import Person, bcolors
from classes.magic import Spell


spell_Fire = Spell("Fire", 10, 60, "Elemental")
spell_Thunder = Spell("Thunder", 20, 100, "Elemental")
spell_Ice = Spell("Ice", 6, 40, "Elemental")
spell_Cure = Spell("Cure", 5, 80, "Holy")

magic = [spell_Fire, spell_Thunder, spell_Ice, spell_Cure]

player = Person(460, 65, 60, 34, magic)
enemy = Person(1200, 65, 45, 25, magic)

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
    elif choice == "Leave":
        print(bcolors.FAIL + bcolors.BOLD + "You've left the battlefield!" + bcolors.ENDC)
        break

    if enemy.get_hp() == 0:
        print(bcolors.OKGREEN + bcolors.BOLD + "You won!" + bcolors.ENDC)
        break

    player_hp_old = player.get_hp()
    player.take_damage(enemy.generate_damage())
    player_hp_new = player.get_hp()
    print(f"You got hit by enemy: {bcolors.WARNING}-{player_hp_old - player_hp_new}HP.{bcolors.ENDC}")

    if player.get_hp() == 0:
        print(bcolors.FAIL + bcolors.BOLD + "You lost!" + bcolors.ENDC)
        break