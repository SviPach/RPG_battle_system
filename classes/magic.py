import math


class Spell:
    def __init__(self, name, cost, dmg, prop_optional, type, description):
        # Name
        self.name = name
        # Description
        self.description = description
        # MP cost
        self.cost = cost
        # Type of the spell
        self.type = type

        # Attack damage
        # -------------
        # Base damage. If used: amount of hp this spell restores
        self.dmg = dmg
        # Lowest damage
        self.dmg_low = math.ceil(dmg - dmg * 0.1)
        # Highest damage
        self.dmg_high = math.ceil(dmg + dmg * 0.1)

        # Optional property
        self.prop_optional = prop_optional

    def get_name(self):
        """ Get the spell's name. """
        return self.name

    def get_cost(self):
        """ Get the spell's cost. """
        return self.cost

    def get_damage(self):
        """ Calculate the spell's damage. """
        return [self.dmg_low, self.dmg_high, self.dmg]

    def get_type(self):
        """ Get the spell's type. '"""
        return self.type

    def get_description(self):
        """ Get the spell's description. '"""
        return self.description

    def get_prop_optional(self):
        """ Get the spell's optional property. '"""
        return self.prop_optional
