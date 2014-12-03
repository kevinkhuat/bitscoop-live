__author__ = 'kyle'

import jsonpickle

from django.core import serializers
from django.db import models
from mongoengine.base.document import BaseDocument

from ografy.apps.obase.documents import Data, Event, Message


class Jsonizer:

    def serialize(self, obj):
        return jsonpickle.encode(obj)

    def deserialize(self, obj):
        return jsonpickle.decode(obj)

    def auto_serialize(self, obj):
        if isinstance(obj, models.Model):
            obj.isDjangoModel = True
            return self.django_serializer(obj)
        if isinstance(obj, BaseDocument):
            obj.isMongoEngineDoc = True
            return BaseDocument.to_json(obj)
        if isinstance(obj, list):
            ret_list = []
            for sub_obj in obj:
                ret_list.append(self.custom_encode(sub_obj))
            return ret_list
        if isinstance(obj, dict):
            ret_dict = {}
            for key, value in obj:
                ret_dict[self.custom_encode(key)] = self.custom_encode(value)
            return ret_dict
        return jsonpickle.encode(obj)

    def auto_deserialize(self, obj):
        if isinstance(obj, str):
            decoded_obj = jsonpickle.decode(obj)
        else:
            decoded_obj = obj

        if decoded_obj.isDjangoModel:
            return self.django_deserializer(obj)
        if decoded_obj.isMongoEngineDoc:
            return BaseDocument.from_json(obj)
        if isinstance(decoded_obj, list):
            ret_list = []
            for sub_obj in obj:
                ret_list.append(self.custom_decode(sub_obj))
            return ret_list
        if isinstance(decoded_obj, dict):
            ret_dict = {}
            for key, value in obj:
                ret_dict[self.custom_decode(key)] = self.custom_decode(value)
            return ret_dict
        return decoded_obj

    def serialize_list(self, obj_list):
        ret_list = '['
        not_first = False
        for obj in obj_list:
            if not_first:
                ret_list += ','
            ret_list += self.serialize(obj)
        ret_list = ']'
        return ret_list

    # Todo: Remove
    # def _reverse_replace(s, old, new, occurrence):
    #     li = s.rsplit(old, occurrence)
    #     return new.join(li)

    # Todo: Fix, look at
    # http://stackoverflow.com/questions/13384454/split-json-objects-using-a-regular-expression
    # http://stackoverflow.com/questions/10889506/different-json-encoders-for-different-depths
    # http://www.django-rest-framework.org/api-guide/serializers/
    def deserialize_list(self, json_list):
        # json_list.replace('[', '', 1)
        # self._reverse_replace(list, ']', '', 1)
        raise NotImplementedError


class MongoJsonizer(Jsonizer):
    def serialize(self, obj):
        return BaseDocument.to_json(obj)

    def deserialize(self, obj):
        return BaseDocument.to_json(obj)


class DjangoJsonizer(Jsonizer):

    def __init__(self):
        self.django_serializer = serializers.get_serializer("json")
        self.django_deserializer = serializers.get_deserializer("json")

    def serialize(self, obj):
        return self.django_serializer(obj)

    def deserialize(self, obj):
        return self.django_deserializer(obj)

    def serialize_list(self, obj_list):
        return self.django_serializer(obj_list)

    def deserialize_list(self, json_list):
        return self.django_deserializer(json_list)


class EventJsonizer(MongoJsonizer):
    def serialize(self, obj):
        return Event.to_json(obj)

    def deserialize(self, obj):
        return Event.to_json(obj)


class DataJsonizer(MongoJsonizer):
    def serialize(self, obj):
        return Data.to_json(obj)

    def deserialize(self, obj):
        return Data.to_json(obj)


class MessageJsonizer(MongoJsonizer):
    def serialize(self, obj):
        return Message.to_json(obj)

    def deserialize(self, obj):
        return Message.to_json(obj)

