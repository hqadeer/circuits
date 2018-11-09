# General scheme for connectors and constraints.

class ConnectionError(Exception):
    pass

# Base class for components.
class Connector:
    """Base class for all circuit components. Defines mutuality
    and graph-based operations, and establishes core parameters."""

    def __init__(self):
        """Attached -- a list of Connector instances.
        Constraints -- a list of Constraint instances that must all return True
                       for the Connector.
        Attributes --- a dict of parameters"""

        self.attached = []
        self.constraints = []
        self.attributes = {}

    def set_value(self, attribute, value):
        """Set attribute to value and adjust all connected components
        accordingly. Check validity of all attached components and of self."""

        self.attributes[attribute] = value
        for element in self.attached:
            element.deduce_value()
        for element in self.attached:
            element.check()
        self.check()

    def deduce_value(self):
        """Must be implemented by descendant class"""
        pass

    def check(self):
        for constraint in self.constraints:
            if not constraint.passes(self):









# Wire

# Resistor

# Voltage source

# Current source

# Open circuit