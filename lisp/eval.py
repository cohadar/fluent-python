"""
Every LISP data object has 3 properties:
* identity - memory address of str or tuple
* type - str or tuple
* value - for str self, for tuple id


### t symbol in context
# >>> pp('t')
# t

# >>> pp('(cons t ())')
# (t)

# >>> pp('(cond (t))')
# t


"""

import copy
from s_expression import S


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
    return params.head()


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
    arg1 = eval(params.head(), context)
    return S('t') if arg1.isAtom() else S()


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

    >>> pp('(eq (quote (aaa bbb)) (quote (aaa bbb)))')
    ()

    >>> pp('(eq (quote a))')
    Traceback (most recent call last):
    ValueError: wrong numbers of params for EQ

    >>> pp('(eq (quote a) (quote a) (quote a))')
    Traceback (most recent call last):
    ValueError: wrong numbers of params for EQ
    """
    if len(params) != 2:
        raise ValueError('wrong numbers of params for EQ')
    arg1 = eval(params.head(), context)
    arg2 = eval(params.tail().head(), context)
    return S('t') if arg1 == arg2 else S()


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
    ValueError: CAR param not a list: x

    >>> pp('(car (quote x) (quote x))')
    Traceback (most recent call last):
    ValueError: wrong numbers of params for CAR

    >>> pp('(car)')
    Traceback (most recent call last):
    ValueError: wrong numbers of params for CAR
    """
    if len(params) != 1:
        raise ValueError('wrong numbers of params for CAR')
    arg1 = eval(params.head(), context)
    if arg1.isNil():
        return arg1
    if arg1.isVar():
        raise ValueError('CAR param not a list: ' + str(arg1))
    return arg1.head()


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
    ValueError: CDR param not a list: t
    """
    if len(params) != 1:
        raise ValueError('wrong numbers of params for CDR')
    arg1 = eval(params.head(), context)
    if arg1.isVar():
        raise ValueError('CDR param not a list: ' + str(arg1))
    return arg1.tail()


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
    arg1 = eval(params.head(), context)
    arg2 = eval(params.tail().head(), context)
    if arg2.isVar():
        raise ValueError('not a list: ' + str(arg2))
    return S.cons(arg1, arg2)


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
    >>> pp('(cond ((quote t)))')
    t
    >>> pp('(cond t)')
    Traceback (most recent call last):
    ValueError: COND clause must be a list
    """
    for clause in params:
        if clause.isNil():
            raise ValueError('COND clause cannot be empty list')
        if clause.isVar():
            raise ValueError('COND clause must be a list')
        ret = eval(clause.head(), context)
        if ret == 't':
            for exp in clause.tail():
                ret = eval(exp, context)
            return ret
    return S()


def lambda_(e, context):
    # """
    # LAMBDA function
    # >>> pp('((lambda () (quote foo)))')
    # foo

    # >>> pp('((lambda (x) (cons x (quote (b)))) (quote a))')
    # (a b)

    # >>> pp('((lambda (x y) (cons x (cdr y))) \
    #          (quote z)                       \
    #          (quote (a b c)))')
    # (z b c)

    # >>> pp('((lambda (f) (f (quote (b c)))) (quote (lambda (x) (cons (quote a) x))))')
    # Traceback (most recent call last):
    # ValueError: undefined function: f

    # >>> pp('((lambda ((x)) (cons x (quote (b)))) (quote a))')
    # Traceback (most recent call last):
    # ValueError: invalid parameter: (x)

    # >>> pp('((lambda x (cons x (quote (b)))) (quote a))')
    # Traceback (most recent call last):
    # ValueError: params should be a list, not: x

    # >>> pp('((lambda (x) (cons x (quote (b))) (quote t)) (quote a))')
    # t

    # >>> pp('((lambda (x) ) (quote a))')
    # ()

    # >>> pp('((lambda (x) (cons x (quote (b)))) (quote a) (quote b))')
    # Traceback (most recent call last):
    # ValueError: too many arguments given to LAMBDA

    # >>> pp('((lambda (x) (cons x (quote (b)))) )')
    # Traceback (most recent call last):
    # ValueError: too few arguments given to LAMBDA
    # """
    decl = e.head()
    assert decl.head() == 'lambda'
    params = decl.head().head()
    args = e.tail()
    if isinstance(params, str):
        raise ValueError('params should be a list, not: ' + str(params))
    if len(params) < len(args):
        raise ValueError('too many arguments given to LAMBDA')
    if len(params) > len(args):
        raise ValueError('too few arguments given to LAMBDA')
    for param in params:
        if not isinstance(param, str):
            raise ValueError('invalid parameter: ' + str(param))
    args = [eval(arg, context) for arg in args]
    context = copy.deepcopy(context)
    context.update_vars(zip(params, args))
    ret = ()
    for body in decl[2:]:
        ret = eval(body, context)
    return ret


def defun(e, context):
    # """
    # define a function
    # >>> context = Context(); pp('(defun madd (a b) (cons a (cons b ())))', context); \
    #     pp('(madd (quote x) (quote y))', context)
    # madd
    # (x y)
    # """
    # TODO: cornercases
    name = e[0]
    newe = ['lambda']
    newe += e[1:]
    context.update_funcs({name: tuple(newe)})
    return name


def eval(e, context):
    """
    >>> s = S.parse('()'); eval(s, Context()) == s
    True
    """
    assert isinstance(e, S)
    if e.isNil():
        return e
    if context is None:
        context = Context()
    assert isinstance(context, Context)
    if e.isVar():
        return context.vars[e]
    head = e.head()
    tail = e.tail()
    if head.isVar():
        if head == 'quote':
            return quote(tail, context)
        elif head == 'atom':
            return atom(tail, context)
        elif head == 'eq':
            return eq(tail, context)
        elif head == 'car':
            return car(tail, context)
        elif head == 'cdr':
            return cdr(tail, context)
        elif head == 'cons':
            return cons(tail, context)
        elif head == 'cond':
            return cond(tail, context)
        elif head == 'defun':
            return defun(tail, context)
        else:
            newhead = context.funcs[head]
            assert isinstance(newhead, S)
            newe = S.cons(newhead, tail)
            return eval(newe, context)
    elif head.head() == 'lambda':
        return lambda_(e, context)
    raise ValueError('NYI: ' + str(e))


def pp(text, context=None):
    return print(eval(S.parse(text), context))


class Context():
    def __init__(self, vars=None, funcs=None):
        if vars is None:
            self.vars = {}
        if funcs is None:
            self.funcs = {}
