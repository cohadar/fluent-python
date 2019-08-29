"""
Every LISP data object has 3 properties:
* identity - memory address of str or list
* type - str or list
* value - for str self, for list id

### quote operator
>>> pp('(quote a)')
a

>>> pp('(quote (a b c))')
(a b c)

### atom operator
>>> pp('(atom (quote a))')
t

>>> pp('(atom (quote (a b c)))')
()

>>> pp('(atom (quote ()))')
t

>>> pp('(atom (atom (quote a)))')
t

>>> pp('(atom (quote (atom (quote a))))')
()

### eq operator
>>> pp('(eq (quote a) (quote a))')
t

>>> pp('(eq (quote a) (quote b))')
()

>>> pp('(eq (quote ()) (quote ()))')
t

### car operator
>>> pp('(car (quote (a b c)))')
a

### cdr operator
>>> pp('(cdr (quote (a b c)))')
(b c)

### cons operator
>>> pp('(cons (quote a) (quote (b c)))')
(a b c)

>>> pp('(cons (quote a) (cons (quote b) (cons (quote c) (quote ()))))')
(a b c)

>>> pp('(car (cons (quote a) (quote (b c))))')
a

>>> pp('(cdr (cons (quote a) (quote (b c))))')
(b c)
"""

from parser import parse, unparse


def _isAtom(e):
    """
    >>> _isAtom('foo')
    True

    >>> _isAtom([])
    True

    >>> _isAtom(['foo'])
    False
    """
    assert e is not None
    return isinstance(e, str) or e == []


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
            arg1 = eval(e[1])
            return 't' if _isAtom(arg1) else []
        elif str(e[0]) == 'eq':
            # what if eq has wrong number of args?
            arg1 = eval(e[1])
            arg2 = eval(e[2])
            return 't' if arg1 == arg2 else []
        elif str(e[0]) == 'car':
            # what if car has wrong number of args?
            arg1 = eval(e[1])
            # what if arg1 is not a list?
            return arg1[0]
        elif str(e[0]) == 'cdr':
            # what if cdr has wrong number of args?
            arg1 = eval(e[1])
            # what if arg1 is not a list?
            return arg1[1:]
        elif str(e[0]) == 'cons':
            # what if cons has wrong number of args?
            arg1 = eval(e[1])
            arg2 = eval(e[2])
            ret = [arg1]
            ret.extend(arg2)
            return ret
        else:
            raise ValueError('NYI: {}'.format(e[0]))
    raise ValueError('NYI')


def pp(s):
    return print(unparse(eval(parse(s))))
