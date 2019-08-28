class Atom():
    def __init__(self, _value):
        assert _value is not None
        assert isinstance(_value, str)
        self._value = _value
        self._refcount = 1

    def __repr__(self):
        return self._value

    def isAtom(self):
        return True

    def isNil(self):
        return self._value == "()"

    def _vals(self):
        if self.isNil():
            return []
        raise ValueError('atoms have no embedded values: ' + self._value)


nil = Atom("()")


class Node():
    def __init__(self, _value, _next=None):
        assert _value is not None
        assert _next is None or _next == nil or isinstance(_next, Node)
        self._next = nil if _next is None else _next
        self._value = _value
        self._refcount = 1

    def isAtom(self):
        return False

    def isNil(self):
        return False

    def _vals(self):
        ret = self._next._vals()
        ret.insert(0, self._value)
        return ret

    def __repr__(self):
        if self.isAtom():
            return self._value
        else:
            return "({})".format(" ".join([str(v) for v in self._vals()]))
