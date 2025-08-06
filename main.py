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
    info_enemy = f""
    if enemy.health_critical():
        info_enemy += f"{bcolors.FAIL}{enemy.get_hp()}{bcolors.ENDC}/{enemy.get_hp_max()}HP, "
    else:
        info_enemy += f"{enemy.get_hp()}/{enemy.get_hp_max()}HP, "

    if enemy.mana_critical():
        info_enemy += f"{bcolors.FAIL}{enemy.get_mp()}{bcolors.ENDC}/{enemy.get_mp_max()}MP"
    else:
        info_enemy += f"{enemy.get_mp()}/{enemy.get_mp_max()}MP"
    print(info_enemy)


    print(bcolors.OKBLUE + "=== Player: " + bcolors.ENDC)

    info_player = f""
    if player.health_critical():
        info_player += f"{bcolors.FAIL}{player.get_hp()}{bcolors.ENDC}/{player.get_hp_max()}HP, "
    else:
        info_player += f"{player.get_hp()}/{player.get_hp_max()}HP, "

    if player.mana_critical():
        info_player += f"{bcolors.FAIL}{player.get_mp()}{bcolors.ENDC}/{player.get_mp_max()}MP"
    else:
        info_player += f"{player.get_mp()}/{player.get_mp_max()}MP"
    print(info_player)


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
        dmg = player.generate_spell_damage(spell)
        enemy_hp_old = enemy.hp
        enemy.take_damage(dmg)
        enemy_hp_new = enemy.hp
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
