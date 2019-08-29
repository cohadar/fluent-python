"""
Every LISP data object has 3 properties:
* identity - memory address of str or list
* type - str or list
* value - for str self, for list id

# atoms are symbols
>>> peval('foo')
foo

# empty list is also an atom
>>> peval([]); \
    _isAtom([]);
()
True

# list with one element
>>> prepr(['foo'])
(foo)

# list with two elements
>>> prepr([foo, bar])
(foo bar)

# nested lists
>>> prepr([a, [b, c], d])
(a (b c) d)

# quote operator
>>> x = [quote, a]; prepr(x); peval(x)
(quote a)
a

>>> x = [quote, [a, b, c]]; prepr(x); peval(x)
(quote (a b c))
(a b c)

# atom operator
>>> x = [atom, [quote, a]]; prepr(x); peval(x)
(atom (quote a))
t

>>> x = [atom, qu([a, b, c])]; prepr(x); peval(x)
(atom (quote (a b c)))
()

>>> x = [atom, qu([])]; prepr(x); peval(x)
(atom (quote ()))
t

>>> x = [atom, [atom, qu(a)]]; prepr(x); peval(x)
(atom (atom (quote a)))
t

>>> x = [atom, qu([atom, qu(a)])]; prepr(x); peval(x)
(atom (quote (atom (quote a))))
()

# eq operator
>>> x = [eq, qu(a), qu(a)]; prepr(x); peval(x)
(eq (quote a) (quote a))
t

>>> x = [eq, qu(a), qu(b)]; prepr(x); peval(x)
(eq (quote a) (quote b))
()

>>> x = [eq, qu([]), qu([])]; prepr(x); peval(x)
(eq (quote ()) (quote ()))
t

# car operator
>>> x = [car, qu([a, b, c])]; prepr(x); peval(x)
(car (quote (a b c)))
a

# cdr operator
>>> x = [cdr, qu([a, b, c])]; prepr(x); peval(x)
(cdr (quote (a b c)))
(b c)

# cons operator
>>> x = [cons, qu(a), qu([b, c])]; prepr(x); peval(x)
(cons (quote a) (quote (b c)))
(a b c)

>>> x = [cons, qu(a), [cons, qu(b), [cons, qu(c), qu([])]]]; prepr(x); peval(x)
(cons (quote a) (cons (quote b) (cons (quote c) (quote ()))))
(a b c)

>>> x = [car, [cons, qu(a), qu([b, c])]]; prepr(x); peval(x)
(car (cons (quote a) (quote (b c))))
a

>>> x = [cdr, [cons, qu(a), qu([b, c])]]; prepr(x); peval(x)
(cdr (cons (quote a) (quote (b c))))
(b c)
"""


def _isAtom(e):
    assert e is not None
    return isinstance(e, str) or e == []


def _isNil(e):
    assert e is not None
    return e == []


def _repr(e):
    assert e is not None
    if isinstance(e, str):
        return e
    else:
        return "({})".format(" ".join([_repr(v) for v in e]))


def qu(e):
    """
    >>> prepr(qu(a))
    (quote a)
    """
    return [quote, e]


def eval(e, a=[]):
    if e == []:
        return e
    assert isinstance(e, str) or isinstance(e, list)
    assert isinstance(a, str) or isinstance(a, list)
    if isinstance(e, str):
        return e
    if isinstance(e[0], str):
        if str(e[0]) == 'quote':
            # what is quote has wrong number of args?
            # note quote does not do argument eval!
            return e[1]
        elif str(e[0]) == 'atom':
            # what is atom has wrong number of args?
            el2 = eval(e[1])
            return t if _isAtom(el2) else []
        elif str(e[0]) == 'eq':
            # what if eq has wrong number of args?
            el2 = eval(e[1])
            el3 = eval(e[2])
            return t if el2 == el3 else []
        elif str(e[0]) == 'car':
            # what if car has wrong number of args?
            el2 = eval(e[1])
            # what if el2 is not a list?
            return el2[0]
        elif str(e[0]) == 'cdr':
            # what if cdr has wrong number of args?
            el2 = eval(e[1])
            # what if el2 is not a list?
            return el2[1:]
        elif str(e[0]) == 'cons':
            # what if cons has wrong number of args?
            el2 = eval(e[1])
            el3 = eval(e[2])
            ret = [el2]
            ret.extend(el3)
            return ret
        else:
            raise ValueError('NYI: {}'.format(e[0]))
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
