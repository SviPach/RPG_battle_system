class Potion:
    def __init__(self, name, type, description, prop):
        self.name = name                    # Name.
        self.type = type                    # Type of potion.
        self.description = description      # Description of potion.
        self.prop = prop                    # Property value.

    def get_name(self):
        """ Get the name of the potion. """
        return self.name

    def get_type(self):
        """ Get the type of the potion. """
        return self.type

    def get_description(self):
        """ Get the description of the potion. """
        return self.description

    def get_prop(self):
        """ Get the property value of the potion. """
        return self.prop