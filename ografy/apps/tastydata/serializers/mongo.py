import bson
import jsonpickle
import mongoengine
import warnings
import ografy.apps.tastydata.fields.mongo as mongo_fields

from bson.json_util import dumps as bson_dumps, loads as bson_loads
from collections import OrderedDict
from django.core.paginator import Page
from django.db import models
from django.forms import widgets
from mongoengine.base import BaseDocument
from rest_framework import fields, relations, serializers


class DocumentSerializer(serializers.ModelSerializer):

    """
    A `DocumentSerializer` is just a regular `Serializer`, except that:

    * A set of default fields are automatically populated.
    * A set of default validators are automatically populated.
    * Default `.create()` and `.update()` implementations are provided.

    The process of automatically determining a set of serializer fields
    based on the model fields is reasonably complex, but you almost certainly
    don't need to dig into the implementation.

    If the `DocumentSerializer` class *doesn't* generate the set of fields that
    you need you should either declare the extra/differing fields explicitly on
    the serializer class, or simply use a `Serializer` class.
    """

    _default_depth = 5

    _field_mapping = {
        mongoengine.BooleanField: fields.BooleanField,
        mongoengine.DateTimeField: fields.DateTimeField,
        mongoengine.DecimalField: fields.DecimalField,
        mongoengine.DynamicField: mongo_fields.DynamicField,
        mongoengine.EmailField: fields.EmailField,
        mongoengine.EmbeddedDocumentField:  mongo_fields.EmbeddedDocumentField,
        mongoengine.FileField: fields.FileField,
        mongoengine.FloatField: fields.FloatField,
        mongoengine.ImageField: fields.ImageField,
        mongoengine.IntField: fields.IntegerField,
        mongoengine.ListField:  mongo_fields.ListField,
        mongoengine.ObjectIdField:  mongo_fields.ObjectIdField,
        mongoengine.ReferenceField:  mongo_fields.ReferenceField,
        mongoengine.SortedListField:  mongo_fields.ListField,
        mongoengine.StringField: fields.CharField,
        mongoengine.URLField: fields.URLField,
        mongoengine.UUIDField: fields.CharField
    }
    _related_class = relations.PrimaryKeyRelatedField
    _attribute_dict = {
        mongoengine.StringField: ['max_length'],
        mongoengine.DecimalField: ['min_value', 'max_value'],
        mongoengine.EmailField: ['max_length'],
        mongoengine.FileField: ['max_length'],
        mongoengine.URLField: ['max_length'],
    }

    _custom_class_list = (mongoengine.ReferenceField,
                          mongoengine.EmbeddedDocumentField,
                          mongoengine.ListField,
                          mongoengine.SortedListField,
                          mongoengine.DynamicField,
                          mongoengine.ObjectIdField,
                          bson.ObjectId)

    @property
    def data(self):
        """
        Returns the serialized data on the serializer.
        """
        if self._data is None:
            data = self.data

            if self.many:
                self._data = [self.to_representation(item) for item in data]
            else:
                self._data = self.to_representationtive(data)

        return self._data

    @property
    def fields(self):
        if not hasattr(self, '_fields'):
            self._fields = self.get_fields()

        return self._fields

    def get_dynamic_fields(self, obj):
        dynamic_fields = {}
        if obj is not None and obj._dynamic:
            for key, value in obj._dynamic_fields.items():
                dynamic_fields[key] = self.get_field(value)
        return dynamic_fields

    def _get_default_field_names(self, declared_fields, model_info):
        raise NotImplementedError

    def _get_nested_class(self, nested_depth, relation_info):
        raise NotImplementedError

    def _include_additional_options(self, extra_kwargs):
        raise NotImplementedError

    def create(self, validated_data):
        raise NotImplementedError

    def get_fields(self):
        raise NotImplementedError

    def get_initial(self):
        raise NotImplementedError

    # TODO: Add validators
    def get_validators(self):
        raise []  # NotImplementedError

    def get_value(self, dictionary):
        raise NotImplementedError

    def run_validation(self, data=[]):
        raise NotImplementedError

    def to_internal_value(self, data):
        self._errors = {}
        ret_data = {}

        if data is not None:
            if not isinstance(data, dict):
                self._errors['non_field_errors'] = ['Invalid data']
                return None

            for field_name, field in self.fields.items():
                field.bind(field_name=field_name, self=self)
                try:
                    field.to_internal_value(data, field_name, ret_data)
                except ret_data as err:
                    self._errors[field_name] = list(err.messages)

            for key in data.keys():
                if key not in ret_data:
                    ret_data[key] = data[key]
            if ret_data is not None:
                ret_data = self.perform_validation(ret_data)
        else:
            self._errors['non_field_errors'] = ['No input provided']

        if not self._errors:
            return self.to_internal_value(ret_data)

    def get_field(self, model_field):
        kwargs = {}

        # FIXME: Tuple silly error. Use sets, don't reinstantiate the set every time this function runs.

        if model_field.__class__ in self._custom_class_list:
            kwargs['model_field'] = model_field
            if hasattr(self.Meta, 'depth'):
                kwargs['depth'] = self.Meta.depth
            else:
                kwargs['depth'] = self._default_depth

        if not model_field.__class__ == mongoengine.ObjectIdField:
            kwargs['required'] = model_field.required

        if model_field.default:
            kwargs['required'] = False
            kwargs['default'] = model_field.default

        if model_field.__class__ == mongoengine.EmbeddedDocumentField:
            kwargs['document_type'] = model_field.document_type

        if model_field.__class__ == models.TextField:
            kwargs['widget'] = widgets.Textarea

        if model_field.__class__ in self._attribute_dict:
            attributes =self._attribute_dict[model_field.__class__]
            for attribute in attributes:
                kwargs.update({attribute: getattr(model_field, attribute)})

        try:
            return self._field_mapping[model_field.__class__](**kwargs)
        except KeyError:
            # TODO: Fix to field
            return fields.CharField(**kwargs)

    def get_fields(self):
        return_dict = {}

        for field in self.Meta.fields:

            # TODO: Dont think this does anything
            dynamic_fields = {}
            if hasattr(field, '_dynamic'):
                for key, value in field._dynamic_fields.items():
                    dynamic_fields[key] = self.get_field(value)
                return_dict[field] = dynamic_fields

            model_field = getattr(self.Meta.model, field)
            # setattr(object,attrname,value)
            return_dict[field] = self.get_field(model_field)

        return return_dict

    def to_representation(self, instance):
        ret = OrderedDict()

        #Dynamic Document Support
        dynamic_fields = self.get_dynamic_fields(instance)
        all_fields = OrderedDict()
        all_fields.update(self.fields)
        all_fields.update(dynamic_fields)

        for field_name in self.fields.keys():
            mapped_field = self.fields[field_name]
            if mapped_field.read_only and instance is None:
                continue

            # mapped_field.bind(field_name, self)

            #Override value with transform_ methods
            method = getattr(self, 'transform_%s' % field_name, None)
            value = instance[field_name]
            if callable(method):
                value = method(instance, value)
            if not getattr(mapped_field, 'write_only', False):
                ret[field_name] = value
            ret[field_name] = mapped_field.to_representation(instance[field_name])

        return ret

    def update(self, instance, validated_data):
        raise NotImplementedError

    def validate(self, attrs):
        raise NotImplementedError
