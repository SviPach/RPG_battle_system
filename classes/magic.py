import math


class Spell:
    def __init__(self, name, cost, dmg, type):
        self.name = name                            # Name.
        self.cost = cost                            # MP cost.
        self.dmg = dmg                              # If used: amount of hp this spell restores. If not: value to calculate damage.
        self.dmg_low = math.ceil(dmg - dmg*0.1)     # Weakest damage.
        self.dmg_high = math.ceil(dmg + dmg*0.1)    # Strongest damage.
        self.type = type                            # Type of the spell.

    def get_spell_name(self):
        """ Get the spell's name. """
        return self.name

    def get_spell_cost(self, spell = 0):
        """ Get the spell's cost. """
        return self.cost

    def get_spell_damage(self, spell = 0):
        """ Calculate the spell's damage. """
        return [self.dmg_low, self.dmg_high, self.dmg]

    def get_spell_type(self):
        """ Get the spell's type. '"""
        return self.type