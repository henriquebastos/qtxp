from collections import OrderedDict, Callable


class DefaultOrderedDict(OrderedDict):
    # Source: http://stackoverflow.com/a/6190500/562769
    def __init__(self, default_factory, *args, **kwargs):
        if not isinstance(default_factory, Callable):
            raise TypeError('first argument must be callable')

        super().__init__(*args, **kwargs)

        self.default_factory = default_factory

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key):
        self[key] = value = self.default_factory()
        return value

    def __reduce__(self):
        return type(self), self.default_factory, None, None, self.items()

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        return type(self)(self.default_factory, self)

    def __deepcopy__(self, memo):
        import copy
        return type(self)(self.default_factory,
                          copy.deepcopy(self.items()))

    def __repr__(self):
        return f'{type(self).__name__}({self.default_factory}, {super().__repr__(self)})'
