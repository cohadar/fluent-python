"""
Every LISP data object has 3 properties:
* identity - memory address of str or Node
* type - str or Node
* value - for str self, for Node id

# atoms are symbols
>>> peval('foo')
foo

# empty list is also an atom
>>> peval(nil); \
    _isAtom(nil);
()
True

# list with one element
>>> Node('foo')
(foo)

# list with two elements
>>> Node('foo', Node('bar'))
(foo bar)

# nested lists
>>> Node(a,           \
         Node(b,       \
         Node(Node(c), \
         Node(d))))
(a b (c) d)

# quote operator
>>> x = li(quote, a); print(x); peval(x)
(quote a)
a

>>> x = li(quote, li(a, b, c)); print(x); peval(x)
(quote (a b c))
(a b c)

# atom operator
>>> x = li(atom, qu(a)); print(x); peval(x)
(atom (quote a))
t

>>> x = li(atom, qu(li(a, b, c))); print(x); peval(x)
(atom (quote (a b c)))
()

>>> x = li(atom, qu(nil)); print(x); peval(x)
(atom (quote ()))
t

>>> x = li(atom, li(atom, qu(a))); print(x); peval(x)
(atom (atom (quote a)))
t

>>> x = li(atom, qu(li(atom, qu(a)))); print(x); peval(x)
(atom (quote (atom (quote a))))
()

# eq operator
>>> x = li(eq, qu(a), qu(a)); print(x); peval(x)
(eq (quote a) (quote a))
t

>>> x = li(eq, qu(a), qu(b)); print(x); peval(x)
(eq (quote a) (quote b))
()

>>> x = li(eq, qu(nil), qu(nil)); print(x); peval(x)
(eq (quote ()) (quote ()))
t

# car operator
>>> x = li(car, qu(li(a, b, c))); print(x); peval(x)
(car (quote (a b c)))
a

# cdr operator
>>> x = li(cdr, qu(li(a, b, c))); print(x); peval(x)
(cdr (quote (a b c)))
(b c)

# cons operator
>>> x = li(cons, qu(a), qu(li(b, c))); print(x); peval(x)
(cons (quote a) (quote (b c)))
(a b c)

>>> x = li(cons, qu(a), li(cons, qu(b), li(cons, qu(c), qu(nil)))); print(x); peval(x)
(cons (quote a) (cons (quote b) (cons (quote c) (quote ()))))
(a b c)

>>> x = li(car, li(cons, qu(a), qu(li(b, c)))); print(x); peval(x)
(car (cons (quote a) (quote (b c))))
a

>>> x = li(cdr, li(cons, qu(a), qu(li(b, c)))); print(x); peval(x)
(cdr (cons (quote a) (quote (b c))))
(b c)
"""


def _isAtom(e):
    return isinstance(e, str)


def _isNil(e):
    return str(e) == "()"


def _elist(e):
    if isinstance(e, str):
        if _isNil(e):
            return []
        raise ValueError('atoms have no embedded values: ' + e)
    else:
        ret = _elist(e.tail())
        ret.insert(0, e.head())
        return ret


def _repr(e):
    if isinstance(e, str):
        return e
    else:
        return "({})".format(" ".join([str(v) for v in _elist(e)]))


nil = "()"  # enforce singleton?


class Node():
    def __init__(self, head, tail=nil):
        assert head is not None
        assert tail is not None
        assert tail == nil or isinstance(tail, Node)
        self.__tail = nil if tail is None else tail
        self.__head = head
        self.__refcount = 1

    def head(self):
        return self.__head

    def tail(self):
        return self.__tail

    def __repr__(self):
        return _repr(self)


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
    assert isinstance(e, str) or isinstance(e, Node)
    assert isinstance(a, str) or isinstance(a, Node)
    if isinstance(e, str):
        return e
    if isinstance(e.head(), str):
        if str(e.head()) == 'quote':
            # what is quote has wrong number of args?
            # note quote does not do argument eval!
            return e.tail().head()
        elif str(e.head()) == 'atom':
            # what is atom has wrong number of args?
            el2 = eval(e.tail().head())
            return t if _isAtom(el2) else nil
        elif str(e.head()) == 'eq':
            # what if eq has wrong number of args?
            el2 = eval(e.tail().head())
            el3 = eval(e.tail().tail().head())
            return t if el2 == el3 else nil
        elif str(e.head()) == 'car':
            # what if car has wrong number of args?
            el2 = eval(e.tail().head())
            # what if el2 is not a list?
            return el2.head()
        elif str(e.head()) == 'cdr':
            # what if cdr has wrong number of args?
            el2 = eval(e.tail().head())
            # what if el2 is not a list?
            return el2.tail()
        elif str(e.head()) == 'cons':
            # what if cons has wrong number of args?
            el2 = eval(e.tail().head())
            el3 = eval(e.tail().tail().head())
            return Node(el2, el3)
        else:
            raise ValueError('NYI: {}'.format(e.head()))
    raise ValueError('NYI')


def peval(e):
    print(eval(e))


##############################################################################
t = "t"
foo = 'foo'
bar = 'bar'
a = 'a'
b = 'b'
c = 'c'
d = 'd'
quote = 'quote'
atom = 'atom'
eq = 'eq'
car = 'car'
cdr = 'cdr'
cons = 'cons'
