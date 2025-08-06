class Spell:
    def __init__(self, name, cost, dmg, type):
        self.name = name
        self.cost = cost
        self.dmg = dmg
        self.type = type

    def get_spell_name(self):
        return self.name

    def get_spell_cost(self, spell = 0):
        return self.cost

    def get_spell_damage(self, spell = 0):
        return self.dmg

    def get_spell_type(self):
        return self.type