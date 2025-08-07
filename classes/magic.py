import math


class Spell:
    def __init__(self, name, cost, dmg, type):
        self.name = name
        self.cost = cost
        self.dmg = dmg
        self.dmg_low = math.ceil(dmg - dmg*0.1)
        self.dmg_high = math.ceil(dmg + dmg*0.1)
        self.type = type

    def get_spell_name(self):
        return self.name

    def get_spell_cost(self, spell = 0):
        return self.cost

    def get_spell_damage(self, spell = 0):
        return [self.dmg_low, self.dmg_high, self.dmg]

    def get_spell_type(self):
        return self.type