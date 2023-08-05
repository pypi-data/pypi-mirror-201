"""
Test variable.py
2022, May 06
"""

import collections.abc

from fonsim.core.variable import Variable
from fonsim.core.terminal import Terminal


def test_hashable():
    # Test whether Variable object is hashable
    var = Variable(key='pressure', orientation='across')
    assert isinstance(var, collections.abc.Hashable)


def test_copy_and_attach():
    """Method copy_and_attach"""
    var_a = Variable(key='pressure', orientation='across')
    term = Terminal('a', [])
    var_b = var_a.copy_and_attach(term)

    assert var_a != var_b
    assert var_a.key == var_b.key
    assert var_a.orientation == var_b.orientation
    assert var_a.terminal is None
    assert var_b.terminal == term
