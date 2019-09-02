
class Njak():
    """
    >>> d = {}; d; \
        n = Njak(); n
    {}
    Njak{}
    >>> d = dict({'aa': 33}); d; \
        n = Njak({'aa': 33}); n
    {'aa': 33}
    Njak{'aa': 33}
    """
    def __init__(self, d=None):
        if d is None:
            d = {}
        self._dict = d

    def __repr__(self):
        return 'Njak' + repr(self._dict)


