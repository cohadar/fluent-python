"""
Every LISP data object has 3 properties:
* identity - memory address of str or tuple
* type - str or tuple
* value - for str self, for tuple id


### t symbol in context
>>> pp('t')
t

>>> pp('(cons t ())')
(t)

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

### label-ed function
>>> pp('((label f (lambda (x) (cons x f))) \
         (quote foo))')
(foo label f (lambda (x) (cons x f)))

### recursive function
# >>> pp('((label subst (lambda (x y z) \
#                        (cond ((atom z) \
#                               (cond ((eq z y) x) \
#                                     ((quote t) z))) \
#                              ((quote t) (cons (subst x y (car z)) \
#                                               (subst x y (cdr z))))))) \
#              (quote m) (quote b) (quote (a b (a b c) d)))')
# (a m (a m c) d)
"""

from s_parser import parse, unparse


def quote(params, context):
    """
    QUOTE operator.
    note that quote does not do argument eval!
    >>> pp('(quote a)')
    a

    >>> pp('(quote (a b c))')
    (a b c)

    >>> pp('(quote)')
    Traceback (most recent call last):
    ValueError: wrong numbers of params for QUOTE

    >>> pp('(quote a b c)')
    Traceback (most recent call last):
    ValueError: wrong numbers of params for QUOTE
    """
    if len(params) != 1:
        raise ValueError('wrong numbers of params for QUOTE')
    return params[0]


def atom(params, context):
    """
    ATOM operator.
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

    >>> pp('(atom)')
    Traceback (most recent call last):
    ValueError: wrong numbers of params for ATOM

    >>> pp('(atom (quote a) (quote a))')
    Traceback (most recent call last):
    ValueError: wrong numbers of params for ATOM
    """
    if len(params) != 1:
        raise ValueError('wrong numbers of params for ATOM')
    arg1 = eval(params[0], context)
    return 't' if isinstance(arg1, str) or arg1 == () else ()


def eq(params, context):
    """
    EQ operator.
    returns 't' if both args are same string or both are empty lists, else ()
    >>> pp('(eq (quote a) (quote a))')
    t

    >>> pp('(eq (quote a) (quote b))')
    ()

    >>> pp('(eq (quote ()) (quote ()))')
    t

    >>> pp('(eq (quote a))')
    Traceback (most recent call last):
    ValueError: wrong numbers of params for EQ

    >>> pp('(eq (quote a) (quote a) (quote a))')
    Traceback (most recent call last):
    ValueError: wrong numbers of params for EQ
    """
    if len(params) != 2:
        raise ValueError('wrong numbers of params for EQ')
    arg1 = eval(params[0], context)
    arg2 = eval(params[1], context)
    if isinstance(arg1, str):
        if isinstance(arg2, str):
            return 't' if arg1 == arg2 else ()
        else:
            return ()
    else:
        if isinstance(arg2, str):
            return ()
        else:
            if arg1 == () and arg2 == ():
                return 't'
            else:
                return id(arg1) == id(arg2)


def car(params, context):
    """
    CAR operator.
    returns the head of the list or nil
    >>> pp('(car (quote (a b c)))')
    a

    >>> pp('(car (quote ()))')
    ()

    >>> pp('(car (quote x))')
    Traceback (most recent call last):
    ValueError: not a list: x

    >>> pp('(car (quote x) (quote x))')
    Traceback (most recent call last):
    ValueError: wrong numbers of params for CAR

    >>> pp('(car)')
    Traceback (most recent call last):
    ValueError: wrong numbers of params for CAR
    """
    if len(params) != 1:
        raise ValueError('wrong numbers of params for CAR')
    arg1 = eval(params[0], context)
    if not isinstance(arg1, tuple):
        raise ValueError('not a list: ' + str(arg1))
    if arg1 == ():
        return ()
    return arg1[0]


def cdr(params, context):
    """
    CDR operator.
    gets the tail of the list

    >>> pp('(cdr (quote (a b c)))')
    (b c)

    >>> pp('(cdr (quote (c)))')
    ()

    >>> pp('(cdr (quote ()))')
    ()

    >>> pp('(cdr (quote ()) (quote ()))')
    Traceback (most recent call last):
    ValueError: wrong numbers of params for CDR

    >>> pp('(cdr)')
    Traceback (most recent call last):
    ValueError: wrong numbers of params for CDR

    >>> pp('(cdr (quote t))')
    Traceback (most recent call last):
    ValueError: not a list: t
    """
    if len(params) != 1:
        raise ValueError('wrong numbers of params for CDR')
    arg1 = eval(params[0], context)
    if not isinstance(arg1, tuple):
        raise ValueError('not a list: ' + str(arg1))
    return arg1[1:]


