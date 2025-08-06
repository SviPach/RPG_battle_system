from classes.game import Person, bcolors

magic = [{"name": "Fire", "cost": 10, "dmg": 60},
         {"name": "Thunder", "cost": 20, "dmg": 100},
         {"name": "Ice", "cost": 6, "dmg": 40}]

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
        dmg = player.generate_damage()
        enemy_hp_old = enemy.hp
        enemy.take_damage(dmg)
        enemy_hp_new = enemy.hp
        print(f"You are attacking for {dmg}HP with {bcolors.WARNING}Physical attack{bcolors.ENDC}.")
        print(f"Enemy took damage: {bcolors.WARNING}-{enemy_hp_old - enemy_hp_new}HP.{bcolors.ENDC}")
    elif choice == "Magic":
        spell = player.choose_magic()
        spell_cost = player.get_spell_cost(spell)
        player.reduce_mp(spell_cost)
        dmg = player.generate_damage(spell)
        enemy_hp_old = enemy.hp
        enemy.take_damage(dmg)
        enemy_hp_new = enemy.hp
        if spell == 0: spell = "Physical attack"
        print(f"You are attacking for {dmg}HP with {bcolors.WARNING}{spell}{bcolors.ENDC}.")
        print(f"Enemy took damage: {bcolors.WARNING}-{enemy_hp_old - enemy_hp_new}HP.{bcolors.ENDC}")
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