class Equipment:
    def __init__(self, name, slot, prop, prop_type, description):
        self.name = name                    # Name.
        self.slot = slot                    # Slot.
        self.prop = prop                    # Property value (attribute it improves).
        self.prop_type = prop_type          # Property type.
        self.description = description      # Description.

    def get_name(self):
        """ Get equipment's name. """
        return self.name

    def get_slot(self):
        """ Get the slot this equipment belongs to. """
        return self.slot

    def get_prop(self):
        """ Get equipment's property value. """
        return self.prop

    def get_prop_type(self):
        """ Get the type of the equipment's property. """
        return self.prop_type

    def get_description(self):
        """ Get equipment's description. """
        return self.description