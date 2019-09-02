"""
klasa koja predstavlja s-expression
i lista i sam string su s-expression

interni data da je ili str ili nested tuple S expressiona

da ima fromStrTuple method koji prihvata izlaz parsera i vraća S kao prelazno
rešenje.
Prvo vidi kako će da se uklopi u eval, a onda napravi direktan parser za S

ima lep quote handling

ima isAtom, isNil i __eq__ __hash__ implementirano,
kao i razne potrebne konstruktore i __iter__
"""

import s_parser


class S():
    """
    LISP S-expression.
    Wrapper around str and tuple
    """
    def __init__(self, data=None):
        """
        >>> S()._data
        ()
        >>> S('foo')._data
        'foo'
        >>> S(())._data
        ()
        >>> S(('foo',))._data
        ('foo',)
        >>> S(('foo','bar'))._data
        ('foo', 'bar')
        >>> S(('foo', ('aa', 'bb'), 'bar'))._data
        ('foo', ('aa', 'bb'), 'bar')
        >>> S(55)._data
        Traceback (most recent call last):
        AssertionError: '55' must be str or tuple, not '<class 'int'>'
        >>> S(('foo', ('a', 'b', ('x', [], 'y'), 'bar')))._data
        Traceback (most recent call last):
        AssertionError: '[]' must be str or tuple, not '<class 'list'>'
        """
        if data is None:
            data = ()
        S._validate(data)
        self._data = data
        if isinstance(data, tuple):
            if data == ():
                self._head = self
                self._tail = self
            else:
                self._head = S(data[0])
                self._tail = S(data[1:])

    @staticmethod
    def _validate(data):
        if isinstance(data, str):
            return True
        elif isinstance(data, tuple):
            return all((S._validate(el) for el in data))
        else:
            assert False, "'{}' must be str or tuple, not '{}'".format(data, type(data))

    def __repr__(self):
        """
        >>> S(())
        ()
        >>> S('foo')
        foo
        >>> S(('foo',))
        (foo)
        >>> S(('foo', 'bar'))
        (foo bar)
        >>> S((('foo',),))
        ((foo))
        >>> S(('cdr', ('cons', ('quote', 'a'), ('quote', ('b', 'c')))))
        (cdr (cons (quote a) (quote (b c))))
        """
        return s_parser.unparse(self._data)

    @staticmethod
    def parse(text):
        """
        >>> S.parse('()')
        ()

        >>> S.parse('foo')
        foo

        >>> S.parse('(foo)')
        (foo)

        >>> S.parse('(foo bar)')
        (foo bar)

        >>> S.parse('((foo))')
        ((foo))

        >>> S.parse('(cdr (cons (quote a) (quote (b c))))')
        (cdr (cons (quote a) (quote (b c))))

        >>> S.parse('(a) b')
        Traceback (most recent call last):
        ValueError: extra stuff:['b']
        """
        assert isinstance(text, str)
        return S(s_parser.parse(text))

    def isNil(self):
        """
        >>> S.parse('()').isNil()
        True
        >>> S.parse('foo').isNil()
        False
        >>> S.parse('(foo)').isNil()
        False
        """
        return self._data == ()

    def isVar(self):
        """
        >>> S.parse('()').isVar()
        False
        >>> S.parse('foo').isVar()
        True
        >>> S.parse('(foo)').isVar()
        False
        """
        return isinstance(self._data, str)

    def isAtom(self):
        """
        >>> S.parse('()').isAtom()
        True
        >>> S.parse('foo').isAtom()
        True
        >>> S.parse('(foo)').isAtom()
        False
        """
        return self.isNil() or self.isVar()

    def head(self):
        """
        >>> S.parse('(foo bar zar)').head()
        foo
        """
        assert isinstance(self._data, tuple)
        return self._head

    def tail(self):
        """
        >>> S.parse('(foo bar zar)').tail()
        (bar zar)
        """
        assert isinstance(self._data, tuple)
        return self._tail

    @classmethod
    def cons(cls, head, tail):
        """
        >>> S.cons(S('foo'), S.parse('(bar zar)'))
        (foo bar zar)
        >>> S.cons(S(()), S.parse('(bar zar)'))
        (() bar zar)
        >>> S.cons(S('foo'), S())
        (foo)
        """
        assert isinstance(head, S)
        assert isinstance(tail, S)
        return cls((head._data,) + tail._data)

    def __len__(self):
        """
        >>> len(S.parse('()'))
        0
        >>> len(S.parse('(foo)'))
        1
        >>> len(S.parse('(foo bar)'))
        2
        >>> len(S('foo'))
        1
        """
        if self.isVar():
            return 1
        return len(self._data)

    def __eq__(self, other):
        """
        >>> S.parse('foo') == 'foo'
        True
        >>> S.parse('foo') == 'bar'
        False
        >>> S.parse('foo') == S('foo')
        True
        >>> S.parse('()') == S(())
        True
        >>> S.parse('(foo bar)') == S.parse('(foo bar)')
        False
        >>> S.parse('(foo bar)') == S.parse('(foo zar)')
        False
        """
        if isinstance(other, str):
            return self._data == other
        if self.isAtom() and other.isAtom():
            return self._data == other._data
        return id(self) == id(other)

    def __hash__(self):
        return hash(self._data)
