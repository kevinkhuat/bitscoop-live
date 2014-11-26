from django.db.models.fields import CharField
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _


class NullCharField(CharField):
    """
    Character field that obeys uniqueness and nullability enforced in the database
    """
    description = _('Nullable string (up to %(max_length)s)')

    def __init__(self, *args, **kwargs):
        kwargs['null'] = True
        kwargs['blank'] = True

        super(NullCharField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            return ''

        if isinstance(value, CharField):
            return value

        return smart_text(value)

    def get_prep_value(self, value):
        if not value:
            return None

        if isinstance(value, CharField):
            return value

        return smart_text(value)
