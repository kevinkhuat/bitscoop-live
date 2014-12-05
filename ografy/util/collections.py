from collections import Mapping


class DictView(Mapping):
    """
    View of a subset of a dictionary.
    """
    # TODO: Implement other methods to clean this up.
    def __init__(self, source, valid_keys):
        self.source = source
        self.valid_keys = set(valid_keys)
        self._length = len(valid_keys)

    def __getitem__(self, key):
        if key in self.valid_keys:
            return self.source.get(key)
        else:
            raise KeyError(key)

    def __len__(self):
        return self._length

    def __iter__(self):
        for key in self.valid_keys:
            yield key


def update(obj, kwargs):
    for key, value in kwargs.items():
        setattr(obj, key, value)
