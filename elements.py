import numpy as np

class CircuitError(Exception):
    pass


class Wire:

    potential = 0

    def __init__(self):
        self.attached = []

    def connect(self, component):
        assert isinstance(component, DualSided), 'Cannot connect to' \
                                                          '%s' % component
        self.attached.append(component)

class DualSided:
    """Circuit component that can only connect to two wires. Voltage sources,
    current sources, and resistors extend this class."""

    pos, neg = None, None

    def connect_pos(self, wire):
        assert isinstance(wire, Wire), 'Can only connect to wires'
        self.pos = wire

    def connect_neg(self, wire):
        assert isinstance(wire, Wire), 'Can only connect to wires'
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


def is_component(obj):
    return isinstance(obj, Wire) or isinstance(object, DualSided)


class Circuit:
    """Contains circuit elements; Class is used to solve circuit. All
    elements must be contained with the elements iterable passed to
    constructor"""

    ground = None

    def __init__(self, elements):
        check_elements(elements)
        self.elements = elements

    def solve(self):
        """Solves for all wire potentials and element currents"""

        # Set first wire in elements as ground (can be changed later)
        self.ground = ground(elements)

        # Assign variables to each quantity being solved.
        r_lookup, lookup, num = {}, {}, 0
        for element in self.elements:
            if isinstance(element, Wire) and element is not self.ground:
                lookup[num] = element.potential
                r_lookup[element] = num
            elif not isinstance(element, CurrentSource):
                lookup[num] = element.current
                r_lookup[element] = num
            num += 1

        # Set up the linear algebraic equation Ax=b
        A = np.zeros((num + 1, num + 1))
        b = np.zeros(num + 1)
        for row, element in zip(range(num), self.elements):
            if isinstance(element, Wire) and element is not self.ground:
                for two_sided in element.attached:
                    if isinstance(two_sided, CurrentSource):
                        if two_sided.pos is element:
                            b[row] += -1 * element.current
                        else:
                            b[row] += element.current
                    else:
                        if two_sided.pos is element:
                            flow = 1
                        else:
                            flow = -1
                    A[row, r_lookup[two_sided]] = flow
            elif isinstance(element, VoltageSource):
                check_connected(element)
                if element.pos is not self.ground:
                    A[row, r_lookup[element.pos]] = 1
                if element.neg is not self.ground:
                    A[row, r_lookup[element.neg]] = -1
                b[row] = element.voltage
            elif isinstance(element, Resistor):
                check_connected(element)
                if element.pos is not self.ground:
                    A[row, r_lookup[element.pos]] = 1
                if element.neg is not self.ground:
                    A[row, r_lookup[element.neg]] = -1
                A[row, r_lookup[element]] = -1 * element.resistance

        x = np.linalg.solve(A, b)

        # Assign values to all circuit components
        for i in range(num):
            item = lookup[i]
            if isinstance(item, Wire):
                item.potential = x[i]
            elif isinstance(item, DualSided):
                item.current = x[i]


def check_connected(two_sided_element):
    if two_sided_element.pos is None:
        raise CircuitError('Positive terminal of a voltage source '
                           'not connected to wire.')
    if two_sided_element.neg is None:
        raise CircuitError('Negative terminal of a voltage source '
                           'not connected to wire')


def check_elements(elements):
    try:
        for element in elements:
            if not is_component(element):
                raise CircuitError('Elements of a circuit must be wires, '
                                   'voltage sources, or resistors (as of now')
    except TypeError:
        raise CircuitError('Elements of a circuit must be iterable')


def ground(elements):
    for element in elements:
        if isinstance(element, Wire):
            element.potential = 0
            return element
    raise CircuitError('Circuit must contain at least one node (wire)')


















