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

    def value(self):
        return self

    def vals(self):
        if self.isNil():
            return []
        raise ValueError('atoms have no embedded values: ' + self._value)


nil = Atom("()")
t = Atom("t")


class Node():
    def __init__(self, _value, _next=nil):
        assert _value is not None
        assert _next is not None
        assert _next == nil or isinstance(_next, Node)
        self._next = nil if _next is None else _next
        self._value = _value
        self._refcount = 1

    def isAtom(self):
        return False

    def isNil(self):
        return False

    def value(self):
        return self._value

    def vals(self):
        ret = self._next.vals()
        ret.insert(0, self._value)
        return ret

    def __repr__(self):
        if self.isAtom():
            return self._value
        else:
            return "({})".format(" ".join([str(v) for v in self.vals()]))


def eval(e, a=nil):
    assert isinstance(e, Atom) or isinstance(e, Node)
    assert isinstance(a, Atom) or isinstance(a, Node)
    if isinstance(e, Atom):
        return e
    if isinstance(e._value, Atom):
        if str(e._value) == 'quote':
            return e._next.value()
        elif str(e._value) == 'atom':
            return t if eval(e._next.value()).isAtom() else nil
    raise ValueError('NYI')


##############################################################################
foo = Atom('foo')
bar = Atom('bar')
a = Atom('a')
b = Atom('b')
c = Atom('c')
quote = Atom('quote')
x1 = Node(quote, Node(a))
abc = Node(a, Node(b, Node(c)))
x2 = Node(quote, Node(abc))
print(eval(x1))
print(eval(x2))

atom = Atom('atom')
x3 = Node(atom, Node(Node(quote, Node(a))))
x4 = Node(atom, Node(Node(quote, Node(Node(a, Node(b, Node(c)))))))
x5 = Node(atom, Node(Node(quote, Node(nil))))
print(eval(x3))
print(eval(x4))
print(eval(x5))
