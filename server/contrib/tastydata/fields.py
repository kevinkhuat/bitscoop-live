from bson.errors import InvalidId
from django.core.exceptions import ValidationError
from django.utils.encoding import smart_str
from mongoengine import dereference
from mongoengine.base.document import BaseDocument
from mongoengine.document import Document
from mongoengine.fields import ObjectId, ReferenceField as MongoReferenceField
from rest_framework import serializers
from rest_framework.relations import HyperlinkedRelatedField
from rest_framework.reverse import reverse


class DocumentField(serializers.Field):
    """
    Base field for Mongoengine fields that we can not convert to DRF fields.
    To Users:
        - You can subclass DocumentField to implement custom (de)serialization
    """

    type_label = 'DocumentField'

    def __init__(self, *args, **kwargs):
        self.depth = kwargs.pop('depth')
        try:
            self.model_field = kwargs.pop('model_field')
        except KeyError:
            raise ValueError('%s requires `model_field` kwarg' % self.type_label)

        super(DocumentField, self).__init__(*args, **kwargs)

    def transform_document(self, document, depth):
        data = {}

        # serialize each required field
        for field in document._fields:
            if hasattr(document, smart_str(field)):
                # finally check for an attribute 'field' on the instance
                obj = getattr(document, field)
            else:
                continue

            val = self.transform_object(obj, depth - 1)

            if val is not None:
                data[field] = val

        return data

    def transform_dict(self, obj, depth):
        return dict([(key, self.transform_object(val, depth - 1)) for key, val in obj.items()])

    def transform_object(self, obj, depth):
        """
        Models to natives
        Recursion for (embedded) objects  
        """
        if isinstance(obj, BaseDocument):
            # Document, EmbeddedDocument
            if depth == 0:
                # Return primary key if exists, else return default text
                return smart_str(getattr(obj, 'pk', 'Max recursion depth exceeded'))
            return self.transform_document(obj, depth)
        elif isinstance(obj, dict):
            # Dictionaries
            return self.transform_dict(obj, depth)
        elif isinstance(obj, list):
            # List
            return [self.transform_object(value, depth) for value in obj]
        elif obj is None:
            return None
        else:
            return smart_str(obj) if isinstance(obj, ObjectId) else obj

    def to_internal_value(self, data):
        return self.model_field.to_python(data)

    def to_representation(self, value):
        return self.transform_object(value, self.depth)


class ListField(DocumentField):

    type_label = 'ListField'

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_internal_value(self, data):
        return self.model_field.to_python(data)

    def to_representation(self, value):
        if value is None:
            return None
        else:
            return_list = []

            for item in value:
                if isinstance(item, BaseDocument):
                    val = ReferenceField.to_representation(item, item)
                else:
                    val = self.transform_object(item, self.depth - 1)

                return_list.append(val)

        return return_list


class DynamicField(DocumentField):

    type_label = 'DynamicField'

    def __init__(self, field_name=None, source=None, *args, **kwargs):
        super(DynamicField, self).__init__(*args, **kwargs)
        self.field_name = field_name
        self.source = source
        if source:
            self.source_attrs = self.source.split('.')

    def to_representation(self, value):
        return self.model_field.to_python(value)


class ObjectIdField(DocumentField):

    type_label = 'ObjectIdField'

    def to_representation(self, value):
        return smart_str(value)

    def to_internal_value(self, data):
        return ObjectId(data)


class BinaryField(DocumentField):

    type_label = 'BinaryField'

    def __init__(self, **kwargs):
        try:
            self.max_bytes = kwargs.pop('max_bytes')
        except KeyError:
            raise ValueError('BinaryField requires "max_bytes" kwarg')
        super(BinaryField, self).__init__(**kwargs)

    def to_representation(self, value):
        return smart_str(value)

    def to_internal_value(self, data):
        return super(BinaryField, self).to_internal_value(smart_str(data))


class BaseGeoField(DocumentField):

    type_label = 'BaseGeoField'


class SortedListField(DocumentField):
    type_label = 'SortedListField'

    def __init__(self, *args, **kwargs):
        super(SortedListField, self).__init__(*args, **kwargs)

    def to_internal_value(self, data):
        return self.model_field.to_python(data)

    def to_representation(self, value):
        return self.transform_object(value, self.depth - 1)


class ReferenceField(DocumentField):
    """
    Field representing an association between Mongo Documents used in the Serializer.
    This field uses the references found in Mongoengine ReferenceField.

    Attributes are the same as in HyperlinkedRelatedFields in DRF
    Attributes:
    view_name
    depth
    lookup_field
    lookup_url_kwself.__class__.serializer(inst, **kwargs).dataarg
    format
    queryset
    """
    # TODO: FIX BIGTIME!
    default_error_messages = {
        'invalid_dbref': ('Unable to convert to internal value.'),
        'invalid_doc': ('DBRef invalid dereference.'),
    }

    type_label = 'ReferenceField'

    def __init__(self, *args, **kwargs):
        super(ReferenceField, self).__init__(*args, **kwargs)

    def to_internal_value(self, data):
        try:
            dbref = self.model_field.to_python(data)
        except InvalidId:
            raise ValidationError(self.error_messages['invalid_dbref'])

        instance = dereference.DeReference()([dbref])[0]

        # Check if dereference was successful
        if not isinstance(instance, Document):
            msg = self.error_messages['invalid_doc']
            raise ValidationError(msg)

        return instance

    def to_representation(self, value):
        if hasattr(value, 'id'):
            return smart_str(value.id)
        else:
            return None