def cons(params, context):
    """
    CONS operator.
    append item to the head of the list
    >>> pp('(cons (quote a) (quote (b c)))')
    (a b c)

    >>> pp('(cons (quote a) (cons (quote b) (cons (quote c) (quote ()))))')
    (a b c)

    >>> pp('(car (cons (quote a) (quote (b c))))')
    a

    >>> pp('(cdr (cons (quote a) (quote (b c))))')
    (b c)

    >>> pp('(cons (quote a))')
    Traceback (most recent call last):
    ValueError: wrong numbers of params for CONS

    >>> pp('(cons (quote a) (quote a) (quote a))')
    Traceback (most recent call last):
    ValueError: wrong numbers of params for CONS

    >>> pp('(cons (quote a) (quote b))')
    Traceback (most recent call last):
    ValueError: not a list: b
    """
    if len(params) != 2:
        raise ValueError('wrong numbers of params for CONS')
    arg1 = eval(params[0], context)
    arg2 = eval(params[1], context)
    if not isinstance(arg2, tuple):
        raise ValueError('not a list: ' + str(arg2))
    return (arg1,) + arg2


def cond(params, context):
    """
    COND operator.
    lazy conditional execution of pair alternatives
    >>> pp('(cond \
                ((eq(quote a)(quote b)) \
                    (quote first)) \
                ((atom(quote a)) \
                    (quote second)))')
    second

    >>> pp('(cond \
                ((eq(quote a)(quote a)) \
                    (quote first)) \
                ((atom (quote a)) \
                    (quote second)))')
    first

    >>> pp('(cond \
                (() \
                    (quote first)) \
                (() \
                    (quote second)))')
    ()

    >>> pp('(cond \
                (() \
                    (quote first)) \
                ((quote t) \
                    (quote second)))')
    second

    >>> pp('(cond)')
    ()

    >>> pp('(cond (t))')
    t

    >>> pp('(cond ((quote t)))')
    t

    >>> pp('(cond t)')
    Traceback (most recent call last):
    ValueError: COND clause must be a list
    """
    # what if cond is not composed of pairs?
    # is it correct to return () if no pair matches?
    for clause in params:
        if not isinstance(clause, tuple):
            raise ValueError('COND clause must be a list')
        if clause == ():
            raise ValueError('COND clause cannot be empty list')
        ret = eval(clause[0], context)
        if ret == 't':
            for exp in clause[1:]:
                ret = eval(exp, context)
            return ret
    return ()


def eval(e, context):
    if e == ():
        return e
    if context is None:
        context = {}
    assert isinstance(e, str) or isinstance(e, tuple)
    assert isinstance(context, dict)
    if isinstance(e, str):
        return from_context(context, e[0])
    if isinstance(e[0], str):
        if e[0] == 'quote':
            return quote(e[1:], context)
        elif e[0] == 'atom':
            return atom(e[1:], context)
        elif e[0] == 'eq':
            return eq(e[1:], context)
        elif e[0] == 'car':
            return car(e[1:], context)
        elif e[0] == 'cdr':
            return cdr(e[1:], context)
        elif e[0] == 'cons':
            return cons(e[1:], context)
        elif e[0] == 'cond':
            return cond(e[1:], context)
        else:
            s = from_context(context, e[0])
            if s == e[0]:
                if len(e) == 1:
                    return s
                else:
                    raise ValueError('symbols cannot be operators: ' + str(s))
            return eval((s,) + e[1:], context)
    elif e[0][0] == 'lambda':
        decl = e[0]
        params = decl[1]
        body = decl[2]
        args = [eval(arg, context) for arg in e[1:]]
        context.update(zip(params, args))
        return eval(body, context)
    elif e[0][0] == 'label':
        name = e[0][1]
        decl = e[0][2]
        params = decl[1]
        body = decl[2]
        args = [eval(arg, context) for arg in e[1:]]
        context.update(zip(params, args))
        context.update([[name, e[0]]])
        return eval(body, context)
    raise ValueError('NYI: ' + str(e))


def from_context(context, atom):
    assert isinstance(atom, str)
    if context is None:
        raise ValueError('unknown atom: ' + atom)
    elif atom in context:
        return context[atom]
    raise ValueError('unknown atom: {}\ncontext: {}'.format(atom, context))


def pp(s):
    return print(unparse(eval(parse(s), {'t': 't'})))
