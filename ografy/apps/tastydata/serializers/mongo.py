import bson
import jsonpickle
import mongoengine
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

    def to_representation(self, instance):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError

    def validate(self, attrs):
        raise NotImplementedError

    @property
    def data(self):
        self._data = self.to_representation(self.instance)
        return self._data


def get_serialized_dict(self, obj):
    serialized_object = self.serialize(obj)
    return jsonpickle.decode(serialized_object)


def get_serialized_value(self, obj, key):
    return self.get_serialized_dict(obj)[key]


def create_object_id(id):
    return bson.ObjectId(id)

