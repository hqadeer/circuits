import numpy as np

from backend.helpers import *


class Circuit:
    """Contains circuit elements; Class is used to solve circuit. All
    elements must be contained with the elements iterable passed to
    constructor"""

    def __init__(self, elements):
        check_elements(elements)
        self.elements = tuple(elements)
        self.ground = ground(self.elements)
        self.been_solved = False

    def solve(self):
        """Solves for all wire potentials and element currents"""

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
        diff, wire.potential = 0 - wire.potential, 0
        self.ground = wire

        for element in self.elements:
            if is_wire(element) and element is not self.ground:
                element.potential += diff

    def ground_min(self):
        """Set circuit's ground to node with lowest potential."""

        def compare(e):
            if is_wire(e):
                return e.potential
            else:
                return float('inf')
        self.move_ground(min(self.elements, key=compare))

    def align_resistors(self):
        """Swap resistor terminals to make all associated currents positive."""

        if not self.been_solved:
            self.solve()
        for element in self.elements:
            if is_resistor(element) and element.current < 0:
                element.pos, element.neg = element.neg, element.pos
                element.current = -1 * element.current


# To do - solving: dependent sources, capacitors, op-amps
#         steps: capacitor/resistor equivalences, super-position
#         other: norton/thevenin, symbolic
#         web app

if __name__ == '__main__':
    """Testing"""
    ground_wire = Wire()
    v1, v2, v3 = VoltageSource(8), VoltageSource(8), VoltageSource(8)
    r1, r2, r3, r4, r5, r6 = Resistor(200), Resistor(200), Resistor(200), \
                             Resistor(200), Resistor(100), Resistor(100)
    ground_wire.connect(v1, 'neg')
    ground_wire.connect(v2, 'neg')
    ground_wire.connect(v3, 'neg')
    ground_wire.connect(r1, 'neg')
    v1_r, v2_r, v3_r = Wire(), Wire(), Wire()
    v1_r.connect(v1, 'pos')
    v1_r.connect(r2, 'neg')
    v2_r.connect(v2, 'pos')
    v2_r.connect(r3, 'neg')
    v3_r.connect(v3, 'pos')
    v3_r.connect(r4, 'neg')
    top_l, top_mid, top_r = Wire(), Wire(), Wire()
    top_l.connect(r1, 'pos')
    top_l.connect(r2, 'pos')
    top_l.connect(r5, 'pos')
    top_mid.connect(r5, 'neg')
    top_mid.connect(r3, 'pos')
    top_mid.connect(r6, 'pos')
    top_r.connect(r6, 'neg')
    top_r.connect(r4, 'pos')
    e = [r1, r2, r3, r4, r5, r6, v1, v2, v3, ground_wire, v1_r, v2_r, v3_r,
         top_l, top_mid, top_r]
    c = Circuit(e)
    c.solve()
    c.ground_min()