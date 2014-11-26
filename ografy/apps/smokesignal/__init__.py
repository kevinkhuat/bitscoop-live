from ografy.apps.smokesignal.parsers import Parser


def parse_content(name, method_name, data, parser_name=None):
    inst = Parser.create(name, parser_name)

    method = getattr(inst, method_name)

    return method(data)
