import s_parser


class S():
    """
    Class representing LISP S-expressions
    """
    def __init__(self, data=None):
        """
        constructor takes None or a string or a tuple containing only
        strings or other tuples.
        >>> S(None)._data
        ()
        >>> S(())._data
        ()
        >>> S('foo')._data
        'foo'
        >>> S(('foo', ('aaa', 'bbb'), 'bar'))._data
        ('foo', ('aaa', 'bbb'), 'bar')
        """
        if data is None:
            data = ()
        if isinstance(data, str):
            assert data.find('(') == -1
            assert data.find(')') == -1
        else:
            assert isinstance(data, tuple)
            for el in data:
                assert isinstance(el, str) or isinstance(el, tuple)
        self._data = data

    def __repr__(self):
        s_parser.unparse(self._data)

    @staticmethod
    def parse(text):
        """
        >>> type(s_parser.parse('foo', S))
        tuple

        >>> type(s_parser.parse('()', S))
        tuple

        >>> type(s_parser.parse('(foo)', S))
        <class 's_expression.S'>

        >>> repr(s_parser.parse('()', S))
        '()'
        """
        return S(s_parser.parse(text, tuple))

    def isNil(self):
        return self._data == ()

    def isVariable(self):
        return isinstance(self._data, str)

    def isAtom(self):
        return self.isNil() or self.isVariable()

    def __iter__(self):
        assert not self.isVariable()
        return iter(self._data)

    def __getitem__(self, i):
        return self._data[i]

    def __add__(self, other):
        return S(self._data + other._data)

    def __eq__(self, other):
        if isinstance(self._data, str):
            return self._data == other._data
        else:
            return id(self._data) == id(other._data)
