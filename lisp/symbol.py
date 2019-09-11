"""
>>> Symbol('A') == Symbol('A')
True

>>> Symbol('A') == Symbol('B')
False

>>> Symbol.NIL
NIL

>>> Symbol.T
T

>>> Symbol('ABC')
ABC

>>> Symbol.isNIL(Symbol("NIL"))
True

>>> Symbol.isNIL(Symbol.T)
False
"""


class Symbol():
    NIL = None
    T = None

    def __init__(self, atom):
        assert isinstance(atom, str)
        self._atom = atom

    def __hash__(self):
        return hash(self._atom)

    def __eq__(self, other):
        return self._atom == other._atom

    def __repr__(self):
        return self._atom

    @staticmethod
    def isNIL(other):
        if isinstance(other, Symbol) and other._atom == "NIL":
            return True
        return False


Symbol.NIL = Symbol('NIL')
Symbol.T = Symbol('T')
