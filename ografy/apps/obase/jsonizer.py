__author__ = 'kyle'

import jsonpickle

from django.core import serializers
from django.db import models
from mongoengine.base.document import BaseDocument


class Jsonizer(jsonpickle):
    """A custom JSONEncoder class that knows how to encode core custom
    objects.

    Custom objects are encoded as JSON object literals (ie, dicts) with
    one key, '__TypeName__' where 'TypeName' is the actual name of the
    type to which the object belongs.  That single key maps to another
    object literal which is just the __dict__ of the object encoded."""

    django_serializer = serializers.get_serializer("json")
    django_deserializer = serializers.get_deserializer("json")

    def custom_encode(self, obj):
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

    def custom_decode(self, obj):
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