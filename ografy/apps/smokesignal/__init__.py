from __future__ import unicode_literals

from ografy.lib.smokesignal.parsers import Parser


def parse_content(name, method_name, data, parser_name=None):
    inst = Parser.create(name, parser_name)

    method = getattr(inst, method_name)

    return method(data)
