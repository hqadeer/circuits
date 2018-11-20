from solver.elements import *


def is_component(obj):
    return isinstance(obj, Wire) or isinstance(obj, DualSided)


def check_connected(two_sided_element):
    """Ensures that a two-sided element is connected to a wire on both ends."""

    if two_sided_element.pos is None:
        raise CircuitError('Positive terminal of a voltage source '
                           'not connected to wire.')
    if two_sided_element.neg is None:
        raise CircuitError('Negative terminal of a voltage source '
                           'not connected to wire')


def check_elements(elements):
    """Ensures that elements is an iterable of valid circuit components"""

    try:
        for element in elements:
            if not is_component(element):
                raise CircuitError('Elements of a circuit must be wires, '
                                   'voltage sources, or resistors (as of now)')
    except TypeError:
        raise CircuitError('Elements of a circuit must be iterable')


def ground(elements):
    """Identifies a ground wire in elements and sets its potential to zero.
    If no ground found, raises a CircuitError"""

    for element in elements:
        if isinstance(element, Wire):
            element.potential = 0
            return element
    raise CircuitError('Circuit must contain at least one node (wire)')


def is_wire(element):
    return isinstance(element, Wire)


def is_vs(element):
    return isinstance(element, VoltageSource)


def is_cs(element):
    return isinstance(element, CurrentSource)


def is_resistor(element):
    return isinstance(element, Resistor)