import numpy as np

from backend.elements import *
from backend.helpers import *


class Circuit:
    """Contains circuit elements; Class is used to solve circuit. All
    elements must be contained with the elements iterable passed to
    constructor"""

    ground = None

    def __init__(self, elements):
        check_elements(elements)
        self.elements = tuple(elements)
        self.been_solved = False

    def solve(self):
        """Solves for all wire potentials and element currents"""

        # Set first wire in elements as ground (can be changed later)
        self.ground = ground(self.elements)

        # Assign variables to each quantity being solved.
        r_lookup, lookup, num = {}, {}, 0
        for element in self.elements:
            if is_wire(element) and element is not self.ground:
                lookup[num] = element
                r_lookup[element] = num
                num += 1
            elif not is_cs(element) and element is not self.ground:
                lookup[num] = element
                r_lookup[element] = num
                num += 1

        # Set up the linear algebraic equation Ax=b
        A = np.zeros((num, num))
        b = np.zeros(num)
        for row, element in lookup.items():
            if is_wire(element) and element is not self.ground:
                for two_sided in element.attached:
                    if is_cs(two_sided):
                        if two_sided.pos is element:
                            b[row] += -1 * two_sided.current
                        else:
                            b[row] += two_sided.current
                    else:
                        if two_sided.pos is element:
                            flow = 1
                        else:
                            flow = -1
                        A[row, r_lookup[two_sided]] = flow
            elif is_vs(element):
                check_connected(element)
                if element.pos is not self.ground:
                    A[row, r_lookup[element.pos]] = 1
                if element.neg is not self.ground:
                    A[row, r_lookup[element.neg]] = -1
                b[row] = element.voltage
            elif is_resistor(element):
                check_connected(element)
                if element.pos is not self.ground:
                    A[row, r_lookup[element.pos]] = 1
                if element.neg is not self.ground:
                    A[row, r_lookup[element.neg]] = -1
                A[row, r_lookup[element]] = -1 * element.resistance

        b = b.reshape((num, 1))
        try:
            x = np.linalg.solve(A, b)
        except np.linalg.LinAlgError:
            raise CircuitError('Insufficient information to solve circuit')

        # Assign values to all circuit components
        for i in range(num):
            item = lookup[i]
            if is_wire(item):
                item.potential = x[i, 0]
            elif isinstance(item, DualSided):
                item.current = x[i, 0]

        # Mark circuit as solved
        self.been_solved = True

    def move_ground(self, wire):
        """Mark another node as ground and shift all other potentials"""

        if not self.been_solved:
            self.solve()
        if not is_wire(wire):
            raise CircuitError('Ground node must be a wire!')
        diff = wire.potential - self.ground.potential
        wire.potential, self.ground = 0, wire

        for element in self.elements:
            if is_wire(element) and element is not self.ground:
                wire.potential += diff

    def ground_min(self):
        """Set circuit's ground to node with lowest potential."""

        def compare(e):
            if is_wire(e):
                return e.potential
            else:
                return float('inf')
        self.move_ground(min(self.elements, compare))


# To do - superposition, dependent sources, capacitors, op-amps, nort/thev

if __name__ == '__main__':
    """Testing"""

    w1, w2 = Wire(), Wire()
    c, r = CurrentSource(0.5), Resistor(1000)
    c.connect_pos(w1)
    w1.connect(r, 'pos')
    r.connect_neg(w2)
    w2.connect(c, 'neg')
    c = Circuit([w1, w2, c, r])
    c.solve()