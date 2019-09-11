from symbol import Symbol


class Cons():
    """
    >>> Cons(Symbol.T, Symbol.NIL)
    (T)

    >>> Cons(Symbol.NIL, Symbol.NIL)
    (NIL)

    >>> Cons(Symbol('A'), Cons(Symbol('B'), Cons(Symbol('C'), Symbol.NIL)))
    (A B C)
    """
    def __init__(self, car, cdr):
        assert car is not None
        assert cdr is not None
        assert isinstance(car, Cons) or isinstance(car, Symbol)
        assert isinstance(cdr, Cons) or Symbol.isNIL(cdr)
        self.car = car
        self.cdr = cdr

    def __repr__(self):
        curr = self
        top = []
        while not Symbol.isNIL(curr):
            top.append(curr.car)
            curr = curr.cdr
        return '(' + ' '.join(repr(x) for x in top) + ')'
