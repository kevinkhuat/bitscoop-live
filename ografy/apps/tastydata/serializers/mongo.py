import jsonpickle
import bson
import mongoengine

from collections import OrderedDict
from django.db import models
from django.forms import widgets
from mongoengine import Document, fields as mongo_fields
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
    _field_mapping = {
        mongoengine.BooleanField: fields.BooleanField,
        mongoengine.DateTimeField: fields.DateTimeField,
        mongoengine.DecimalField: fields.DecimalField,
        mongoengine.DynamicField: mongo_fields.DynamicField,
        mongoengine.EmailField: fields.EmailField,
        mongoengine.EmbeddedDocumentField: mongo_fields.EmbeddedDocumentField,
        mongoengine.FileField: fields.FileField,
        mongoengine.FloatField: fields.FloatField,
        mongoengine.ImageField: fields.ImageField,
        mongoengine.IntField: fields.IntegerField,
        mongoengine.ListField: mongo_fields.ListField,
        mongoengine.ObjectIdField: fields.Field,
        mongoengine.ReferenceField: mongo_fields.ReferenceField,
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

    def get_validators(self):
        raise NotImplementedError

    def get_value(self, dictionary):
        raise NotImplementedError

    def run_validation(self, data=fields.empty):
        raise NotImplementedError

    def to_internal_value(self, data):
        raise NotImplementedError

    def get_field(self, model_field):
        kwargs = {}

        # FIXME: Tuple silly error. Use sets, don't reinstantiate the set every time this function runs.

        if model_field.__class__ in (mongoengine.ReferenceField, mongoengine.EmbeddedDocumentField,
                                     mongoengine.ListField, mongoengine.DynamicField):
            kwargs['model_field'] = model_field
            kwargs['depth'] = self.opts.depth

        if not model_field.__class__ == mongoengine.ObjectIdField:
            kwargs['required'] = model_field.required

        if model_field.__class__ == mongoengine.EmbeddedDocumentField:
            kwargs['document_type'] = model_field.document_type

        if model_field.default:
            kwargs['required'] = False
            kwargs['default'] = model_field.default

        if model_field.__class__ == models.TextField:
            kwargs['widget'] = widgets.Textarea

        if model_field.__class__ in self._attribute_dict:
            attributes =self._attribute_dict[model_field.__class__]
            for attribute in attributes:
                kwargs.update({attribute: getattr(model_field, attribute)})

        try:
            return self._field_mapping[model_field.__class__](**kwargs)
        except KeyError:
            return fields.CharField(**kwargs)

    def get_fields(self):
        return_dict = {}

        for field in self.Meta.fields:
            model_field = getattr(self.Meta.model, field)
            # setattr(object,attrname,value)
            return_dict[field] = self.get_field(model_field)

        return return_dict

    @property
    def fields(self):
        if not hasattr(self, '_fields'):
            self._fields = self.get_fields()

        return self._fields

    def to_representation(self, instance):
        ret = OrderedDict()

        model_serializer = super(serializers.ModelSerializer, self)

        for field_name in self.fields.keys():
            mapped_field = self.fields[field_name]
            if isinstance(mapped_field, fields.Field):
                try:
                    ret[field_name] = mapped_field.to_representation(instance[field_name])
                except NotImplementedError:
                    ret[field_name] = None  # bson.ObjectId.to_json(instance[field_name])
            else:
                ret[field_name] = None

        return ret

    def update(self, instance, validated_data):
        raise NotImplementedError

    def validate(self, attrs):
        raise NotImplementedError

    @property
    def data(self):
        self._data = self.to_representation(self.instance)
        return self._data

    # def get_dynamic_fields(self, obj):
    #     dynamic_fields = {}
    #     if obj is not None and obj._dynamic:
    #         for key, value in obj._dynamic_fields.items():
    #             dynamic_fields[key] = self.get_field(value)
    #     return dynamic_fields
    #
    # def get_field(self, model_field):
    #     kwargs = {}
    #
    #     # FIXME: Tuple silly error. Use sets, don't reinstantiate the set every time this function runs.
    #     if model_field.__class__ in (mongoengine.ReferenceField, mongoengine.EmbeddedDocumentField, mongoengine.ListField, mongoengine.DynamicField):
    #         kwargs['model_field'] = model_field
    #         kwargs['depth'] = self.opts.depth
    #
    #     if not model_field.__class__ == mongoengine.ObjectIdField:
    #         kwargs['required'] = model_field.required
    #
    #     if model_field.__class__ == mongoengine.EmbeddedDocumentField:
    #         kwargs['document_type'] = model_field.document_type
    #
    #     if model_field.default:
    #         kwargs['required'] = False
    #         kwargs['default'] = model_field.default
    #
    #     if model_field.__class__ == models.TextField:
    #         kwargs['widget'] = widgets.Textarea
    #
    #     if model_field.__class__ in self._attribute_dict:
    #         attributes = self._attribute_dict[model_field.__class__]
    #         for attribute in attributes:
    #             kwargs.update({attribute: getattr(model_field, attribute)})
    #
    #     try:
    #         return self._field_mapping[model_field.__class__](**kwargs)
    #     except KeyError:
    #         # Defaults to WritableField if not in field mapping
    #         return fields.WritableField(**kwargs)
