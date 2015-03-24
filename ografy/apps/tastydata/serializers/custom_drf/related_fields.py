# from django.utils.translation import ugettext_lazy as _
from rest_framework.reverse import reverse

from ografy.apps.tastydata.serializers.custom_drf_mongoengine.related_fields import ReferenceField


class MongoRefField(ReferenceField):
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

    type_label = 'MongoRefField'

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
