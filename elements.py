class Wire:

    potential = 0

    def __init__(self):
        self.attached = []

    def connect(self, component):
        assert isinstance(component, DualSidedComponent), 'Cannot connect to' \
                                                          '%s' % component
        self.attached.append(component)

class DualSidedComponent:
    """Circuit component that can only connect to two wires. Voltage sources,
    current sources, and resistors extend this class."""

    pos, neg = None, None

    def connect_pos(self, wire):
        assert isinstance(wire, Wire), 'Can only connect to wires'
        self.pos = wire

    def connect_neg(self, wire):
        assert isinstance(wire, Wire), 'Can only connect to wires'
        self.neg = wire


class VoltageSource(DualSidedComponent):

    current = 0

    def __init__(self, voltage):
        self.voltage = voltage


class CurrentSource(DualSidedComponent):

    voltage = 0

    def __init__(self, current):
        self.current = current


class Resistor(DualSidedComponent):

    current, voltage = 0, 0

    def __init__(self, resistance):
        self.resistance = resistance


def is_component(obj):
    return isinstance(obj, Wire) or isinstance(object, DualSidedComponent)





