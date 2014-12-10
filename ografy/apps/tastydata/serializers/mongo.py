import mongoengine
from mongoengine import fields as mongo_fields
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







    #
    #
    # def get_dynamic_fields(self, obj):
    #     dynamic_fields = {}
    #     if obj is not None and obj._dynamic:
    #         for key, value in obj._dynamic_fields.items():
    #             dynamic_fields[key] = self.get_field(value)
    #     return dynamic_fields
    #
    # # TODO: Create and Update should be broken out for each type?
    # def restore_object(self, validated_data, instance=None):
    #     if instance is None:
    #         instance = self.opts.model()
    #
    #     dynamic_fields = self.get_dynamic_fields(instance)
    #     all_fields = dict(dynamic_fields, **self.fields)
    #
    #     for key, val in validated_data.items():
    #         field = all_fields.get(key)
    #         if not field or field.read_only:
    #             continue
    #
    #         if isinstance(field, serializers.ModelSerializer):
    #             many = field.many
    #
    #             def _restore(field, item):
    #                 # looks like a bug, sometimes there are decerialized objects in attrs
    #                 # sometimes they are just dicts
    #                 if isinstance(item, BaseDocument):
    #                     return item
    #                 return field.to_internal_value(item)
    #
    #             if many:
    #                 val = [_restore(field, item) for item in val]
    #             else:
    #                 val = _restore(field, val)
    #
    #         key = getattr(field, 'source', None) or key
    #         try:
    #             setattr(instance, key, val)
    #         except ValueError:
    #             self._errors[key] = self.error_messages['required']
    #
    #     return instance
    #
    # def create(self, validated_data):
    #     raise NotImplementedError
    #
    # def update(self, instance, validated_data):
    #     raise NotImplementedError
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
    #
    # # # FIXME: Move fields.py transform_<field_name> to here
    # # def to_representation(self, instance):
    # #     ret = super(MongoEngineModelSerializer, self).to_representation(instance)
    # #     for key, value in ret.items():
    # #         method = getattr(self, 'transform_' + key, None)
    # #         if method is not None:
    # #             ret[key] = method(value)
    # #     return ret
    #
    # def to_internal_value(self, data):
    #     """
    #     Rest framework built-in to_native + transform_object
    #     """
    #     ret = self._dict_class()
    #     ret.fields = self._dict_class()
    #
    #     #Dynamic Document Support
    #     dynamic_fields = self.get_dynamic_fields(data)
    #     all_fields = self._dict_class()
    #     all_fields.update(self.fields)
    #     all_fields.update(dynamic_fields)
    #
    #     for field_name, field in all_fields.items():
    #         if field.read_only and data is None:
    #             continue
    #         field.initialize(parent=self, field_name=field_name)
    #         key = self.get_field_key(field_name)
    #         value = fields.get_attribute(data, field_name)
    #         #Override value with transform_ methods
    #         method = getattr(self, 'transform_%s' % field_name, None)
    #         if callable(method):
    #             value = method(data, value)
    #         if not getattr(field, 'write_only', False):
    #             ret[key] = value
    #         ret.fields[key] = self.augment_field(field, field_name, key, value)
    #
    #     return ret
