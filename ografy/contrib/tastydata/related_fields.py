# TODO: FIX BIGTIME for reference field!
from bson.errors import InvalidId
from django.core.exceptions import ValidationError
from mongoengine import dereference
from mongoengine.document import Document
from rest_framework.relations import HyperlinkedRelatedField
from rest_framework.reverse import reverse

from ografy.contrib.tastydata.fields import DocumentField


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
        self.depth = kwargs.pop('depth')
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
        return self.transform_object(value, self.depth - 1)
    # lookup_field = 'pk'
    #
    # # TODO : Implement as in DRF?
    # # default_error_messages  = {
    # # 'invalid_dbref': _('Unable to convert to internal value.'),
    # #      'invalid_doc': _('DBRef invalid dereference.'),
    # #      'required': _('This field is required.'),
    # #      'no_match': _('Invalid hyperlink - No URL match.'),
    # #      'incorrect_match': _('Invalid hyperlink - Incorrect URL match.'),
    # #      'does_not_exist': _('Invalid hyperlink - Object does not exist.'),
    # #      'incorrect_type': _('Incorrect type. Expected URL string, received {data_type}.'),
    # #  }
    #
    # type_label = 'ReferenceField'
    #
    # def __init__(self, *args, **kwargs):
    #     self.view_name = kwargs.pop('view_name', None)
    #     self.depth = kwargs.pop('depth', 5)
    #     self.lookup_field = kwargs.pop('lookup_field', self.lookup_field)
    #     self.lookup_url_kwarg = kwargs.pop('lookup_url_kwarg', self.lookup_field)
    #     self.format = kwargs.pop('format', None)
    #     self.queryset = kwargs.pop('queryset', None)
    #
    #     # We include this simply for dependency injection in tests.
    #     # We can't add it as a class attributes or it would expect an
    #     # implicit `self` argument to be passed.
    #     self.reverse = reverse
    #     super(ReferenceField, self).__init__(*args, **kwargs)
    #
    # def use_pk_only_optimization(self):
    #     return self.lookup_field == 'pk'
    #
    # def get_queryset(self):
    #     def get(lookup_kwargs):
    #         return self.queryset
    #
    # def get_object(self, view_name, view_args, view_kwargs):
    #     """
    #     Return the object corresponding to a matched URL.
    #
    #     Takes the matched URL conf arguments, and should return an
    #     object instance, or raise an `ObjectDoesNotExist` exception.
    #     """
    #     lookup_value = view_kwargs[self.lookup_url_kwarg]
    #     lookup_kwargs = {self.lookup_field: lookup_value}
    #     return self.get_queryset().get(**lookup_kwargs)
    #
    # def get_url(self, obj, view_name, request, format):
    #     """
    #     Given an object, return the URL that hyperlinks to the object.
    #
    #     May raise a `NoReverseMatch` if the `view_name` and `lookup_field`
    #     attributes are not configured to correctly match the URL conf.
    #     """
    #     # Unsaved objects will not yet have a valid URL.
    #     if obj.pk is None:
    #         return None
    #
    #     lookup_value = getattr(obj, self.lookup_field)
    #     kwargs = {self.lookup_url_kwarg: lookup_value}
    #     return self.reverse(view_name, kwargs=kwargs, request=request, format=format)
    #
    # def to_internal_value(self, data):
    #     request = self.context.get('request', None)
    #     try:
    #         http_prefix = data.startswith(('http:', 'https:'))
    #     except AttributeError:
    #         self.fail('incorrect_type', data_type=type(data).__name__)
    #
    #     if http_prefix:
    #         # If needed convert absolute URLs to relative path
    #         data = urlparse.urlparse(data).path
    #         prefix = get_script_prefix()
    #         if data.startswith(prefix):
    #             data = '/' + data[len(prefix):]
    #
    #     try:
    #         match = resolve(data)
    #     except Resolver404:
    #         self.fail('no_match')
    #
    #     try:
    #         expected_viewname = request.versioning_scheme.get_versioned_viewname(self.view_name, request)
    #     except AttributeError:
    #         expected_viewname = self.view_name
    #
    #     if match.view_name != expected_viewname:
    #         self.fail('incorrect_match')
    #
    #     try:
    #         return self.get_object(match.view_name, match.args, match.kwargs)
    #     except (ObjectDoesNotExist, TypeError, ValueError):
    #         self.fail('does_not_exist')
    #
    #         # try:
    #         #     dbref = self.model_field.to_python(data)
    #         # except InvalidId:
    #         #     raise ValidationError(self.error_messages['invalid_dbref'])
    #         #
    #         # instance = dereference.DeReference()([dbref])[0]
    #         #
    #         # # Check if dereference was successful
    #         # if not isinstance(instance, Document):
    #         #     msg = self.error_messages['invalid_doc']
    #         #     raise ValidationError(msg)
    #         #
    #         # return instance
    #
    # def to_representation(self, value):
    #     request = self.context.get('request', None)
    #     format = self.context.get('format', None)
    #
    #     assert request is not None, (
    #         "`%s` requires the request in the serializer"
    #         " context. Add `context={'request': request}` when instantiating "
    #         "the serializer." % self.__class__.__name__
    #     )
    #
    #     # By default use whatever format is given for the current context
    #     # unless the target is a different type to the source.
    #     #
    #     # Eg. Consider a HyperlinkedIdentityField pointing from a json
    #     # representation to an html property of that representation...
    #     #
    #     # '/snippets/1/' should link to '/snippets/1/highlight/'
    #     # ...but...
    #     # '/snippets/1/.json' should link to '/snippets/1/highlight/.html'
    #     if format and self.format and self.format != format:
    #         format = self.format
    #
    #     # Return the hyperlink, or error if incorrectly configured.
    #     try:
    #         return self.get_url(value, self.view_name, request, format)
    #     except NoReverseMatch:
    #         msg = (
    #             'Could not resolve URL for hyperlinked relationship using '
    #             'view name "%s". You may have failed to include the related '
    #             'model in your API, or incorrectly configured the '
    #             '`lookup_field` attribute on this field.'
    #         )
    #         raise ImproperlyConfigured(msg % self.view_name)
    #         # return self.transform_object(value, self.depth - 1)


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

    # TODO : Implement as in DRF?
    # default_error_messages = {
    #      'required': _('This field is required.'),
    #      'no_match': _('Invalid hyperlink - No URL match.'),
    #      'incorrect_match': _('Invalid hyperlink - Incorrect URL match.'),
    #      'does_not_exist': _('Invalid hyperlink - Object does not exist.'),
    #      'incorrect_type': _('Incorrect type. Expected URL string, received {data_type}.'),
    #  }

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

    # TODO : Implement as in DRF?
    # default_error_messages  = {
    # 'invalid_dbref': _('Unable to convert to internal value.'),
    #      'invalid_doc': _('DBRef invalid dereference.'),
    #      'required': _('This field is required.'),
    #      'no_match': _('Invalid hyperlink - No URL match.'),
    #      'incorrect_match': _('Invalid hyperlink - Incorrect URL match.'),
    #      'does_not_exist': _('Invalid hyperlink - Object does not exist.'),
    #      'incorrect_type': _('Incorrect type. Expected URL string, received {data_type}.'),
    #  }

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
