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
    arg1 = eval(params[0], context)
    if not isinstance(arg1, tuple):
        raise ValueError('CAR param not a list: ' + str(arg1))
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
    ValueError: CDR param not a list: t
    """
    if len(params) != 1:
        raise ValueError('wrong numbers of params for CDR')
    arg1 = eval(params[0], context)
    if not isinstance(arg1, tuple):
        raise ValueError('CDR param not a list: ' + str(arg1))
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


def lambda_(e, context):
    """
    LAMBDA function
    >>> pp('((lambda () (quote foo)))')
    foo

    >>> pp('((lambda (x) (cons x (quote (b)))) (quote a))')
    (a b)

    >>> pp('((lambda (x y) (cons x (cdr y))) \
             (quote z)                       \
             (quote (a b c)))')
    (z b c)

    >>> pp('((lambda (f) (f (quote (b c)))) (quote (lambda (x) (cons (quote a) x))))')
    Traceback (most recent call last):
    ValueError: undefined function: f

    >>> pp('((lambda ((x)) (cons x (quote (b)))) (quote a))')
    Traceback (most recent call last):
    ValueError: invalid parameter: (x)

    >>> pp('((lambda x (cons x (quote (b)))) (quote a))')
    Traceback (most recent call last):
    ValueError: params should be a list, not: x

    >>> pp('((lambda (x) (cons x (quote (b))) (quote t)) (quote a))')
    t

    >>> pp('((lambda (x) ) (quote a))')
    ()

    >>> pp('((lambda (x) (cons x (quote (b)))) (quote a) (quote b))')
    Traceback (most recent call last):
    ValueError: too many arguments given to LAMBDA

    >>> pp('((lambda (x) (cons x (quote (b)))) )')
    Traceback (most recent call last):
    ValueError: too few arguments given to LAMBDA
    """
    decl = e[0]
    assert decl[0] == 'lambda'
    params = decl[1]
    args = e[1:]
    if isinstance(params, str):
        raise ValueError('params should be a list, not: ' + unparse(params))
    if len(params) < len(args):
        raise ValueError('too many arguments given to LAMBDA')
    if len(params) > len(args):
        raise ValueError('too few arguments given to LAMBDA')
    for param in params:
        if not isinstance(param, str):
            raise ValueError('invalid parameter: ' + unparse(param))
    args = [eval(arg, context) for arg in args]
    context = copy.deepcopy(context)
    context.update_vars(zip(params, args))
    ret = ()
    for body in decl[2:]:
        ret = eval(body, context)
    return ret


def defun(e, context):
    """
    define a function
    >>> context = Context(); pp('(defun madd (a b) (cons a (cons b ())))', context); \
        pp('(madd (quote x) (quote y))', context)
    (x y)
    """
    # TODO cornercases
    decl = e[0]
    assert decl[0] == 'label'
    name = decl[1]
    lam = decl[2]
    args = e[1:]
    context.update_vars({name: lam})
    return lambda_(((lam,),) + tuple(args), context)


def eval(e, context):
    if e == ():
        return e
    if context is None:
        context = Context()
    assert isinstance(e, str) or isinstance(e, tuple)
    assert isinstance(context, Context)
    if isinstance(e, str):
        return context.get_var(e)
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
            raise ValueError('undefined function: ' + str(e[0]))
    elif e[0][0] == 'lambda':
        return lambda_(e, context)
    elif e[0][0] == 'defun':
        return defun(e, context)
    raise ValueError('NYI: ' + unparse(e))


def pp(s, context=None):
    return print(unparse(eval(parse(s), context)))


class Context():
    def __init__(self, var_context=None, func_context=None):
        self.var_context = var_context if var_context is not None else {}
        self.func_context = func_context if func_context is not None else {}

    def get_var(self, key):
        assert isinstance(key, str)
        ret = self.var_context.get(key, None)
        if ret:
            return ret
        raise ValueError('unknown variable: ' + key)

    def get_func(self, key):
        assert isinstance(key, str)
        ret = self.func_context.get(key, None)
        if ret:
            return ret
        raise ValueError('undefined function: ' + key)

    def update_vars(self, d):
        self.var_context.update(d)

    def update_funcs(self, d):
        self.func_context.update(d)

