# General scheme for connectors and constraints.

class ConnectionError(Exception):
    pass

# Base class for components.
class Connector:
    """Base class for all circuit components. Defines mutuality
    and graph-based operations, and establishes core parameters."""
    constraints = []
    attached = []
    fixed = {}

    def set_value(self, attribute, value):
        """Set attribute to value and adjust all connected components
        accordingly. Check validity of all attached components and of self."""

        if attribute in self.fixed:
            raise ConnectionError("Cannot change %s" % attribute)
        if attribute not in self.attributes:
            raise AttributeError("Invalid attribute: %s" % attribute)
        self.attributes[attribute] = value
        for element in self.attached:
            try:
                element.deduce_value()
            except AttributeError:
                raise ConnectionError('Connector class %s is missing '
                                      'deduce_value method' %
                                      str(type(element)))
        for element in self.attached:
            element.check()
        self.check()

    def deduce_value(self):
        """Must be implemented by descendant class"""
        raise ConnectionError()

    def check(self):
        for constraint in self.constraints:
            constraint.check(self)

    def connect(self, connector):
        assert isinstance(connector, Connector) 'Can only connect to ' \
                                                'Connector instances'
        self.attached.append(connector)
        connector.attached.append(self)

class Constraint:

    def __init__(self, fn, type, vis):
        """Initialize a constraint with the function fn, which takes an object
        of type Type as its input."""

        self.func = fn
        self.type = type
        self.vis = vis

    def __str__(self):
        return self.vis

    def check(obj):
        if not isinstance(obj, type) or not fn(obj):
            raise SchemeError('Constraint failed: %s' % str(self))

class Empty:
    pass


empty = Empty() # Instance masks the class.

# Wire

# Resistor

# Voltage source

# Current source

# Open circuit