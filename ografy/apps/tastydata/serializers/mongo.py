import bson
import jsonpickle
import mongoengine
import warnings

from bson.json_util import dumps as bson_dumps, loads as bson_loads
from collections import OrderedDict
from django.core.paginator import Page
from django.db import models
from django.forms import widgets
from mongoengine.base import BaseDocument
from rest_framework import fields, relations, serializers
from ografy.apps.tastydata.fields.mongo import ReferenceField, ListField, EmbeddedDocumentField, DynamicField, ObjectIdField


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
        mongoengine.DynamicField: DynamicField,
        mongoengine.EmailField: fields.EmailField,
        mongoengine.EmbeddedDocumentField: EmbeddedDocumentField,
        mongoengine.FileField: fields.FileField,
        mongoengine.FloatField: fields.FloatField,
        mongoengine.ImageField: fields.ImageField,
        mongoengine.IntField: fields.IntegerField,
        mongoengine.ListField: ListField,
        mongoengine.ObjectIdField: ObjectIdField,
        mongoengine.ReferenceField: ReferenceField,
        mongoengine.SortedListField: ListField,
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
                          mongoengine.ObjectIdField)

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
        raise NotImplementedError

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
        ret.fields = OrderedDict()

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
            ret.fields[field_name] = mapped_field

        # for field_name in self.fields.keys():
        #     mapped_field = self.fields[field_name]
        #
        #     # FIXME: Make less awful
        #     if isinstance(instance[field_name], bson.ObjectId):
        #         ret[field_name] = jsonpickle.decode(bson_dumps(instance[field_name]))['$oid']
        #
        #     elif isinstance(mapped_field, fields.Field):
        #
        #         if type(mapped_field) == fields.Field:
        #             # ret[field_name] = jsonpickle.decode(Document.to_json(instance[field_name]))
        #             ret[field_name] = None
        #         else:
        #             ret[field_name] = mapped_field.to_representation(instance[field_name])
        #
        #     else:
        #         ret[field_name] = None

        return ret

    def update(self, instance, validated_data):
        raise NotImplementedError

    def validate(self, attrs):
        raise NotImplementedError
