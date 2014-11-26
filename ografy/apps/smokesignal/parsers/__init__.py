import json
import types

from ografy.apps.smokesignal.util.importlib import import_module


def from_json(data):
    return json.loads(data)


def get_json_at_location(list_location, json_data):
    split_list_location = list_location.split('.')

    if list_location != '':
        for loc in split_list_location:
            if isinstance(json_data, dict):
                if loc in json_data:
                    json_data = json_data[loc]

    return json_data


def parse_list_data_mapping(data_mapping, json_at_mapped_location, sub_submapping=None, sub_schema_location=None):
    parsed_mapping = []
    for list_item in json_at_mapped_location:
        new_dict = parse_dict_data_mapping(data_mapping, list_item)
        if sub_submapping and sub_schema_location:
            json_at_mapped_location = get_json_at_location(sub_schema_location, list_item)
            new_dict[sub_submapping['outputName']] = parse_json_submapping(sub_submapping, json_at_mapped_location)
        parsed_mapping.append(new_dict)

    return parsed_mapping


def parse_dict_data_mapping(data_mapping, json_at_mapped_location):
    parsed_mapping_item = {}
    for k, v in data_mapping.items():
        if v in json_at_mapped_location:
            parsed_mapping_item[k] = json_at_mapped_location[v]
    return parsed_mapping_item


def parse_json_submapping(submapping, json_dict):
    schema_location = submapping['schemaLocation']
    json_at_mapped_location = get_json_at_location(schema_location, json_dict)
    data_mapping = submapping['dataMapping']
    parsed_mapping = []

    if 'submapping' in submapping:
        sub_submapping = submapping['submapping']
        sub_schema_location = sub_submapping['schemaLocation']
        if submapping['type'] == 'list':
            parsed_mapping.extend(parse_list_data_mapping(data_mapping, json_at_mapped_location, sub_submapping, sub_schema_location))
        elif submapping['type'] == 'dict':
            parsed_mapping.append(parse_dict_data_mapping(data_mapping, json_at_mapped_location, sub_submapping, sub_schema_location))
    else:
        if submapping['type'] == 'list':
            parsed_mapping.extend(parse_list_data_mapping(data_mapping, json_at_mapped_location))
        elif submapping['type'] == 'dict':
            parsed_mapping.append(parse_dict_data_mapping(data_mapping, json_at_mapped_location))

    return parsed_mapping


class Parser(object):
    @staticmethod
    def create(name, parser_name=None, mapping={}):
        module = import_module('ografy.apps.smokesignal.parsers.' + name.lower())
        mapping_dict = from_json(mapping)

        if parser_name is None:
            parser_name = name

        instance = {}

        for mapping_name in list(mapping_dict):
            submapping_dict = mapping_dict.get(mapping_name)
            level_1_submapping = submapping_dict.get('submapping')
            func = Parser.parse
            instance[mapping_name] = types.MethodType(func(func, level_1_submapping), instance)

        return type(parser_name, (), instance)


    def parse(self, submapping):
        def _parse(self, json_data):
            # json_dict = from_json(json_data)
            output_to_return = {}

            if isinstance(submapping, dict):
                output_to_return[submapping['outputName']] = parse_json_submapping(submapping, json_dict)

            return output_to_return

        return _parse
