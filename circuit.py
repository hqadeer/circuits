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
        self.ground = ground(self.elements)

        # Assign variables to each quantity being solved.
        r_lookup, lookup, num = {}, {}, 0
        for element in self.elements:
            if isinstance(element, Wire) and element is not self.ground:
                lookup[num] = element
                r_lookup[element] = num
                num += 1
            elif not isinstance(element, CurrentSource) and element is not \
                    self.ground:
                lookup[num] = element
                r_lookup[element] = num
                num += 1

        # Set up the linear algebraic equation Ax=b
        A = np.zeros((num, num))
        b = np.zeros(num)
        for row, element in lookup.items():
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

        b = b.reshape((num, 1))
        x = np.linalg.solve(A, b)

        # Assign values to all circuit components
        for i in range(num):
            item = lookup[i]
            if isinstance(item, Wire):
                item.potential = x[i, 0]
            elif isinstance(item, DualSided):
                item.current = x[i, 0]