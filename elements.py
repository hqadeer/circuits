class CircuitError(Exception):
    pass


class Wire:

    potential = 0

    def __init__(self):
        self.attached = []

    def connect(self, component, terminal):
        assert isinstance(component, DualSided), 'Cannot connect to %s' %\
                                                 component
        if terminal == 'pos':
            component.connect_pos(self)
        elif terminal == 'neg':
            component.connect_neg(self)


class DualSided:
    """Circuit component that can only connect to two wires. Voltage sources,
    current sources, and resistors extend this class."""

    pos, neg = None, None

    def connect_pos(self, wire):
        assert isinstance(wire, Wire), 'Can only connect to wires'
        wire.attached.append(self)
        self.pos = wire

    def connect_neg(self, wire):
        assert isinstance(wire, Wire), 'Can only connect to wires'
        wire.attached.append(self)
        self.neg = wire


class VoltageSource(DualSided):

    current = 0

    def __init__(self, voltage):
        self.voltage = voltage


class CurrentSource(DualSided):

    voltage = 0

    def __init__(self, current):
        self.current = current


class Resistor(DualSided):

    current, voltage = 0, 0

    def __init__(self, resistance):
        self.resistance = resistance

if __name__ == '__main__':
    """Testing"""

    v = VoltageSource(10)
    r = Resistor(10)
    w1 = Wire()
    w2 = Wire()
    v.connect_pos(w1)
    r.connect_pos(w1)
    v.connect_neg(w2)
    r.connect_neg(w2)
    e = [v, r, w1, w2]
    c = Circuit(e)
    c.solve()
    print('done')