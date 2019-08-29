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

### cond operator
>>> pp('(cond ((eq (quote a) (quote b)) (quote first)) \
              ((atom (quote a)) (quote second)))')
second

>>> pp('(cond ((eq (quote a) (quote a)) (quote first)) \
              ((atom (quote a)) (quote second)))')
first

>>> pp('(cond (() (quote first)) \
              (() (quote second)))')
()

### lambda
>>> pp('((lambda () (quote foo)))')
foo

>>> pp('((lambda (x) (cons x (quote (b)))) (quote a))')
(a b)

>>> pp('((lambda (x y) (cons x (cdr y))) \
         (quote z)                       \
         (quote (a b c)))')
(z b c)

>>> pp('((lambda (f) (f (quote (b c)))) \
         (quote (lambda (x) (cons (quote a) x))))')
(a b c)

# ### label-ed function
# >>> pp('((label f (lambda (x) (quote f))))   \
#          (quote a))')
# (a b)

### program
>>> pp('(program \
         (label f (lambda (x) (cons x (quote (b)))))   \
         (f (quote a)))')
(a b)
"""

from s_parser import parse, unparse


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


def eval(e, context):
    if e == []:
        return e
    if context is None:
        context = []
    assert isinstance(e, str) or isinstance(e, list)
    assert isinstance(context, list)
    if isinstance(e, str):
        return from_context(context, e[0])
    if isinstance(e[0], str):
        if e[0] == 'quote':
            # what is quote has wrong number of args?
            # note quote does not do argument eval!
            return e[1]
        elif e[0] == 'atom':
            # what is atom has wrong number of args?
            arg1 = eval(e[1], context)
            return 't' if _isAtom(arg1) else []
        elif e[0] == 'eq':
            # what if eq has wrong number of args?
            arg1 = eval(e[1], context)
            arg2 = eval(e[2], context)
            return 't' if arg1 == arg2 else []
        elif e[0] == 'car':
            # what if car has wrong number of args?
            arg1 = eval(e[1], context)
            # what if arg1 is not a list?
            return arg1[0]
        elif e[0] == 'cdr':
            # what if cdr has wrong number of args?
            arg1 = eval(e[1], context)
            # what if arg1 is not a list?
            return arg1[1:]
        elif e[0] == 'cons':
            # what if cons has wrong number of args?
            arg1 = eval(e[1], context)
            arg2 = eval(e[2], context)
            ret = [arg1]
            ret.extend(arg2)
            return ret
        elif e[0] == 'cond':
            # what if cond is not composed of pairs?
            # is it correct to return () if no pair matches?
            # note cond does lazy evaluation!
            for pair in e[1:]:
                if eval(pair[0], context) == 't':
                    return eval(pair[1], context)
            return []
        elif e[0] == 'label':
            # are labels for functions only or for general expressions?
            context.append([e[1], e[2]])
            # return value or () here?
            return []
        elif e[0] == 'program':
            # context get's updated from 'statement' to statement
            p = [eval(arg, context) for arg in e[1:]]
            # last expression return is the value of program
            return p[-1]
        else:
            s = from_context(context, e[0])
            if s == e[0]:
                raise ValueError('symbols cannot be operators: ' + str(s))
            e[0] = s
            return eval(e, context)
    elif e[0][0] == 'lambda':
        func = e[0]
        args = [eval(arg, context) for arg in e[1:]]
        params = func[1]
        body = func[2]
        return eval(body, context + list(zip(params, args)))
    raise ValueError('NYI: ' + str(e))


def from_context(context, atom):
    assert isinstance(atom, str)
    if context is None:
        raise ValueError('unknown atom: ' + atom)
    else:
        for k, v in context:
            if k == atom:
                return v
    raise ValueError('unknown atom: {}\ncontext: {}'.format(atom, context))


def pp(s):
    return print(unparse(eval(parse(s), [])))
