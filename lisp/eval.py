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
>>> prepr(Node('foo'))
(foo)

# list with two elements
>>> prepr(Node('foo', Node('bar')))
(foo bar)

# nested lists
>>> x = Node(a,       \
        Node(b,       \
        Node(Node(c), \
        Node(d)))); prepr(x)
(a b (c) d)

# quote operator
>>> x = li(quote, a); prepr(x); peval(x)
(quote a)
a

>>> x = li(quote, li(a, b, c)); prepr(x); peval(x)
(quote (a b c))
(a b c)

# atom operator
>>> x = li(atom, qu(a)); prepr(x); peval(x)
(atom (quote a))
t

>>> x = li(atom, qu(li(a, b, c))); prepr(x); peval(x)
(atom (quote (a b c)))
()

>>> x = li(atom, qu(nil)); prepr(x); peval(x)
(atom (quote ()))
t

>>> x = li(atom, li(atom, qu(a))); prepr(x); peval(x)
(atom (atom (quote a)))
t

>>> x = li(atom, qu(li(atom, qu(a)))); prepr(x); peval(x)
(atom (quote (atom (quote a))))
()

# eq operator
>>> x = li(eq, qu(a), qu(a)); prepr(x); peval(x)
(eq (quote a) (quote a))
t

>>> x = li(eq, qu(a), qu(b)); prepr(x); peval(x)
(eq (quote a) (quote b))
()

>>> x = li(eq, qu(nil), qu(nil)); prepr(x); peval(x)
(eq (quote ()) (quote ()))
t

# car operator
>>> x = li(car, qu(li(a, b, c))); prepr(x); peval(x)
(car (quote (a b c)))
a

# cdr operator
>>> x = li(cdr, qu(li(a, b, c))); prepr(x); peval(x)
(cdr (quote (a b c)))
(b c)

# cons operator
>>> x = li(cons, qu(a), qu(li(b, c))); prepr(x); peval(x)
(cons (quote a) (quote (b c)))
(a b c)

>>> x = li(cons, qu(a), li(cons, qu(b), li(cons, qu(c), qu(nil)))); prepr(x); peval(x)
(cons (quote a) (cons (quote b) (cons (quote c) (quote ()))))
(a b c)

>>> x = li(car, li(cons, qu(a), qu(li(b, c)))); prepr(x); peval(x)
(car (cons (quote a) (quote (b c))))
a

>>> x = li(cdr, li(cons, qu(a), qu(li(b, c)))); prepr(x); peval(x)
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
        ret = _elist(_tail(e))
        ret.insert(0, _head(e))
        return ret


def _repr(e):
    if isinstance(e, str):
        return e
    else:
        return "({})".format(" ".join([_repr(v) for v in _elist(e)]))


nil = "()"  # enforce singleton?


def _head(e):
    assert isinstance(e, Node)
    return e._head


def _tail(e):
    assert isinstance(e, Node)
    return e._tail


class Node():
    def __init__(self, head, tail=nil):
        assert head is not None
        assert tail is not None
        assert tail == nil or isinstance(tail, Node)
        self._tail = nil if tail is None else tail
        self._head = head


def li(*elements):
    """
    >>> prepr(li(a, b, li(c), d))
    (a b (c) d)
    """
    if not elements:
        return nil
    return Node(elements[0], li(*elements[1:]))


def qu(element):
    """
    >>> prepr(qu(a))
    (quote a)
    """
    return Node(quote, Node(element))


def eval(e, a=nil):
    assert isinstance(e, str) or isinstance(e, Node)
    assert isinstance(a, str) or isinstance(a, Node)
    if isinstance(e, str):
        return e
    if isinstance(_head(e), str):
        if str(_head(e)) == 'quote':
            # what is quote has wrong number of args?
            # note quote does not do argument eval!
            return _head(_tail(e))
        elif str(_head(e)) == 'atom':
            # what is atom has wrong number of args?
            el2 = eval(_head(_tail(e)))
            return t if _isAtom(el2) else nil
        elif str(_head(e)) == 'eq':
            # what if eq has wrong number of args?
            el2 = eval(_head(_tail(e)))
            el3 = eval(_head(_tail(_tail(e))))
            return t if el2 == el3 else nil
        elif str(_head(e)) == 'car':
            # what if car has wrong number of args?
            el2 = eval(_head(_tail(e)))
            # what if el2 is not a list?
            return _head(el2)
        elif str(_head(e)) == 'cdr':
            # what if cdr has wrong number of args?
            el2 = eval(_head(_tail(e)))
            # what if el2 is not a list?
            return _tail(el2)
        elif str(_head(e)) == 'cons':
            # what if cons has wrong number of args?
            el2 = eval(_head(_tail(e)))
            el3 = eval(_head(_tail(_tail(e))))
            return Node(el2, el3)
        else:
            raise ValueError('NYI: {}'.format(_head(e)))
    raise ValueError('NYI')


def prepr(e):
    print(_repr(e))


def peval(e):
    prepr(eval(e))


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