class HydratedReferenceField(DocumentField):
    """
    Field representing an association between Mongo Documents used in the Serializer.
    This field uses the references found in Mongoengine ReferenceField.

    Attributes are the same as in HyperlinkedRelatedFields in DRF
    Attributes:
    view_name
    depth
    lookup_field
    lookup_url_kwself.__class__.serializer(inst, **kwargs).dataarg
    format
    queryset
    """
    # TODO: FIX BIGTIME!
    default_error_messages = {
        'invalid_dbref': ('Unable to convert to internal value.'),
        'invalid_doc': ('DBRef invalid dereference.'),
    }

    type_label = 'HydratedReferenceField'

    def __init__(self, *args, **kwargs):
        super(HydratedReferenceField, self).__init__(*args, **kwargs)

    def to_internal_value(self, data):
        try:
            dbref = self.model_field.to_python(data)
        except InvalidId:
            raise ValidationError(self.error_messages['invalid_dbref'])

        instance = dereference.DeReference()([dbref])[0]

        # Check if dereference was successful
        if not isinstance(instance, Document):
            msg = self.error_messages['invalid_doc']
            raise ValidationError(msg)

        return instance

    def to_representation(self, value):
        return self.transform_object(value, self.depth - 1)


class DjangoField(HyperlinkedRelatedField):
    """
    Field representing an association From a Mongo Document to a Django Model used in the Serializer.

    Attributes are the same as in HyperlinkedRelatedFields in DRF
    Attributes:
    view_name
    depth
    lookup_field
    lookup_url_kwarg
    format
    queryset
    """
    lookup_field = 'pk'

    type_label = 'DjangoField'

    def __init__(self, view_name=None, **kwargs):
        assert view_name is not None, 'The `view_name` argument is required.'
        self.view_name = view_name
        self.lookup_field = kwargs.pop('lookup_field', self.lookup_field)
        self.lookup_url_kwarg = kwargs.pop('lookup_url_kwarg', self.lookup_field)
        self.format = kwargs.pop('format', None)

        # We include this simply for dependency injection in tests.
        # We can't add it as a class attributes or it would expect an
        # implicit `self` argument to be passed.
        self.reverse = reverse

        super(HyperlinkedRelatedField, self).__init__(**kwargs)


class MongoField(ReferenceField):
    """
    Field representing an association from a Django Model to a Mongo Document used in the Serializer.

    Attributes are the same as in HyperlinkedRelatedFields in DRF
    Attributes:
    view_name
    depth
    lookup_field
    lookup_url_kwarg
    format
    queryset
    """
    lookup_field = 'pk'

    type_label = 'MongoField'

    def __init__(self, *args, **kwargs):
        self.view_name = kwargs.pop('view_name', self.view_name)
        self.depth = kwargs.pop('depth')
        self.lookup_field = kwargs.pop('lookup_field', self.lookup_field)
        self.lookup_url_kwarg = kwargs.pop('lookup_url_kwarg', self.lookup_field)
        self.format = kwargs.pop('format', None)
        self.queryset = kwargs.pop('queryset', None)

        # We include this simply for dependency injection in tests.
        # We can't add it as a class attributes or it would expect an
        # implicit `self` argument to be passed.
        self.reverse = reverse
        super(ReferenceField, self).__init__(*args, **kwargs)


class EmbeddedDocumentField(DocumentField):
    type_label = 'EmbeddedDocumentField'

    def __init__(self, *args, **kwargs):
        try:
            self.document_type = kwargs.pop('document_type')
        except KeyError:
            raise ValueError('EmbeddedDocumentField requires `document_type` kwarg')

        super(EmbeddedDocumentField, self).__init__(*args, **kwargs)

    def to_representation(self, value):
        data = {}

        # serialize each required field
        for field_name, field_value in value._fields.items():
            if hasattr(value, smart_str(field_name)):
                # finally check for an attribute 'field' on the instance
                obj = getattr(value, field_name)
            else:
                continue

            if isinstance(field_value, MongoReferenceField):
                val = ReferenceField.to_representation(field_value, obj)
            else:
                val = self.transform_object(obj, self.depth - 1)

            if val is not None:
                data[field_name] = val

        return data

    def to_internal_value(self, data):
        return self.model_field.to_python(data)


class EmbeddedDocumentListField(DocumentField):
    type_label = 'EmbeddedDocumentListField'

    def __init__(self, *args, **kwargs):
        super(EmbeddedDocumentListField, self).__init__(*args, **kwargs)

    def to_representation(self, value):
        if value is None:
            return None
        else:
            return_list = []

            for item in value:
                return_list.append(EmbeddedDocumentField.to_representation(self, item))

            return return_list

    def to_internal_value(self, data):
        return self.model_field.to_python(data)
