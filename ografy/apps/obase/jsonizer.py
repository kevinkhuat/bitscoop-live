import jsonpickle

from bson import json_util
from django.core import serializers
from django.db import models
from mongoengine.base.document import BaseDocument
from rest_framework_mongoengine.serializers import MongoEngineModelSerializer

from ografy.apps.obase import documents


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
        first = True
        for obj in obj_list:
            if first:
                first = False
            else:
                ret_list += ','
            ret_list += self.serialize(obj)
        ret_list += ']'
        return ret_list

    def deserialize_list(self, json_list):
        raise NotImplementedError

    def get_serialized_dict(self, obj):
        serialized_object = self.serialize(obj)
        return jsonpickle.decode(serialized_object)

    def get_serialized_value(self, obj, key):
        return self.get_serialized_dict(obj)[key]


class MongoJsonizer(Jsonizer):
    def serialize(self, obj):
        return BaseDocument.to_json(obj)

    def deserialize(self, obj):
        return BaseDocument.from_json(obj)


class BsonJsonizer(Jsonizer):
    def serialize(self, obj):
        return json_util.dumps(obj)

    def deserialize(self, obj):
        return json_util.loads(obj)


class DjangoJsonizer(Jsonizer):
    def __init__(self):
        super.__init__()
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


class EventDRFSerializer(MongoEngineModelSerializer):
    class Meta:
        model = documents.Event
        # depth = 2
        # exclude = ('pk',)


class EventJsonizer(MongoJsonizer):
    def __init__(self):
        super.__init__()
        self.DRF_serializer = EventDRFSerializer()

    def serialize(self, obj):
        return documents.Event.to_json(obj)

    def deserialize(self, obj):
        return documents.Event.from_json(obj)


class DataDRFSerializer(MongoEngineModelSerializer):
    class Meta:
        model = documents.Data


class DataJsonizer(MongoJsonizer):
    def __init__(self):
        super.__init__()
        self.DRF_serializer = DataDRFSerializer()

    def serialize(self, obj):
        return documents.Data.to_json(obj)

    def deserialize(self, obj):
        return documents.Data.from_json(obj)


class MessageDRFSerializer(MongoEngineModelSerializer):
    class Meta:
        model = documents.Message


class MessageJsonizer(MongoJsonizer):
    def __init__(self):
        super.__init__()
        self.DRF_serializer = MessageDRFSerializer()

    def serialize(self, obj):
        return documents.Message.to_json(obj)

    def deserialize(self, obj):
        return documents.Message.from_json(obj)

