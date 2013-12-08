import six


class Options(object):
    test = 'pants'

    def __new__(cls):
        return object.__new__(type('Options', (cls,), {}))


class CoolMeta(type):
    def __new__(cls, name, bases, attrs):
        new_class = super(CoolMeta, cls).__new__(cls, name, bases, attrs)
        return new_class