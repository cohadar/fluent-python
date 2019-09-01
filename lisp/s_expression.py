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
                self.head = self
                self.tail = self
            else:
                self.head = S(data[0])
                self.tail = S(data[1:])

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
        assert isinstance(self._data, tuple)
        return self.head

    def tail(self):
        assert isinstance(self._data, tuple)
        return self.tail

    @staticmethod
    def cons(head, tail):
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
        return S((head._data,) + tail._data)

    def __eq__(self, other):
        if isinstance(other, str):
            return self._data == other
        raise ValueError('NYI __eq__')

    def __hash__(self):
        return hash(self._data)


class Smap():
    """
    map{str -> S}
    TODO: S -> S mapping
    """
    def __init__(self, smap=None):
        """
        >>> Smap()
        {}
        >>> Smap({'foo': S.parse('(aaa bbb)')})
        {'foo': (aaa bbb)}
        """
        self._data = {} if smap is None else dict(smap)
        self.validate()

    def validate(self):
        """
        >>> Smap({'foo': S.parse('(aaa bbb)'), 123: S()})
        Traceback (most recent call last):
        AssertionError: key is not str: 123
        >>> Smap({'foo': S.parse('(aaa bbb)'), "123": ['do', 're', 'mi']})
        Traceback (most recent call last):
        AssertionError: value is not S: ['do', 're', 'mi']
        """
        for k, v in self._data.items():
            assert isinstance(k, str), "key is not str: {}".format(k)
            assert isinstance(v, S), "value is not S: {}".format(v)

    def __getitem__(self, key):
        """
        >>> Smap({'foo': S.parse('(aaa bbb)')})['foo']
        (aaa bbb)
        >>> Smap({'foo': S.parse('(aaa bbb)')})['bar']
        Traceback (most recent call last):
        ValueError: unknown variable or func: bar
        >>> Smap({'foo': S.parse('(aaa bbb)')})[1.23]
        Traceback (most recent call last):
        AssertionError: key is not str: 1.23
        """
        assert isinstance(key, str), "key is not str: {}".format(key)
        ret = self._data.get(key, None)
        if ret:
            return ret
        raise ValueError('unknown variable or func: ' + key)

    def update(self, d):
        """
        >>> a = Smap({'foo': S.parse('(quote aaa)')}); \
            b = Smap({'bar': S.parse('(quote bbb)')}); \
            a.update(b); \
            a; \
            b
        """
        self._data.update(d)
        self.validate()

    def __repr__(self):
        return repr(self._data)
