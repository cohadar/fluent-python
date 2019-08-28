"""
Every LISP data object has 3 properties:
* identity - memory address of Atom or Node
* type - Atom or Node
* value - for Atom str(self), for Node id

# atoms are symbols
>>> Atom('foo')
foo

# empty list is also an atom
>>> nil; \
    nil.isAtom();
()
True

# list with one element
>>> Node(foo)
(foo)

# list with two elements
>>> Node(foo, Node(bar))
(foo bar)

# nested lists
>>> Node(a,           \
         Node(b,       \
         Node(Node(c), \
         Node(d))))
(a b (c) d)

# quote operator
>>> x = li(quote, a); print(x); eval(x)
(quote a)
a

>>> x = li(quote, li(a, b, c)); print(x); eval(x)
(quote (a b c))
(a b c)

# atom operator
>>> x = li(atom, qu(a)); print(x); eval(x)
(atom (quote a))
t

>>> x = li(atom, qu(li(a, b, c))); print(x); eval(x)
(atom (quote (a b c)))
()

>>> x = li(atom, qu(nil)); print(x); eval(x)
(atom (quote ()))
t

>>> x = li(atom, li(atom, qu(a))); print(x); eval(x)
(atom (atom (quote a)))
t

>>> x = li(atom, qu(li(atom, qu(a)))); print(x); eval(x)
(atom (quote (atom (quote a))))
()

# eq operator
>>> x = li(eq, qu(a), qu(a)); print(x); eval(x)
(eq (quote a) (quote a))
t

>>> x = li(eq, qu(a), qu(b)); print(x); eval(x)
(eq (quote a) (quote b))
()

>>> x = li(eq, qu(nil), qu(nil)); print(x); eval(x)
(eq (quote ()) (quote ()))
t

# car operator
>>> x = li(car, qu(li(a, b, c))); print(x); eval(x)
(car (quote (a b c)))
a
"""


# implement Atom "interning" optimization?
class Atom():
    def __init__(self, symbol):
        assert symbol is not None
        assert isinstance(symbol, str)
        self.__symbol = symbol
        self.__refcount = 1

    def isAtom(self):
        return True

    def isNil(self):
        return self.__symbol == "()"

    def _vals(self):
        if self.isNil():
            return []
        raise ValueError('atoms have no embedded values: ' + self.__symbol)

    def __repr__(self):
        return self.__symbol

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))


nil = Atom("()")  # enforce singleton?


class Node():
    def __init__(self, head, tail=nil):
        assert head is not None
        assert tail is not None
        assert tail == nil or isinstance(tail, Node)
        self.__tail = nil if tail is None else tail
        self.__head = head
        self.__refcount = 1

    def isAtom(self):
        return False

    def isNil(self):
        return False

    def head(self):
        return self.__head

    def tail(self):
        return self.__tail

    def _vals(self):
        ret = self.__tail._vals()
        ret.insert(0, self.__head)
        return ret

    def __repr__(self):
        if self.isAtom():
            return self.__head
        else:
            return "({})".format(" ".join([str(v) for v in self._vals()]))


def li(*elements):
    """
    >>> li(a, b, li(c), d)
    (a b (c) d)
    """
    if not elements:
        return nil
    return Node(elements[0], li(*elements[1:]))


def qu(element):
    """
    >>> qu(a)
    (quote a)
    """
    return Node(quote, Node(element))


def eval(e, a=nil):
    assert isinstance(e, Atom) or isinstance(e, Node)
    assert isinstance(a, Atom) or isinstance(a, Node)
    if isinstance(e, Atom):
        return e
    if isinstance(e.head(), Atom):
        if str(e.head()) == 'quote':
            # what is quote tail has != 1 element?
            # note quote does not do argument eval!
            return e.tail().head()
        elif str(e.head()) == 'atom':
            # what if atom tail has != 1 element?
            return t if eval(e.tail().head()).isAtom() else nil
        elif str(e.head()) == 'eq':
            # what if eq tail has != 2 elements?
            el2 = eval(e.tail().head())
            el3 = eval(e.tail().tail().head())
            return t if el2 == el3 else nil
        elif str(e.head()) == 'car':
            # what if car tail has != 1 element?
            # what if car tail head is not a list?
            el2 = eval(e.tail().head())
            return el2.head()
        else:
            raise ValueError('NYI: {}'.format(e.head()))
    raise ValueError('NYI')


##############################################################################
t = Atom("t")
foo = Atom('foo')
bar = Atom('bar')
a = Atom('a')
b = Atom('b')
c = Atom('c')
d = Atom('d')
quote = Atom('quote')
atom = Atom('atom')
eq = Atom('eq')
car = Atom('car')
